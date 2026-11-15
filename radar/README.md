# Radar owned-domain proof of concept

Run `python3 -m unittest discover -s radar -v`, then `python3 radar/radar.py --output /tmp/radar-run` from the repository root. Python standard library only. This internal CLI is not deployed as a web API, is not a subscription service and does not accept a target argument.

The collector makes two DNS-over-HTTPS TXT requests to Google's documented JSON API for Cyber Defender's own root and DMARC name, one ordinary HTTPS homepage request, and one standard certificate-validating TLS handshake to its own hostname. It performs no credential testing, exploit checks, port enumeration, subdomain probing or prospecting. Redirects are refused. Requests have eight-second timeouts and response-size limits. There is no background scheduler, arbitrary URL input, parallel job execution or automatic notification.

Output: observations.json with UTC timestamps, raw DNS responses, source URLs, limited response-header evidence, hashes, interpretations and collection errors; report.html with escaped evidence. Exit 2 means an implemented collection failed; skipped checks never turn into passes. Output belongs outside dist. Do not publish customer findings in the marketing bundle.

SPF/DMARC parsing recognises published record prefixes and multiple matching records. It is NOT a full syntax validator, SPF include evaluator, DNSSEC verifier, inherited DMARC policy discovery or message authentication test. Missing header observations are contextual review items, not confirmed vulnerabilities. No severity is assigned automatically. An ordinary successful HTTPS fetch is not a full TLS configuration audit.

## Observed environment behaviour, 15 November 2026

Python urllib HTTPS requests reached both Google's DNS API and Cyber Defender's homepage. The direct socket TLS path failed at getaddrinfo with gaierror. This is consistent with different connectivity paths in the available runtime; no claim is made about the earlier pilot's exact failure cause. HTTPS collection works here; direct certificate inspection requires an approved runtime with functioning socket DNS. Do not disable certificate verification, use untrusted proxies or infer certificate failure from this error.

The recorded owned-domain run returned no matching root SPF record and a DMARC record with p=quarantine. Selected headers were present; other selected headers were not returned by that homepage response. These are point-in-time observations, not compromise findings. TLS remains unable_to_assess. DKIM needs a verified selector; certificate transparency, software applicability and breach exposure integrations are not implemented.

## Provider feasibility

Google's documented DoH JSON interface is usable for this bounded prototype: https://developers.google.com/speed/public-dns/docs/doh/json. Review current terms, quotas, caching and support suitability before production. No paid service was purchased. DomainDNSCheck integration is deferred: a supported API and commercial terms were not established. Have I Been Pwned requires its documented plan/access and verification arrangements: https://haveibeenpwned.com/API/v3. No breach data was queried. Certificate transparency and domain-registration APIs require provider selection; no host probing should follow automatically.

Before extending this code: obtain a separate authorised implementation scope, real ownership/authorisation records and a bounded worker design. This is intentionally not a reusable third-party prospect scanning system.
