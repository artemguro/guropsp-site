"""Shared <head>, header and footer for inner pages (services, blog)."""
import html as H

SITE = 'https://guropsp.com'
e = lambda s: H.escape(s, quote=True)

NAV = {
    'ru': dict(services='Услуги', audit='Аудит платежей', routing='Роутинг и каскадинг', blog='Блог', price='Стоимость', rss='Блог GURO PSP (RSS)'),
    'en': dict(services='Services', audit='Payments audit', routing='Routing and cascading', blog='Blog', price='Pricing', rss='GURO PSP blog (RSS)'),
}


def prefix(lang):
    return '/ru/' if lang == 'ru' else '/'


def redirect_js(ru_path):
    return ("try{var L=localStorage.getItem('guro_lang');var ls=(navigator.languages&&navigator.languages.length?"
            "navigator.languages:[navigator.language||'']).join(',').toLowerCase();"
            "if(L==='ru'||(!L&&/(^|,)(ru|uk|be|kk)\\b/.test(ls))){location.replace('" + ru_path + "'+location.search+location.hash);}}catch(e){}")


def nav_links(lang, cur):
    N = NAV[lang]; h = prefix(lang)
    items = [('services', h + '#services', N['services']),
             ('payments-audit', h + 'services/payments-audit/', N['audit']),
             ('routing-cascading', h + 'services/routing-cascading/', N['routing']),
             ('blog', h + 'blog/', N['blog'])]
    return ''.join('<a href="%s"%s>%s</a>' % (u, ' aria-current="page"' if k == cur else '', e(t)) for k, u, t in items)


def chrome_top(lang, D, ver, title, desc, og_title, url, alt_en, alt_ru, ld, redirect, src, cur='', og_type='website', extra_head=''):
    other = 'en' if lang == 'ru' else 'ru'
    home = prefix(lang)
    alt_x = alt_en if alt_en else alt_ru
    hreflang = ''
    if alt_en: hreflang += '<link rel="alternate" hreflang="en" href="%s">\n' % alt_en
    if alt_ru: hreflang += '<link rel="alternate" hreflang="ru" href="%s">\n' % alt_ru
    hreflang += '<link rel="alternate" hreflang="x-default" href="%s">\n' % alt_x
    switch = (alt_ru if lang == 'en' else alt_en) or (SITE + prefix(other))
    rss = '<link rel="alternate" type="application/rss+xml" title="%s" href="%s">\n' % (e(NAV[lang]['rss']), SITE + home + 'blog/feed.xml')
    return f'''<!doctype html>
<html lang="{lang}" data-tg-msg="{e(D['tg_msg'])}" data-tg-ref="{e(D['tg_ref'])}" data-tg-user="GuroArtem" data-tg-bot="GuroPSPbot" data-tg-src="{src}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:title" content="{e(og_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="GURO PSP">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="{D['og_locale']}">
<meta property="og:image" content="{SITE}/og-{lang}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(og_title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}/og-{lang}.jpg">
<meta name="theme-color" content="#070809">
{extra_head}<link rel="canonical" href="{url}">
{hreflang}{rss}<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-96.png" type="image/png" sizes="96x96">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@400;500;600;700&family=Onest:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css?v={ver}">
<script type="application/ld+json">{ld}</script>
<script>
document.documentElement.classList.add('js');
(function(){{try{{var r=new URLSearchParams(location.search).get('ref');if(r){{r=r.replace(/[^A-Za-z0-9_-]/g,'').slice(0,40);var o=localStorage.getItem('guro_ref'),t=+localStorage.getItem('guro_ref_t')||0;if(r&&(!o||Date.now()-t>7776000000)){{localStorage.setItem('guro_ref',r);localStorage.setItem('guro_ref_t',String(Date.now()));}}}}}}catch(e){{}}
{redirect}}})();
</script>
</head>
<body class="page-svc">

<div class="curtain" id="curtain" aria-hidden="true">
  <div class="curtain-in"><span class="curtain-mark"><i></i></span><span class="curtain-word">GURO <b>PSP</b></span><span class="curtain-bar"><i></i></span></div>
</div>
<div class="grain" aria-hidden="true"></div>
<div class="ambient" aria-hidden="true"><i class="b1"></i><i class="b2"></i><i class="b3"></i></div>
<div class="cursor" id="cursor" aria-hidden="true"><div class="cursor-ring"><span class="cursor-label"></span></div><div class="cursor-dot"></div></div>

<header class="nav" id="nav">
  <div class="nav-pill">
    <a href="{home}" class="logo" aria-label="{e(D['logo_label'])}"><span class="logo-mark"><i></i></span>GURO<b>&nbsp;PSP</b></a>
    <nav class="links" id="links" aria-label="{e(D['nav_label'])}">{nav_links(lang, cur)}</nav>
    <div class="nav-r">
      <a href="{switch}" class="lang" data-set="{other}" hreflang="{other}" lang="{other}" aria-label="{e(D['lang_label'])}" data-cursor="{D['lang_text']}">{D['lang_text']}</a>
      <a href="https://t.me/GuroArtem" class="btn btn-sm magnetic" data-tg data-cursor="Telegram" target="_blank" rel="noopener"><span>{e(D['cta_tg'])}</span></a>
      <button class="burger" id="burger" type="button" aria-label="{e(D['menu_open'])}" aria-expanded="false" aria-controls="links" data-open="{e(D['menu_open'])}" data-close="{e(D['menu_close'])}"><i></i><i></i></button>
    </div>
  </div>
</header>

'''


def chrome_bottom(lang, D, ver):
    N = NAV[lang]; h = prefix(lang)
    return f'''
<footer class="foot">
  <div class="wrap foot-in">
    <span>© <span id="yr">2026</span> GURO PSP. {e(D['foot'])}</span>
    <nav class="foot-links" aria-label="{e(N['services'])}"><a href="{h}services/payments-audit/">{e(N['audit'])}</a><a href="{h}services/routing-cascading/">{e(N['routing'])}</a><a href="{h}blog/">{e(N['blog'])}</a><a href="{h}">GuroPSP.com</a></nav>
  </div>
</footer>

<script src="/assets/gsap.min.js?v={ver}" defer></script>
<script src="/assets/ScrollTrigger.min.js?v={ver}" defer></script>
<script src="/assets/site.js?v={ver}" defer></script>
</body>
</html>
'''
