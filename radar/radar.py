"""Owned-domain research CLI. No arbitrary targets, port scans or outreach."""
import argparse
import datetime as dt
import hashlib
import html
import json
from pathlib import Path
import re
import shlex
import socket
import ssl
import urllib.request

DOMAIN = 'cyberdefender.services'
HOST = 'www.cyberdefender.services'
HEADERS = ('strict-transport-security', 'content-security-policy',
           'x-content-type-options', 'referrer-policy', 'permissions-policy',
           'x-frame-options')


def observation(check, status, evidence=None, interpretation='', classification='informational'):
    return dict(check=check, status=status, evidence=evidence,
                interpretation=interpretation, classification=classification,
                severity='unrated', confidence='observed' if status == 'observed' else 'unknown')


def dns_observation(check, payload):
    """Conservative TXT observation, not an SPF evaluator or DMARC validator."""
    if not isinstance(payload, dict) or payload.get('Status') not in (0, 3) or payload.get('TC'):
        return observation(check, 'unable_to_assess', interpretation='DNS request failed, was truncated or returned an unsupported response.')
    answers = payload.get('Answer', [])
    if not isinstance(answers, list) or any(not isinstance(a, dict) for a in answers):
        return observation(check, 'unable_to_assess', interpretation='Malformed DNS answer collection.')
    records = []
    for answer in answers:
        if answer.get('type') != 16:
            continue
        try:
            if not isinstance(answer.get('data'), str):
                raise ValueError('Invalid TXT data')
            parts = shlex.split(answer['data'])
            text = ''.join(parts) if answer['data'].startswith('"') else answer['data']
        except (KeyError, ValueError, TypeError):
            return observation(check, 'unable_to_assess', interpretation='TXT evidence could not be parsed.')
        prefix = 'v=spf1' if check == 'spf' else 'v=DMARC1'
        if re.match(re.escape(prefix) + r'(?:\s|;|$)', text, re.I):
            records.append(text)
    if not records:
        return observation(check, 'observed', [], 'No matching record returned for this exact queried name at this time. Review intended mail use; this does not establish compromise or effective inherited policy.', 'configuration_review')
    if len(records) > 1:
        return observation(check, 'observed', records, 'Multiple matching records returned; specialist configuration review recommended.', 'configuration_review')
    return observation(check, 'observed', records, 'Published record observed. This is not proof of effective authentication, message alignment, exploitability or account security. Full syntax and dependency evaluation not performed.')


def header_observations(status, headers):
    if status != 200:
        return [observation(name, 'unable_to_assess', interpretation='Expected homepage response not obtained.') for name in HEADERS]
    normal = {k.lower(): v for k, v in headers.items()}
    return [observation(name, 'observed', normal.get(name),
            'Header present; policy correctness and effectiveness not evaluated.' if name in normal else
            'Not returned on this response. Contextual review only, not a confirmed vulnerability; equivalent controls may exist.',
            'informational' if name in normal else 'configuration_review') for name in HEADERS]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('Redirect not followed; scope is fixed.')


def request(url, limit=65536):
    # All URLs are constructed internally; callers cannot supply a target.
    with urllib.request.build_opener(NoRedirect).open(
        urllib.request.Request(url, headers={'User-Agent': 'CyberDefender-Owned-Domain-Research/0.1'}), timeout=8
    ) as response:
        raw = response.read(limit + 1)
        if len(raw) > limit:
            raise ValueError('Evidence response exceeds size limit')
        return response.status, dict(response.headers), raw


def collect():
    results, evidence = [], []
    for check, name in [('spf', DOMAIN), ('dmarc', '_dmarc.' + DOMAIN)]:
        url = 'https://dns.google/resolve?name=' + name + '&type=TXT'
        entry = dict(check=check, source=url, target=name, observed_at=now())
        try:
            status, headers, raw = request(url)
            payload = json.loads(raw)
            entry.update(http_status=status, sha256=hashlib.sha256(raw).hexdigest(), response=payload)
            item = dns_observation(check, payload) if status == 200 else observation(check, 'unable_to_assess')
        except (OSError, ValueError, TypeError) as exc:
            entry.update(error_type=type(exc).__name__, error=str(exc))
            item = observation(check, 'unable_to_assess', interpretation='Collection failed; no security conclusion.')
        item['evidence_index'] = len(evidence)
        evidence.append(entry)
        results.append(item)
    url = 'https://' + HOST + '/'
    entry = dict(check='https_headers', source=url, target=HOST, observed_at=now())
    try:
        status, headers, raw = request(url)
        # Body deliberately discarded; retain no customer or page contents.
        entry.update(http_status=status, headers={k.lower():v for k,v in headers.items() if k.lower() in HEADERS}, response_sha256=hashlib.sha256(raw).hexdigest())
        items = header_observations(status, headers)
    except (OSError, ValueError) as exc:
        entry.update(error_type=type(exc).__name__, error=str(exc))
        items = header_observations(None, {})
    for item in items:
        item['evidence_index'] = len(evidence)
    evidence.append(entry)
    results.extend(items)
    entry = dict(check='tls_handshake', source='TLS connection to '+HOST+':443', target=HOST, observed_at=now())
    try:
        with socket.create_connection((HOST, 443), timeout=8) as sock:
            with ssl.create_default_context().wrap_socket(sock, server_hostname=HOST) as secure:
                cert = secure.getpeercert()
                entry.update(protocol=secure.version(), not_after=cert.get('notAfter'), issuer=cert.get('issuer'))
                item = observation('tls_handshake', 'observed', entry.copy(), 'Local trust-store chain and hostname validation succeeded for one connection. Not a cipher-suite audit or comprehensive TLS assessment.')
    except (OSError, ValueError) as exc:
        entry.update(error_type=type(exc).__name__, error=str(exc))
        item = observation('tls_handshake', 'unable_to_assess', interpretation='Handshake did not complete. A client/environment error is not proof of server insecurity.')
    item['evidence_index'] = len(evidence)
    results.append(item)
    evidence.append(entry)
    for name, reason in [('dkim','No verified selector supplied; no guessing performed.'), ('certificate_transparency','No approved data provider integrated.'), ('software_advisories','No verified software version evidence supplied.'), ('breach_exposure','No verified provider access or customer authorisation configured.')]:
        results.append(observation(name, 'not_assessed', interpretation=reason))
    return dict(schema_version=1, mode='owned-domain-proof', generated_at=now(),
                targets=[DOMAIN,HOST], collector_version='0.1',
                limitations=['Point-in-time research only; no exploitability tests, mail delivery tests, recursive SPF evaluation, inherited DMARC discovery, security score or customer monitoring.', 'Environment and resolver caching can affect results. Raw DNS evidence retained for review.'],
                results=results, evidence=evidence,
                collection_complete=all(x['status']!='unable_to_assess' for x in results))


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def report(results):
    rows = ''.join('<tr>'+''.join('<td>'+html.escape(str(value))+'</td>' for value in
                   (x['check'],x['status'],x.get('evidence'),x.get('interpretation','')))+'</tr>' for x in results)
    return '<!doctype html><html lang="en"><meta charset="utf-8"><title>Radar research report</title><h1>Cyber Defender Radar: owned-domain research</h1><p>Point-in-time observations, not a security certificate. Failed and skipped checks remain explicit. No exploitability established.</p><table><tr><th>Check</th><th>Status</th><th>Evidence</th><th>Interpretation</th></tr>'+rows+'</table></html>'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    data = collect()
    (args.output/'observations.json').write_text(json.dumps(data,indent=2)+'\n')
    (args.output/'report.html').write_text(report(data['results']))
    print(json.dumps({'output':str(args.output),'collection_complete':data['collection_complete'], 'statuses':{x['check']:x['status'] for x in data['results']}}))
    raise SystemExit(0 if data['collection_complete'] else 2)
