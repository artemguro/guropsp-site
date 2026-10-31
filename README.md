# GuroPSP.com

Static site for GURO PSP (iGaming payments consulting).

- `src/` — templates and content (`blog_content.py`, `blog_more.py`, `services_content.py`)
- `build.py` — builds the site into `site/`
- `site/` — built output; the hosting pulls this folder automatically (`deploy/pull.php`, cron every 10 min) when `site/VERSION` changes.
