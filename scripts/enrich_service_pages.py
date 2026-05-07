#!/usr/bin/env python3
"""Inject 'Our Approach' + 'Testimonials' sections into each service/specialty page.
Idempotent: if already injected, page is skipped.
"""

import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ─── Per-page Approach content ──────────────────────────────────────────────
# heading_lead, heading_emph, then 4 steps (label, description)
APPROACH = {
    'services/ar-follow-up.html': (
        'Working A/R is a', 'discipline, not a tactic.',
        [
            ('Review aging accounts',
             'We pull your aging report, sort claims by dollar value and timely-filing risk, and flag the buckets that need attention this week.'),
            ('Prioritize by impact',
             'Stalled claims that need a payer call get one. Rejections that need a correction get fixed. Patient balances move into a structured statement cycle.'),
            ('Take action and follow up',
             'We work each account until it moves — not one attempt and done. Every payer interaction is documented in your billing system.'),
            ('Track patterns and adjust',
             'Recurring denials and slow payers become workflow improvements. Fewer balances land in the 90+ bucket in the first place.'),
        ]),
    'services/charge-capture-coding.html': (
        'Coding accuracy starts with', 'how charges are captured.',
        [
            ('Capture every billable service',
             'Coders work directly from operative notes, encounter records, and ASC schedules. Nothing reimbursable gets missed because documentation was thin.'),
            ('Code to the highest defensible level',
             'CPT, ICD-10, HCPCS, and modifiers selected to match what was actually performed and documented — not under-coded, not over-coded.'),
            ('Audit before submission',
             'Every claim runs through coding edits, payer-specific rules, and bundling logic before it leaves. Clean first time, every time.'),
            ('Feed coding insight back upstream',
             'Documentation patterns that cause downcoding or denials get flagged so providers can adjust how they document going forward.'),
        ]),
    'services/claims-submission.html': (
        'Build clean. Submit fast.', 'Track until paid.',
        [
            ('Build a clean claim',
             'We assemble each claim from coding and documentation, then scrub against payer-specific rules — codes, modifiers, demographics — before it goes out.'),
            ('Submit through the right channel',
             'Electronic when the payer supports it. Paper only when required. Either way: complete claim, nothing missing.'),
            ('Track status in real time',
             'Once submitted, claims are monitored through the clearinghouse and payer portals. Stuck claims surface within days, not weeks.'),
            ('Fix issues before they turn into write-offs',
             'Rejections and requests for additional information get worked the same day they appear. Nothing sits in a queue waiting to age.'),
        ]),
    'services/credentialing.html': (
        'Credentialing is the', 'foundation of getting paid.',
        [
            ('Gather and verify provider data',
             'We pull NPI, DEA, license, board, malpractice, education, and work history into a single complete file. Errors caught now save months later.'),
            ('Submit applications and enrollments',
             'Payer-by-payer enrollment, CAQH attestation, hospital privileging, and Medicare/Medicaid revalidations — handled in parallel rather than one at a time.'),
            ('Track approvals and follow up',
             'Every application is tracked weekly until approved. Payer requests for additional information come back to us, not to your front desk.'),
            ('Maintain credentials before they lapse',
             'License renewals, CAQH re-attestations, and payer revalidations tracked on an ongoing calendar so a lapsed credential never causes a gap in billing.'),
        ]),
    'services/denial-management.html': (
        'Resolve denials.', 'Prevent the next ones.',
        [
            ('Review the denial reason',
             'Every denial is read against the actual payer policy and documentation — not sorted by remark code into a queue. Root cause first, response second.'),
            ('Correct and resubmit fast',
             'Coding fixes, missing-information responses, and demographic corrections turn around in days. Clean resubmission, not a duplicate of the same claim.'),
            ('File formal appeals when warranted',
             'When the denial is wrong, we file the appeal with cited policy language and supporting documentation. We track every appeal until a determination comes back.'),
            ('Feed root causes back into intake',
             'A pattern of authorization denials becomes a pre-cert workflow change. A pattern of medical-necessity denials becomes provider documentation feedback.'),
        ]),
    'services/patient-billing.html': (
        'Patient balances handled', 'with respect and consistency.',
        [
            ('Verify what the patient owes',
             'After insurance settles, we reconcile patient responsibility against the EOB so the statement matches what the payer actually allowed and applied.'),
            ('Send a clear, readable statement',
             'No cryptic abbreviations, no surprise charges. The patient knows what was billed, what insurance covered, and what they owe — in plain language.'),
            ('Manage payment plans and questions',
             'Patients who call get reached. Payment plans are set up, statements are explained, and disputes are routed back into the billing workflow.'),
            ('Follow up consistently, not aggressively',
             'A defined cadence — first statement, second, then phone outreach — replaces sporadic chasing. Better collection rates, fewer angry phone calls.'),
        ]),
    'services/patient-onboarding.html': (
        'Front-end accuracy prevents', 'back-end denials.',
        [
            ('Verify eligibility in real time',
             'EDI 270/271 eligibility checks before service confirm coverage is active and the patient hasn\'t maxed out benefits — not after the claim denies.'),
            ('Confirm benefits and authorization',
             'Co-pays, deductibles, and out-of-pocket are verified. Procedures requiring prior authorization are flagged and authorized before the patient walks in.'),
            ('Capture clean demographics',
             'Names spelled per insurance card. Dates of birth verified. Subscriber relationship correct. Demographic denials caused by typos disappear.'),
            ('Hand off a fully-prepared encounter',
             'When the encounter starts, the financial side is already settled. Your front desk focuses on the patient, not on chasing missing data.'),
        ]),
    'services/payment-posting.html': (
        'Posting accuracy is the', 'foundation of clean A/R.',
        [
            ('Receive ERAs and paper EOBs',
             'Electronic remits posted automatically with payer-specific rules. Paper EOBs and patient payments handled by trained posters — not bulk-imported and ignored.'),
            ('Match payments to the right claim',
             'Every line item reconciled. Bundled, denied, and partial payments routed to the right work queue. Nothing posted to the wrong account.'),
            ('Reconcile against deposits',
             'Daily reconciliation against bank deposits ensures every dollar deposited is also posted, and every posted dollar matches a deposit. Variances surface immediately.'),
            ('Flag underpayments and unusual patterns',
             'Payments below contracted rates flagged for appeal. Recurring underpayment patterns escalated so contract issues get caught and addressed.'),
        ]),
    'services/reporting-analytics.html': (
        'Reporting that shows what is', 'happening — and why.',
        [
            ('Connect to your billing data',
             'We integrate with your practice management or EHR data so reports run on what\'s actually in your system — not on what someone exported last month.'),
            ('Build the reports that matter',
             'A/R aging, denial trends, payer mix, days in A/R, collection rates, write-off analysis — the views you actually need to run the practice.'),
            ('Surface anomalies early',
             'Sudden spikes in denials, slow-paying payers, or charge lag get flagged in the dashboard before they become A/R problems.'),
            ('Review with you on a cadence',
             'Monthly reviews with our analysts walk through the numbers, what changed, and what\'s recommended — not a PDF emailed and forgotten.'),
        ]),

    # ─── SPECIALTIES ─────────────────────────────────────────────────────
    'specialties/ambulatory-surgery.html': (
        'ASC billing is its own discipline —', 'we do nothing else.',
        [
            ('Pre-certify every case',
             'Authorizations and pre-certs handled before the day of surgery. Cases that walk through the door without coverage in place get flagged, not billed.'),
            ('Capture charges from the OR record',
             'Coders work from operative notes, anesthesia records, and supply logs. Implantable devices, drug waste, and observation hours all captured cleanly.'),
            ('Apply ASC-specific coding rules',
             'CPT, modifiers, and HCPCS aligned with the ASC payment system. Bundled procedures handled correctly. Multi-procedure discounts applied where they apply — not where they don\'t.'),
            ('Work A/R until every case is closed',
             'Surgical A/R has high dollar values per claim. Every case followed until paid — no five-figure claims aging out.'),
        ]),
    'specialties/anesthesiology.html': (
        'Anesthesia billing is', 'time, modifiers, and precision.',
        [
            ('Capture the anesthesia record cleanly',
             'Start time, stop time, providers, modifiers, ASA physical status — all coded from the actual anesthesia record, not estimated from the OR schedule.'),
            ('Calculate time units correctly',
             'Time-based unit calculation per payer rules. CRNA and supervising-physician modifiers applied correctly. No revenue lost on miscalculated units.'),
            ('Submit with payer-specific edits applied',
             'Every payer has its own anesthesia rules — concurrent care, medical direction ratios, monitoring services. We handle those rules, not your provider.'),
            ('Appeal modifier-driven denials',
             'Modifier-related denials are common in anesthesia and almost always recoverable. We file the appeals; you keep the revenue.'),
        ]),
    'specialties/cardiology.html': (
        'Cardiology billing is', 'high-volume, high-complexity.',
        [
            ('Capture every procedure cleanly',
             'Cath lab, EP, echo, stress testing, device interrogation — all coded from the procedure note with the correct CPT, modifiers, and supply codes.'),
            ('Apply NCCI edits and bundling rules',
             'Cardiology has complex bundling. We apply the edits before submission so unbundled denials don\'t drive avoidable rework.'),
            ('Manage device and procedural authorizations',
             'Device implants, ablations, and high-cost procedures pre-authorized before the case. No five-figure denials because the auth wasn\'t in place.'),
            ('Track payer-specific cardiology policies',
             'Every payer has its own coverage policies for cardiology procedures. We keep current on them so claims clear the first time.'),
        ]),
    'specialties/emergency-medicine.html': (
        'Emergency medicine billing —', 'fast charges, complex coding.',
        [
            ('Capture charges in near-real-time',
             'Encounters coded within 24-48 hours, not weeks. Late charges hurt cash flow and miss timely-filing windows.'),
            ('Code E/M levels accurately',
             'High-acuity ED visits coded to the level the documentation supports. Critical care time captured separately. Procedures captured alongside E/M.'),
            ('Pursue IDR for surprise billing disputes',
             'Out-of-network ED claims under the No Surprises Act handled through the IDR process. We file and track every eligible dispute.'),
            ('Communicate with patients clearly',
             'ED patients receive bills with clear explanation of insurance coverage, balance billing protections, and what they owe. Fewer disputes, better collection.'),
        ]),
    'specialties/family-practice.html': (
        'Family practice billing —', 'volume meets nuance.',
        [
            ('Capture preventive and chronic-care codes',
             'Annual wellness visits, preventive screenings, and chronic-care management coded to capture the full range of work — not just the office visit.'),
            ('Support E/M level decisions with documentation',
             'E/M leveling under the 2021 guidelines requires documentation of medical decision-making or time. We help providers code to the level the work supports.'),
            ('Bill chronic-care management correctly',
             'CCM and TCM codes have specific time and documentation requirements. We make sure they\'re met before claims go out.'),
            ('Manage patient billing without alienating patients',
             'Family practices live and die on patient relationships. Patient billing handled with the same care your providers extend in the exam room.'),
        ]),
    'specialties/pain-management.html': (
        'Pain management billing —', 'authorization and frequency rules.',
        [
            ('Pre-authorize every injection and procedure',
             'Most pain procedures require prior authorization. We secure auth before the patient is on the table — not as a denial after the fact.'),
            ('Code injections accurately',
             'CPT codes, modifiers, and units selected per the procedure performed and the spinal level treated. No bundled injections billed as separate procedures.'),
            ('Handle frequency edits and step therapy',
             'Pain management has aggressive frequency limits and step-therapy requirements. We track them per payer so claims clear without medical-necessity denials.'),
            ('Track payer policy changes',
             'Coverage policies for spinal injections, ablations, and stimulators change frequently. We monitor those changes so your billing doesn\'t fall out of compliance.'),
        ]),
}

# ─── Shared testimonials block ──────────────────────────────────────────────
TESTIMONIALS_HTML = '''
<section class="content-section alt">
  <div style="max-width: 1200px; margin: 0 auto; text-align: center;">
    <span class="eyebrow reveal" style="justify-content: center;">Testimonials</span>
    <h2 class="reveal" style="margin-top: 24px;">Trusted by surgical<br><span class="em" style="color: var(--gold); font-style: italic;">specialty practices.</span></h2>
    <p class="reveal" style="max-width: 720px; margin: 24px auto 0; color: var(--ink-secondary); font-size: 17px; line-height: 1.6;">Hundreds of healthcare providers trust FAS Medical Summit for transparent, efficient revenue cycle management.</p>
  </div>
  <div class="testimonial-cards">
    <figure class="testimonial-card reveal">
      <div class="testimonial-quote-mark">&ldquo;</div>
      <blockquote class="testimonial-quote">Working with FAS Medical Summit has been one of the most valuable decisions for my practice. Their team brings a rare combination of precision, transparency, and genuine care to every aspect of the billing process. From claim submissions to payer follow-ups, they handle each step with efficiency and integrity.</blockquote>
      <figcaption class="testimonial-author">
        <div class="testimonial-name">Dr. Adeel Haq, MD</div>
        <div class="testimonial-role">Surgical Centers in Frisco &amp; McKinney</div>
      </figcaption>
    </figure>
    <figure class="testimonial-card reveal">
      <div class="testimonial-quote-mark">&ldquo;</div>
      <blockquote class="testimonial-quote">Our claims are processed accurately and efficiently. Denials are minimized, and reimbursements are consistently timely. They&rsquo;ve helped us streamline our revenue cycle while maintaining full transparency and compliance. Their communication is clear and their follow-through is dependable.</blockquote>
      <figcaption class="testimonial-author">
        <div class="testimonial-name">Dr. Jessen Mukalel, MD</div>
        <div class="testimonial-role">Multispecialty Surgical Center</div>
      </figcaption>
    </figure>
    <figure class="testimonial-card reveal">
      <div class="testimonial-quote-mark">&ldquo;</div>
      <blockquote class="testimonial-quote">As a hospitalist managing complex inpatient care across multiple facilities, having a reliable billing partner is essential &mdash; and FAS Medical Summit has exceeded every expectation. Their team understands the unique demands of hospital-based medicine and consistently delivers accurate, timely billing with minimal disruption to clinical flow.</blockquote>
      <figcaption class="testimonial-author">
        <div class="testimonial-name">Dr. Anil Desai, MD</div>
        <div class="testimonial-role">Multispecialty Surgical Center</div>
      </figcaption>
    </figure>
  </div>
</section>
'''

# ─── New CSS to inject ──────────────────────────────────────────────────────
NEW_CSS = '''
/* Approach steps & testimonials (added) */
.approach-steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; max-width: 1200px; margin: 60px auto 0; }
.approach-step { padding: 32px 24px; background: var(--bg-elevated); border: 1px solid var(--line); border-radius: var(--radius-md); transition: all 0.4s var(--ease-out); position: relative; }
.approach-step:hover { border-color: var(--gold); transform: translateY(-4px); }
.approach-step-num { font-family: var(--mono); font-size: 11px; color: var(--gold); letter-spacing: 0.16em; margin-bottom: 16px; }
.approach-step h3 { font-size: 19px; font-weight: 500; margin-bottom: 12px; letter-spacing: -0.015em; font-family: var(--serif); }
.approach-step p { font-size: 14px; line-height: 1.65; color: var(--ink-secondary); }

.testimonial-cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; max-width: 1200px; margin: 60px auto 0; }
.testimonial-card { padding: 36px 30px; background: var(--bg-elevated); border: 1px solid var(--line); border-radius: var(--radius-md); position: relative; transition: all 0.4s var(--ease-out); }
.testimonial-card:hover { border-color: var(--gold); transform: translateY(-4px); }
.testimonial-quote-mark { position: absolute; top: 12px; left: 22px; font-family: var(--serif); font-size: 60px; color: var(--gold); opacity: 0.4; line-height: 1; }
.testimonial-quote { position: relative; font-size: 15px; line-height: 1.7; color: var(--ink-secondary); margin: 24px 0 28px; font-style: italic; font-family: var(--serif); font-weight: 400; }
.testimonial-author { border-top: 1px solid var(--line); padding-top: 18px; }
.testimonial-name { font-family: var(--serif); font-size: 17px; font-weight: 500; color: var(--ink-primary); margin-bottom: 4px; }
.testimonial-role { font-family: var(--mono); font-size: 11px; color: var(--ink-tertiary); letter-spacing: 0.08em; }

@media (max-width: 980px) {
  .approach-steps { grid-template-columns: repeat(2, 1fr); }
  .testimonial-cards { grid-template-columns: 1fr; }
}
@media (max-width: 600px) {
  .approach-steps { grid-template-columns: 1fr; }
}

'''


def build_approach_html(rel_path):
    """Generate the approach section HTML for a given page."""
    if rel_path not in APPROACH:
        return None
    lead, emph, steps = APPROACH[rel_path]
    cards = []
    for i, (label, desc) in enumerate(steps, 1):
        cards.append(f'''    <div class="approach-step reveal">
      <div class="approach-step-num">STEP {i:02d}</div>
      <h3>{label}</h3>
      <p>{desc}</p>
    </div>''')
    cards_html = '\n'.join(cards)
    return f'''
<section class="content-section">
  <div style="max-width: 1200px; margin: 0 auto; text-align: center;">
    <span class="eyebrow reveal" style="justify-content: center;">Our Approach</span>
    <h2 class="reveal" style="margin-top: 24px;">{lead}<br><span class="em" style="color: var(--gold); font-style: italic;">{emph}</span></h2>
  </div>
  <div class="approach-steps">
{cards_html}
  </div>
</section>
'''


SENTINEL = '<!-- enrichment-v1: approach + testimonials -->'

def enrich_one(rel_path):
    full = os.path.join(ROOT, rel_path)
    with open(full) as f:
        c = f.read()
    if SENTINEL in c:
        return f'SKIP (already enriched): {rel_path}'

    # 1. inject CSS just before the .related-section rule
    css_anchor = '.related-section { padding: 100px 32px;'
    if css_anchor not in c:
        return f'FAIL (no CSS anchor): {rel_path}'
    c = c.replace(css_anchor, NEW_CSS + css_anchor, 1)

    # 2. inject HTML just before <section class="related-section">
    approach_html = build_approach_html(rel_path)
    if approach_html is None:
        return f'FAIL (no approach content for): {rel_path}'

    html_anchor = '<section class="related-section">'
    if html_anchor not in c:
        return f'FAIL (no HTML anchor): {rel_path}'
    injection = SENTINEL + '\n' + approach_html + TESTIMONIALS_HTML + '\n'
    c = c.replace(html_anchor, injection + html_anchor, 1)

    with open(full, 'w') as f:
        f.write(c)
    return f'OK: {rel_path}'


if __name__ == '__main__':
    targets = list(APPROACH.keys())
    for t in targets:
        print(enrich_one(t))
