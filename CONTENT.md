# Site content

Approved copy and facts for respeclabs.com. The design reference is **Option D** in the Figma file "RespecLabs – Landing Page".

## Credits strip ("Inventory loadout")
Starfield · Fallout 76 · Battlefield 4 · Killzone 3 · Star Wars Battlefront II · Many more

## Skill sheet ("Your team, respecced")
5-segment RPG meters, half segments allowed; readout shows the fill as N/5.

Class card icons are 16×16 pixel sprites in `assets/classes/`: Class 01 wizard, Class 02 fighter, Class 03 rogue. The player profile CLASS row shows `director.svg`, a sprite of Daniele (swept hair, tortoiseshell glasses, grey beard, dark tee, game controller).

| Stat | Readout | Segments |
|---|---|---|
| Design leadership | 5/5 | 5 |
| Scope & milestones | 3/5 | 3 |
| Team structure & hiring | 3.5/5 | 3.5 |
| Career momentum | 4/5 | 4 |
| Academic advisory | 4.5/5 | 4.5 |

## Player profile
| Field | Value |
|---|---|
| Name | Daniele Nanni |
| Class | Creative & Game Director |
| XP | 25+ years |
| Guilds | Bethesda · EA · Sony · Tencent · Gearbox |
| Languages | EN / IT |

Photo: `assets/img/dan-nanni.jpg` (1200px), with `dan-nanni-600` and `.webp` versions for smaller screens.

## Contact
Contact form (name, email, message) sends directly from the site to hello@respeclabs.com through the `respeclabs-contact` Cloudflare Worker (`worker/contact.js`), sent from website@forms.respeclabs.com via free Cloudflare Email Routing on that subdomain only (iCloud keeps the main domain's mail), with Cloudflare Turnstile spam protection and the sender set as reply-to. The email address is also shown as a plain mailto link. No booking/scheduling links.
LinkedIn: https://www.linkedin.com/in/dnanni/

## Player profile LinkedIn row
PARTY INVITE: "Connect on LinkedIn ↗" in gold with the LinkedIn logo, both linking to https://www.linkedin.com/in/dnanni/

## Footer
Bottom right: "Made with ♥ and a lot of coffee" (pixel heart, #E8392E, same as the Holy Grawlix footer). Easter-egg link to https://holygrawlix.com/: looks like plain text, turns gold on hover.

## Icons
Root `/favicon.ico` (16/32/48) and `/apple-touch-icon.png` (180) exist because Safari (iPad/iPhone) requests them directly. `404.html` keeps missing files returning a real 404 instead of the homepage.
