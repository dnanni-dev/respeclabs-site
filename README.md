# respeclabs-site

Source for [respeclabs.com](https://respeclabs.com), hosted on Cloudflare.

## Brand assets

`assets/logo/` holds the official Respec Labs logo package:

- `with-slogan/` and `no-slogan/`, each with `svg/` (preferred for the web), `png/` and `pdf/`
- variants: `color-logo-no-background` (white text, blue bars, for dark backgrounds), `white-logo-no-background`, `black-logo-no-background` (for light backgrounds), `color-logo-with-background`
- `symbol/` is the bar mark on its own (`symbol.svg`, in the logo steel blue #4A86AB)

The bar mark is five bars in a "rising build": filled to 20, 45, 30, 75 and 100% from left to right, so it reads as progress. The empty part of each bar is the same color at 32% opacity (no cross-hatching), with a small gap above each fill. Every logo file, the favicons and the email signatures use this mark.
- `variants/respeclabs-comic-black-yellow.svg` is a black-and-yellow version (logo on a black plate) made to match the Holy Grawlix studio site; `respeclabs-comic-yellow.svg` is the same in yellow only, for dark backgrounds

`assets/email/` holds the personal email signature (600x150, plus `@2x`).

`assets/favicons/` holds the browser, iPhone and Android icons.

## SEO

- `index.html` head: keyword title and description, Open Graph/Twitter tags with `assets/social/og-image.png` (1200x630), and JSON-LD for Respec Labs (ProfessionalService with its four services), Daniele Nanni (Person), the website and the page. No address or city, on purpose.
- `robots.txt` allows every crawler, including AI answer engines, and points to `sitemap.xml`. Update `<lastmod>` in `sitemap.xml` when the page content changes.
- `llms.txt` is a plain-text summary for AI search tools.
- `signatures.html` and `404.html` are `noindex` and left out of the sitemap.

## Booking links

`intro.html` and `coaching.html` serve `respeclabs.com/intro` and `respeclabs.com/coaching`. Each page carries its own link-preview card (title, description, and `assets/social/og-intro.png` / `og-coaching.png`) and then sends visitors straight on to the hidden Cal.com booking link. To change where a link goes, edit the URL in that page's `meta refresh`, `location.replace` and fallback link. They are not linked from the site or listed in the sitemap; they're for sharing with people who reach out.
