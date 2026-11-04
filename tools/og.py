"""Generates a 1200x630 social preview (og:image) for every blog article that doesn't have one yet.
Output: src/og/<slug>-<lang>.jpg. Uses Playwright + the fonts vendored in src/fonts. Safe to run repeatedly.
Usage: python3 tools/og.py [--force]"""
import base64, html, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT + '/src')
OUT = ROOT + '/src/og'
FONTS = ROOT + '/src/fonts'


def _face(fam, name, w, sub):
    p = f'{FONTS}/{name}-{sub}-{w}-normal.woff2'
    if not os.path.exists(p):
        return ''
    rng = {'latin': 'U+0000-00FF,U+2000-206F,U+20AC,U+2122,U+2190-21FF', 'latin-ext': 'U+0100-024F', 'cyrillic': 'U+0400-045F,U+0490-0491', 'cyrillic-ext': 'U+0460-052F'}[sub]
    return f"@font-face{{font-family:{fam};src:url(data:font/woff2;base64,{base64.b64encode(open(p, 'rb').read()).decode()}) format('woff2');font-weight:{w};unicode-range:{rng}}}"


def _fonts():
    out = ''
    for fam, name, ws in [('U', 'unbounded', (600, 700)), ('O', 'onest', (400, 500)), ('M', 'jetbrains-mono', (500,))]:
        for w in ws:
            for sub in ('latin', 'latin-ext', 'cyrillic', 'cyrillic-ext'):
                out += _face(fam, name, w, sub)
    return out


def page(title, desc, tag, lang, fonts):
    e = lambda s: html.escape(s, quote=True)
    size = 64 if len(title) <= 42 else (54 if len(title) <= 64 else 46)
    site = 'guropsp.com/ru/blog' if lang == 'ru' else 'guropsp.com/blog'
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{fonts}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1200px;height:630px;overflow:hidden;background:#070809;color:#eef1f3;font-family:O}}
.wrap{{position:absolute;inset:0;padding:64px 72px;display:flex;flex-direction:column}}
.glow{{position:absolute;width:760px;height:760px;right:-260px;top:-300px;border-radius:50%;background:radial-gradient(circle,rgba(217,255,63,.2),transparent 62%)}}
.glow2{{position:absolute;width:700px;height:700px;left:-320px;bottom:-380px;border-radius:50%;background:radial-gradient(circle,rgba(124,240,196,.12),transparent 62%)}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);background-size:48px 48px;mask-image:radial-gradient(circle at 60% 40%,#000 20%,transparent 75%)}}
.top{{display:flex;align-items:center;justify-content:space-between}}
.logo{{display:flex;align-items:center;font:700 30px U;letter-spacing:.03em}}
.logo b{{color:#d9ff3f;margin-left:.3em}}
.mark{{width:42px;height:42px;border-radius:50%;border:7px solid #d9ff3f;position:relative;margin-right:16px;box-shadow:0 0 26px rgba(217,255,63,.45)}}
.mark i{{position:absolute;inset:0;margin:auto;width:10px;height:10px;border-radius:50%;background:#d9ff3f}}
.tag{{font:500 20px M;color:#070809;background:#d9ff3f;border-radius:999px;padding:9px 18px;letter-spacing:.04em;text-transform:uppercase}}
h1{{font:700 {size}px/1.08 U;letter-spacing:-.03em;margin-top:auto;max-width:1000px}}
p{{font:400 26px/1.4 O;color:#a8b1bd;margin-top:22px;max-width:960px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.site{{margin-top:34px;font:500 22px M;color:#7cf0c4}}
</style></head><body><div class="grid"></div><div class="glow"></div><div class="glow2"></div>
<div class="wrap"><div class="top"><div class="logo"><span class="mark"><i></i></span>GURO<b>PSP</b></div><span class="tag">{e(tag)}</span></div>
<h1>{e(title)}</h1><p>{e(desc)}</p><div class="site">{site}</div></div></body></html>'''


def generate(force=False):
    """Returns the number of images written. Raises ImportError if Playwright is missing."""
    from playwright.sync_api import sync_playwright
    from blog_articles import ARTICLES
    os.makedirs(OUT, exist_ok=True)
    todo = [(a, l) for a in ARTICLES for l in ('en', 'ru') if force or not os.path.exists(f"{OUT}/{a['slug']}-{l}.jpg")]
    if not todo:
        return 0
    fonts = _fonts()
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1200, 'height': 630})
        for a, l in todo:
            C = a[l]
            pg.set_content(page(C['title'], C['desc'], C.get('tag', 'GURO PSP'), l, fonts))
            pg.evaluate('document.fonts.ready')
            pg.wait_for_timeout(150)
            pg.screenshot(path=f"{OUT}/{a['slug']}-{l}.jpg", type='jpeg', quality=88)
        b.close()
    return len(todo)


if __name__ == '__main__':
    print('og images written:', generate('--force' in sys.argv))
