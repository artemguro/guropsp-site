# GuroPSP.com — how to work with this repo

GURO PSP is an iGaming payments consulting business (cashier/PSP audits, smart routing and cascading,
dashboards and alerting, PSP sourcing). Owner: Artem. The site is bilingual: EN at `/`, RU at `/ru/`.

## Publishing = push to `main`
The hosting pulls this repo automatically every 10 minutes (`deploy/pull.php`, cron on the server):
when `site/VERSION` changes, files from `site/` are copied to the web root. It never deletes files.
New sitemap URLs are pinged to Bing/Yandex via IndexNow by the server script. So: edit `src/`,
run `python3 build.py`, commit both `src/` and `site/`, push to `main`. That's the whole deploy.

## Adding a blog article
1. Add a dict to `src/blog_more.py` (same structure as `CHECKLIST` / `PSP`), with `ru` and `en` versions,
   and append it to `ARTICLES` at the bottom of `src/blog_content.py`.
   - `slug`: English, lowercase, hyphens. `service`: `payments-audit` or `routing-cascading`.
   - `date` / `updated`: today (ISO). `read`: honest reading time.
   - Block types: `('h2', id, text)`, `('p', text)`, `('ul'|'ol', [items])`, `('table', cols, rows)`, `('cta', service_slug)`.
     Only `**bold**` inline markup. Put one `cta` block roughly in the middle.
   - 2 short FAQ items. `seo_title` ends with ` | GURO PSP`, ≤ ~70 chars before it. `desc` 140–160 chars.
2. `python3 build.py` — must print `built`; EN pages must contain no Cyrillic except the "Русская версия" switch label.
3. Optionally render-check with Playwright (`python3 -m http.server` in `site/`).
4. Commit and push.

## Content rules (important — articles are published without manual review)
- Practical, operator-side expertise. No invented statistics, case numbers, client names or quotes.
- Anything that changes over time (regulation, a bank's or scheme's policy, fees, limits, which methods
  a market uses) must be verified with a web search in the same session, and phrased with appropriate
  hedging. If you can't verify it, leave it out.
- Never advise circumventing card scheme rules, issuer gambling blocks, MCC rules, KYC/AML or licensing.
  Responsible framing for declines like insufficient funds (clear message, player's choice).
- We don't sell PSPs/orchestrators; the choice stays with the client. Keep tone factual, not salesy.
- RU and EN versions must say the same thing; RU is natural Russian, not a word-for-word translation.
- Quality over volume: 1–2 articles per week max.

## Content plan (next topics, in order — skip ones already in `ARTICLES`)
1. Cascading after 3DS: when it helps and when it hurts (routing-cascading)
2. Routing by BIN and issuing bank (routing-cascading)
3. Payment orchestrator vs in-house gateway: how to choose (payments-audit)
4. Payment metrics: approval rate, player conversion, cost per successful deposit — how to calculate (payments-audit)
5. Smart alerting for payments: what to alert on and how to route alerts (payments-audit)
6. Casino payments in Canada: cards, Interac, risks — needs fresh web research (payments-audit)
7. Casino payments in Australia and New Zealand — needs fresh web research (payments-audit)
8. Netherlands, UK, France: payments in difficult markets — needs fresh web research (payments-audit)
9. EMI and bank accounts for iGaming businesses — needs fresh web research (payments-audit)

## Do not touch
- `/tg/` on the server (Telegram bot webhook) and anything outside `site/`.
- `site/yandex_8a841c9510d8c0d4.html` and `site/5f3c9e2a7b1d4c8e9a6f0b2d3c4e5f61.txt` (search engine verification / IndexNow key).
