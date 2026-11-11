// Contact form endpoint for respeclabs.com and the Holy Grawlix studio site (Cloudflare Worker "respeclabs-contact").
// Bindings (set in Cloudflare, not in this file):
//   EMAIL            send_email binding, allowed destinations hello@respeclabs.com and hello@holygrawlix.com
//                    (both verified destinations in Cloudflare Email Routing)
// Sent from website@forms.respeclabs.com via free Cloudflare Email Routing. Both inboxes forward to
// the business Gmail, where each site's mail is labelled by its address.
//   TURNSTILE_SECRET secret for the "Respec Labs contact form" Turnstile widget
const FROM = { email: 'website@forms.respeclabs.com', name: 'Respec Labs website' };
const ALLOWED_ORIGINS = [/^https:\/\/(www\.)?respeclabs\.com$/, /^https:\/\/([a-z0-9-]+\.)?respeclabs-site\.pages\.dev$/,
  /^https:\/\/(www\.)?holygrawlix\.com$/, /^https:\/\/([a-z0-9-]+\.)?grawlix-games\.pages\.dev$/];
// Plain-sentence subject naming the site (no bracketed tags, which can look automated to spam filters).
const isGrawlix = (origin) => /holygrawlix|grawlix-games/.test(origin || '');
const siteName = (origin) => (isGrawlix(origin) ? 'Holy Grawlix Games' : 'Respec Labs');
// Each site's enquiries go to its own address.
const toFor = (origin) => (isGrawlix(origin) ? 'hello@holygrawlix.com' : 'hello@respeclabs.com');

function cors(origin) {
  const ok = origin && ALLOWED_ORIGINS.some((re) => re.test(origin));
  return ok ? { 'Access-Control-Allow-Origin': origin, 'Access-Control-Allow-Methods': 'POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type', Vary: 'Origin' } : {};
}
const json = (body, status, headers) => new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json', ...headers } });
const clean = (v, max) => String(v || '').replace(/\r/g, '').trim().slice(0, max);

export default {
  async fetch(req, env) {
    const origin = req.headers.get('Origin');
    const h = cors(origin);
    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: h });
    if (req.method !== 'POST') return json({ ok: false, error: 'Method not allowed' }, 405, h);
    if (!h['Access-Control-Allow-Origin']) return json({ ok: false, error: 'Forbidden' }, 403, h);

    let data;
    try { data = await req.json(); } catch { return json({ ok: false, error: 'Bad request' }, 400, h); }
    if (data.company) return json({ ok: true }, 200, h); // honeypot: bots fill the hidden field

    const name = clean(data.name, 100), email = clean(data.email, 200), message = clean(data.message, 5000);
    if (!name || !message || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json({ ok: false, error: 'Please fill in your name, a valid email, and a message.' }, 400, h);

    const ts = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
      method: 'POST',
      body: new URLSearchParams({ secret: env.TURNSTILE_SECRET, response: String(data.token || ''), remoteip: req.headers.get('CF-Connecting-IP') || '' }),
    }).then((r) => r.json()).catch(() => ({ success: false }));
    if (!ts.success) return json({ ok: false, error: 'Spam check failed. Please try again.' }, 400, h);

    try {
      await env.EMAIL.send({
        to: toFor(origin),
        from: FROM,
        replyTo: { email, name },
        subject: `New message from ${name} via the ${siteName(origin)} website`,
        text: `${message}\n\n---\nFrom: ${name} <${email}>\nSent via the contact form on ${origin}`,
      });
    } catch (e) {
      console.log('send failed', e && (e.code || e.message));
      return json({ ok: false, error: 'Sorry, the message could not be sent.' }, 502, h);
    }
    return json({ ok: true }, 200, h);
  },
};
