# Cyber Defender: repositioning and product foundation

## Audit and before/after

Baseline: production commit `9d813f63ac8434a18e7f930fde01f8a540bec6b4`, Vercel project `cyberdefender-website`, verified 15 November 2026. Plain HTML/CSS and a small mobile-menu script; no dependencies, build pipeline, API, authentication, assessment engine, database or enquiry delivery. A static dashboard concept exists, explicitly illustrative. Pricing is proposed, not a live tariff. Booking and business contact details remain unconfigured. Existing noindex controls are intentionally preserved pending commercial readiness.

Previously: therapist-specific homepage, therapy-room images across general pages, practice-labelled packages and examples. Now: UK SME positioning, original product-overview SVG, Discover/Assess/Notify/Review journey, neutral business report and compact audience group. Existing identity, CSS, cards, prices and service scopes are retained. Therapist content and photography survive at `/industries/therapists`; the old URL redirects. `/security-notice` explains legitimacy checks and limits without publishing individual findings.

Research references: Intruder (https://www.intruder.io/) informed a product-first hierarchy; CyberSmart (https://cybersmart.co.uk/) informed audience-friendly service language; Detectify (https://detectify.com/) demonstrates separating discovery from assessment; SecurityScorecard (https://securityscorecard.com/) demonstrates risk overview presentation; Sophos (https://www.sophos.com/) demonstrates organised product navigation. Essential Cyber (https://essentialcyber.uk/index.html) and CCSW (https://ccsw.co.uk/it-services/cyber-essentials/) remain useful service/package references. These are design observations, not endorsements or claims of equivalent capability. No competitor assets or wording copied.

## Current trust and release gaps

- HTTPS and configured domains are present in Vercel; no certificate-chain or exhaustive security audit was performed.
- Existing nosniff, referrer policy and noindex response headers preserved. Consider tested CSP, framing restrictions, permissions policy and HSTS after checking all deployed integrations and subdomains; do not weaken protections to make embeds work.
- No form, analytics, cookies or third-party scripts were added. No working booking/calendar or inbound enquiry channel exists. Do not launch notifications until a verified business identity and reachable reply channel exist.
- Business registration, real contact details, competent service delivery, VAT, contracts and final prices need confirmation. Do not invent credentials or customer evidence.
- A privacy notice, service terms and data-handling/retention decisions are required before collecting customer information. Obtain current UK privacy/direct-marketing advice before outreach, including audience distinctions and objection handling. No outreach sent by this change.
- Release remains a preview. Production requires Rhys's approval. Search indexing remains disabled until launch readiness is confirmed.

## Proposed architecture (not implemented)

Keep the public marketing site static. Add an isolated authenticated application only after a separate implementation scope is approved. Suitable components: a maintained server-rendered application framework, managed identity provider with MFA support, server API, relational database with tenant enforcement, private object storage, queue/worker for authorised assessment jobs, and restricted reviewer console. Select vendors after reviewing residency, processor terms, cost and operational ownership; no vendor account is provisioned here.

Core records: organisation; membership and role; domain/asset ownership evidence with expiry; written engagement authorisation and asset scope; assessment with method/version/date/status; observation with source/time/attribution/confidence/limitations; human review decision; finding with severity separately from confidence; remediation action; report version; audit event. Every private record carries organisation identity and server-enforced access rules.

Requests must derive identity from a validated session, never a browser-supplied organisation ID. Check membership and object-level permission on every read, export and write. Use tenant isolation in the database as defence in depth. Test cross-tenant reads, writes and exports. Encrypt transport and managed storage; keep credentials in a secrets manager. Maintain least-privilege roles and audited administrative access.

Domain ownership verification should use a time-limited random challenge, such as an approved DNS record, verified server-side. Verification and written permission for assessment are distinct requirements. Email access alone does not authorise a whole domain, supplier infrastructure or another tenant's assets. Reverify after material changes or expiry.

Reports live in private storage. Authorise each download and use short-lived links where appropriate. A notice link is an opaque reference only, never a bearer credential to sensitive findings. Do not put findings, email addresses or evidence in URL parameters, public JavaScript or search indexes. Redact logs and define retention/deletion rules, backups and restore tests before production.

## Staged plan and acceptance gates

### 1. Credible assessment service

Confirm identity, contact channel, competence, scope, VAT, prices and contracts. Provide a real assessment enquiry with validation, abuse protection, minimal fields, retention and accurate success/failure states. Human-led review and secure handover first. Gate: a customer can enquire, agree scope and receive a genuine authorised report without sending passwords or unnecessary sensitive data.

### 2. Secure customer onboarding and reporting

Implement identity, organisation membership, ownership verification, consent/scope records and private report access. Gate: tenant isolation tests pass, invitations expire, account recovery is tested, logs exclude sensitive report contents and exports cannot cross organisations. Complete an independent security review before storing real findings.

### 3. Evidence and reviewer workflow

Start with customer-supplied evidence and approved passive sources. Record attribution, observation time, uncertainty and reproducibility. Human reviewers accept, reject or request evidence. Unknown is not failed. Gate: every released finding has traceable evidence, scope, confidence, limitations and a named reviewer. No public observation implies private MFA configuration or confirmed compromise.

### 4. AI-assisted analysis

Only after a separate scope and data-processing review: use AI to summarise and classify authorised evidence. Treat source material as untrusted data, isolate tool access and require human approval for released conclusions. Evaluate hallucinations, attribution, confidence calibration, sensitive-data leakage and prompt injection using labelled examples. Never let a model send notices or execute testing autonomously. Gate: documented quality thresholds, human review and audit history; model failure cannot publish unsupported findings.

### 5. Responsible notifications

Establish legal review, appropriate business recipient selection, suppression/objection handling, verified sender identity and reply channel. No automated prospect-discovery or bulk notification system is part of this work. Notices should be proportionate, minimally detailed and human-approved; never expose actionable technical evidence publicly. Gate: each notice has an attributable evidence record, reviewer, permitted recipient, safe verification route and a functioning response process.

### 6. Authorised reassessment and monitoring

Separately scope asset limits, cadence, permission expiry, supplier restrictions, safe execution, failure handling, operational response and costs. Do not silently expand from passive observations into active validation. Gate: job execution stays within current written authorisation, expired scope stops work, evidence timestamps and coverage gaps are shown and detection is never marketed as guaranteed protection.

## Future dashboard

Show organisation, verified assets, assessment date/status/scope, severity and confidence as separate fields, evidence labels, plain-English findings, recommended actions, owners, resolved/outstanding state, report downloads and reassessment history. Mark unassessed controls explicitly. Add no fake login, live feed or security rating during the marketing repositioning.

## Validation scope

No runtime JavaScript, dependencies, secrets, analytics or form-processing behaviour introduced. Validate routes/anchors, unchanged prices, image references, headings, navigation, responsive overflow and clearly labelled concepts. Browser screenshots support visual review; they are not accessibility certification or a penetration test. Unknown commercial and legal facts remain release action items.
