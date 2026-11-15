# Radar: product, security and commercial delivery plan

## Current implementation

The broad website preview already exists on the repositioning branch; production remains the earlier therapist-focused site pending approval. This iteration adds a public Radar status page and an internal fixed-own-domain CLI with a tested evidence model. It adds no customer authentication, billing, AI service, background monitoring, inbound contact processing or outbound prospecting system. The existing prices are unchanged. No new service can be purchased through this preview.

## Architecture and data contracts

Keep marketing static. Add a separate maintained server application and managed identity only after a scoped release decision. Use a relational database, private report storage and bounded asynchronous workers rather than browser-driven jobs or premature microservices.

Records: Organisation, User, Membership(role), Asset, DomainVerification(challenge hash, expiry, verified_at), Authorization(asset scope, techniques, windows, exclusions, stop conditions, expiry), Assessment, Job(idempotency key, time budget, attempts, state), Observation(source, timestamp, raw evidence reference, confidence, limitations, error), Finding(reviewed severity separate from confidence), Report(version), Remediation(quote, customer approval, rollback, verification), Subscription, UsageAllowance, Conversation, SupportTicket, Notification and AuditEvent. Prospect, OutreachRecord and SuppressionRecord would be a separately permissioned future business process, not a source of customer assessment authority.

Enforce organisation identity from authenticated server sessions, object-level permissions on every query/export, database tenant restrictions, least privilege, private storage, short-lived authorised downloads, redacted logs and explicit retention. No predictable public report URLs. Domain ownership verification and permission to test are separate checks. Email notification links are not ownership proof. Customer/customer and analyst/customer cross-tenant access tests are release blockers.

Dashboard navigation: Overview, Radar, Findings, Reports, AI Analyst, Human Support, Assets, Billing, Settings. Show last successful and next scheduled check, coverage, failed jobs and unassessed controls. No universal safety score. Human analyst views require time-bounded role permissions and customer-approved context; revocation and access history are mandatory.

## AI Analyst and human support

Start read-only. Retrieve only current-organisation reports through a server-authorised service. Cite finding ID, source date and limitations. Treat retrieved documents as untrusted data, never tool instructions. Allow no model-triggered testing, configuration changes, payments or outbound messages. Test cross-tenant requests, invented findings, stale evidence, prompt injection, unsafe suggestions and unavailable data before customer use.

Handover creates a support ticket with customer-selected findings and a consented conversation summary. Record who can access it, expiry and revocation. Publish real human support hours, included minutes/tickets and response targets only after staffing is confirmed. “Fix this for me” creates a scope/quote/approval task, not an automatic repair. Verify completion independently before closing the finding.

## Commercial experiment, not approved tariffs

Keep existing public figures. Proposed £50 initial assessment and US$100 monthly plan require validation; no currency conversion or new pricing was applied. Do not imply five monthly penetration tests. A future allowance would cover five precisely defined, authorised automated assessment jobs, subject to asset and usage limits, not five comprehensive tests.

Illustrative cost worksheet (planning assumptions, not vendor quotes): a £50 initial assessment with 30 minutes of delivery at £40/hour, £2 of infrastructure and £5 administration leaves £23 before acquisition, tax and overhead. At 90 minutes it loses £17 on those assumptions. Tightly limit the first product and measure actual delivery time.

For a UK recurring experiment, model £80/month solely as an internal scenario, not a recommended or approved price. Assume £5 infrastructure/API, £3 AI/report/storage, £3 processing/administration allocation and 15 minutes analyst time at £40/hour (£10): £21 variable cost, £59 contribution before fixed costs, acquisition, tax and churn. At 60 analyst minutes, contribution falls to £29. These are assumed unit costs; replace each with current vendor quotes and pilot measurements. Do not compare this directly with US$100 without an explicit exchange-rate and tax decision.

Track observed cost per check, job failure/retry rate, AI tokens, report cost, analyst minutes, conversion, churn, gross margin and cost per acquired customer. Reconcile payment webhooks server-side, verify signatures and idempotency, and enforce cancellations/entitlements before adding billing. Use test-mode payments until separately approved.

## Delivery sequence

| Release | Effort | Dependencies/cost | Key risk and acceptance gate |
|---|---|---|---|
| Website preview + internal evidence CLI | Small | Existing host; no paid integration | No operational product claims; parser tests and own-domain run recorded |
| Human-led £50 demand experiment | Small | Confirmed identity, enquiry channel, scope, VAT/contracts and capable delivery | Measure actual minutes and margins; no intrusive or comprehensive test promise |
| Reliable approved worker runtime | Medium | Managed worker/queue provider and current quote | Timeouts, no scope escape, explicit failures, no arbitrary customer URLs |
| Internal review interface | Medium | Authorised evidence store and reviewer role | Every externalised finding has traceable source and human approval |
| Customer reporting MVP | Large | Identity, tenant DB, private storage, ownership and written authorisation | Cross-tenant tests, recovery, secure exports and independent security review pass |
| AI adviser + human ticket handover | Medium | Read-only retrieval, model terms, staffing and measured token costs | Grounded citations, injection/tenant tests, consented handover, finite support |
| Billing and usage | Medium | Approved currency/prices, payment provider test mode | Idempotent lifecycle, accurate quotas and cancellation |
| Recurring authorised monitoring | Medium | Reliable worker, permissions, quotas and alert ownership | Expired/revoked authorisation stops jobs; no failure-as-pass; reconcile usage |
| Prospect records/outreach governance | Separate review | Legal advice, verified sender/identity, lawful-source review and suppression process | No mass outreach activation; do not build autonomous third-party vulnerability targeting |

## Pilot and permission decisions

Counsellors’ Staffroom is not included in this prototype's target set. Its company identity and supplier relationships were not reverified; no vulnerability was established. No tests, notifications or sales messages were sent to it. This iteration demonstrates reliability on Cyber Defender's own assets instead of treating a failed pilot request as insecurity.

Do not launch prospect discovery or marketing on a generic assumption that public data permits every use. Obtain current legal review of subscriber category, legal basis, transparency, objections/suppression, retention and cross-border handling. Corporate registration is not sufficient permission for every communication or assessment. No automated lead-harvesting or scanning-to-outreach workflow is implemented here.

## Remaining launch decisions

Approve the marketing preview before production. Confirm business contact and identity, actual assessment scope, competent delivery, support capacity, VAT and service agreements. Select paid vendors only after reviewing current prices/terms and pilot unit costs. TLS socket collection, DKIM selectors, passive-data providers and customer integrations remain explicitly incomplete. No production portal should hold real customer findings before security review and tenant-isolation verification.
