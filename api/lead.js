// Vercel Serverless Function — receives consultation-form submissions
// from contact.html and index.html and forwards to info@fasmedicalsummitrcm.com.
//
// Required env var (set in Vercel project settings):
//   RESEND_API_KEY  — get one free at https://resend.com (3,000 emails/mo).
//
// Optional env vars:
//   LEAD_TO_EMAIL    — destination (default: info@fasmedicalsummitrcm.com)
//   LEAD_FROM_EMAIL  — sender (default: 'FAS Lead Form <onboarding@resend.dev>')
//
// Until RESEND_API_KEY is set, leads are still captured in the Vercel function
// log so nothing is lost — they just don't email out yet.

const TO_EMAIL = process.env.LEAD_TO_EMAIL || 'info@fasmedicalsummitrcm.com';
const FROM_EMAIL = process.env.LEAD_FROM_EMAIL || 'FAS Lead Form <onboarding@resend.dev>';

function escapeHtml(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function buildEmailBody(data) {
  const fields = [
    ['Name',              data.name],
    ['Email',             data.email],
    ['Phone',             data.phone],
    ['Practice',          data.practice],
    ['Monthly Collection',data.collection],
    ['No. of Providers',  data.providers],
    ['Specialty',         data.specialty],
    ['EHR / PMS',         data.ehr],
    ['Message',           data.message],
    ['Submitted From',    data._source],
    ['Referrer',          data._referrer],
    ['Timestamp',         new Date().toISOString()],
  ];

  const rows = fields
    .filter(([, v]) => v !== undefined && v !== null && String(v).trim() !== '')
    .map(([k, v]) => `<tr>
        <td style="padding:8px 14px;background:#f8f6f1;border-bottom:1px solid #ece6d8;font-family:monospace;font-size:12px;color:#7a6d4f;width:180px;vertical-align:top;">${escapeHtml(k)}</td>
        <td style="padding:8px 14px;border-bottom:1px solid #ece6d8;font-size:14px;color:#1a1a1a;vertical-align:top;">${escapeHtml(v).replace(/\n/g,'<br>')}</td>
      </tr>`)
    .join('');

  const html = `<!doctype html>
<html><body style="margin:0;padding:32px;background:#fafaf6;font-family:-apple-system,BlinkMacSystemFont,sans-serif;">
  <div style="max-width:640px;margin:0 auto;background:#fff;border-radius:12px;overflow:hidden;border:1px solid #ece6d8;">
    <div style="padding:24px 28px;background:#0A1220;color:#F4EFE6;">
      <div style="font-family:Georgia,serif;font-size:20px;font-weight:500;margin-bottom:4px;">New Consultation Request</div>
      <div style="font-size:13px;color:#C9A961;font-family:monospace;letter-spacing:0.04em;">FAS MEDICAL SUMMIT RCM</div>
    </div>
    <table style="width:100%;border-collapse:collapse;">${rows}</table>
    <div style="padding:18px 28px;background:#f8f6f1;font-size:12px;color:#7a6d4f;border-top:1px solid #ece6d8;">
      Reply directly to this email to respond to ${escapeHtml(data.name || 'the lead')}.
    </div>
  </div>
</body></html>`;

  const text = fields
    .filter(([, v]) => v !== undefined && v !== null && String(v).trim() !== '')
    .map(([k, v]) => `${k}: ${v}`)
    .join('\n');

  return { html, text };
}

export default async function handler(req, res) {
  // CORS / method
  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    return res.status(204).end();
  }
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'method_not_allowed' });
  }

  // Body — Vercel parses JSON automatically when content-type is application/json
  const data = (req.body && typeof req.body === 'object') ? req.body : {};

  // Honeypot — silently accept and discard known bot submissions
  if (data.website_url) {
    return res.status(200).json({ ok: true });
  }

  // Validate
  for (const f of ['name', 'email', 'phone']) {
    if (!data[f] || !String(data[f]).trim()) {
      return res.status(400).json({ error: `${f}_required` });
    }
  }
  if (!/.+@.+\..+/.test(String(data.email))) {
    return res.status(400).json({ error: 'invalid_email' });
  }

  // Always log so leads are never lost, even if email is misconfigured
  console.log('[LEAD]', JSON.stringify({
    name: data.name,
    email: data.email,
    phone: data.phone,
    practice: data.practice,
    collection: data.collection,
    providers: data.providers,
    specialty: data.specialty,
    ehr: data.ehr,
    message: data.message,
    source: data._source,
    referrer: data._referrer,
    ts: new Date().toISOString(),
  }));

  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    // No email service configured yet. Still report success — lead is in
    // the Vercel function log and can be retrieved.
    return res.status(200).json({ ok: true, mode: 'logged_only' });
  }

  const { html, text } = buildEmailBody(data);
  const subject = `New lead: ${data.name}${data.practice ? ` — ${data.practice}` : ''}`;

  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: FROM_EMAIL,
        to: [TO_EMAIL],
        reply_to: data.email,
        subject,
        html,
        text,
      }),
    });

    if (!r.ok) {
      const errBody = await r.text();
      console.error('[RESEND_FAIL]', r.status, errBody);
      // Lead is logged. Tell client it succeeded so they don't retry.
      return res.status(200).json({ ok: true, mode: 'logged_only', warning: 'email_send_failed' });
    }

    return res.status(200).json({ ok: true, mode: 'emailed' });
  } catch (e) {
    console.error('[LEAD_EMAIL_ERROR]', e?.message || e);
    return res.status(200).json({ ok: true, mode: 'logged_only', warning: 'email_error' });
  }
}
