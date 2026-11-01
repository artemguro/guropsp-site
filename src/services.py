"""Renders service pages (/services/<slug>/ and /ru/services/<slug>/) in the homepage design."""
import json, html as H
from services_content import PAGES, UI
from layout import chrome_top, chrome_bottom

SITE = 'https://guropsp.com'
e = lambda s: H.escape(s, quote=True)


def prefix(lang):
    return '/ru/' if lang == 'ru' else '/'


def page_url(p, lang):
    return SITE + prefix(lang) + 'services/' + p['slug'] + '/'


def redirect_js(p):
    target = '/ru/services/' + p['slug'] + '/'
    return ("try{var L=localStorage.getItem('guro_lang');var ls=(navigator.languages&&navigator.languages.length?"
            "navigator.languages:[navigator.language||'']).join(',').toLowerCase();"
            "if(L==='ru'||(!L&&/(^|,)(ru|uk|be|kk)\\b/.test(ls))){location.replace('" + target + "'+location.search+location.hash);}}catch(e){}")


def jsonld(p, lang, D, C):
    url = page_url(p, lang); home = SITE + prefix(lang); org = SITE + '/#org'
    g = [
        {'@type': 'Organization', '@id': org, 'name': 'GURO PSP', 'alternateName': 'GuroPSP', 'url': SITE + '/',
         'logo': {'@type': 'ImageObject', 'url': SITE + '/icon-512.png', 'width': 512, 'height': 512},
         'sameAs': ['https://t.me/GuroPSPbot']},
        {'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': C['title'], 'description': C['desc'], 'inLanguage': lang,
         'isPartOf': {'@id': SITE + '/#website'}, 'about': {'@id': url + '#service'}, 'breadcrumb': {'@id': url + '#breadcrumb'}},
        {'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'GURO PSP', 'item': home},
            {'@type': 'ListItem', 'position': 2, 'name': C['crumb'], 'item': url}]},
        {'@type': 'Service', '@id': url + '#service', 'name': C['svc_name'], 'serviceType': C['svc_name'], 'description': C['desc'],
         'provider': {'@id': org}, 'url': url,
         'areaServed': [{'@type': 'Place', 'name': n} for n in ['European Union', 'United Kingdom', 'Canada', 'Australia', 'New Zealand']],
         'offers': [{'@type': 'Offer', 'name': D['pb1l'], 'priceCurrency': 'EUR', 'priceSpecification': {'@type': 'PriceSpecification', 'minPrice': 600, 'priceCurrency': 'EUR'}},
                    {'@type': 'Offer', 'name': D['pb2l'], 'priceCurrency': 'EUR', 'priceSpecification': {'@type': 'PriceSpecification', 'minPrice': 3000, 'maxPrice': 4000, 'priceCurrency': 'EUR'}}]},
        {'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in C['faq']]},
    ]
    return json.dumps({'@context': 'https://schema.org', '@graph': g}, ensure_ascii=False).replace('</', '<\\/')


def diagram(dg):
    # small animated SVG: deposit -> router -> PSP A (declined) -> cascade -> PSP B (approved)
    return f'''<svg class="flow-svg" viewBox="0 0 420 250" role="img" aria-label="{e(dg['dep'])} → {e(dg['router'])} → {e(dg['a'])} ({e(dg['decl'])}) → {e(dg['casc'])} → {e(dg['b'])} ({e(dg['ok'])})">
  <path class="fw" d="M92 125 H160"/>
  <path class="fw" d="M240 112 C280 112 280 60 314 60"/>
  <path class="fw" d="M240 138 C280 138 280 190 314 190"/>
  <path class="fw fw-c" d="M360 82 V168"/>
  <path class="fp fp-1" d="M92 125 H160"/>
  <path class="fp fp-2" d="M240 112 C280 112 280 60 314 60"/>
  <path class="fp fp-3 fp-c" d="M360 82 V168"/>
  <rect class="fn" x="12" y="103" width="80" height="44" rx="12"/><text x="52" y="130">{e(dg['dep'])}</text>
  <rect class="fn fn-r" x="160" y="99" width="80" height="52" rx="14"/><text x="200" y="130">{e(dg['router'])}</text>
  <rect class="fn fn-bad" x="314" y="38" width="92" height="44" rx="12"/><text x="360" y="65">{e(dg['a'])}</text>
  <rect class="fn fn-ok" x="314" y="168" width="92" height="44" rx="12"/><text x="360" y="195">{e(dg['b'])}</text>
  <text class="ft ft-bad" x="360" y="26">{e(dg['decl'])}</text>
  <text class="ft ft-c" x="372" y="129" text-anchor="start">{e(dg['casc'])}</text>
  <text class="ft ft-ok" x="360" y="232">✓ {e(dg['ok'])}</text>
</svg>'''


def render(p, lang, D, ver):
    C = p[lang]; U = UI[lang]; other_lang = 'en' if lang == 'ru' else 'ru'
    url = page_url(p, lang); home = prefix(lang)
    alt_en, alt_ru = page_url(p, 'en'), page_url(p, 'ru')
    others = [q for q in PAGES if q is not p]
    ld = jsonld(p, lang, D, C)
    redirect = redirect_js(p) if lang == 'en' else ''

    # hero card
    if 'dg' in C:
        card_body = diagram(C['dg'])
    else:
        card_body = '<ul class="get">' + ''.join(f'<li><i aria-hidden="true"></i>{e(x)}</li>' for x in C['card']) + '</ul>'

    tiles = lambda items, cls='tile': ''.join(
        f'<div class="{cls}" data-reveal><span class="tnum">{i:02d}</span><h3>{e(h)}</h3><p>{e(t)}</p></div>' for i, (h, t) in enumerate(items, 1))

    codes = ''
    if 'codes' in C:
        mark = {'yes': '✓', 'alt': '↺', 'no': '✕'}
        rows = ''.join(f'<tr class="c-{k}"><td><code>{e(c)}</code></td><td>{e(m)}</td><td><span class="cm">{mark[k]}</span>{e(a)}</td></tr>' for c, m, k, a in C['codes'])
        cols = C['codes_cols']
        table_html = (f'''    <div class="codes-wrap" data-reveal>\n      <table class="codes"><thead><tr><th>{e(cols[0])}</th><th>{e(cols[1])}</th><th>{e(cols[2])}</th></tr></thead><tbody>{rows}</tbody></table>\n    </div>''') if C['codes'] else ''
        codes = f'''
<section class="sec sec-line" id="codes">
  <div class="wrap">
    <div class="sec-head"><h2 class="display" data-words>{e(C['codes_h'])}</h2><p class="sub" data-reveal>{e(C['codes_sub'])}</p></div>
{table_html}
    <p class="codes-note" data-reveal>{e(C['codes_note'])}</p>
    <div class="tds glass" data-reveal><h3>{e(C['tds_h'])}</h3><p>{e(C['tds_p'])}</p></div>
  </div>
</section>'''

    steps = ''.join(f'<li><span class="n">{i}</span><h3>{e(D["st%dh" % i])}</h3><p>{e(D["st%dp" % i])}</p></li>' for i in range(1, 6))
    faq = ''.join(f'<details class="qa" data-reveal><summary><h3>{e(q)}</h3><i aria-hidden="true"></i></summary><div class="qa-a"><p>{e(a)}</p></div></details>' for q, a in C['faq'])
    rel = ''.join(f'<a class="rel tilt" href="{home}services/{q["slug"]}/" data-reveal data-cursor="{e(U["more"])}"><span class="rel-k">{e(U["services"])}</span><strong>{e(q[lang]["crumb"])}</strong><p>{e(q[lang]["desc"])}</p><span class="rel-arrow" aria-hidden="true">→</span></a>' for q in others)
    import blog as BL
    rel += ''.join(BL.card(x, lang, BL.BLOG_UI[lang]) for x in [y for y in BL.ARTICLES if y['service'] == p['slug']][:2])
    rel += f'<a class="rel rel-home tilt" href="{home}#services" data-reveal data-cursor="{e(U["more"])}"><span class="rel-k">GURO PSP</span><strong>{e(U["all_services"])}</strong><p>{e(D["svc_sub"])}</p><span class="rel-arrow" aria-hidden="true">→</span></a>'
    h1 = C['h1']

    return chrome_top(lang, D, ver, C['title'], C['desc'], C['og_title'], url, alt_en, alt_ru, ld, redirect, p['src'], cur=p['slug']) + f'''<main>

<section class="hero hero-svc" id="top">
  <div class="wrap hero-grid">
    <div class="hero-in">
      <nav class="crumbs" aria-label="Breadcrumb" data-intro><a href="{home}">GURO PSP</a><span aria-hidden="true">/</span><span aria-current="page">{e(C['crumb'])}</span></nav>
      <p class="kicker" data-intro><b></b>{e(C['kicker'])}</p>
      <h1 class="display hero-title" id="heroTitle">
        <span class="ln" data-chars>{e(h1[0])}</span>
        <span class="ln" data-chars>{e(h1[1])}</span>
        <span class="ln ln-metal"><span class="metal">{e(h1[2])}</span></span>
      </h1>
      <p class="lead" data-intro>{e(C['lead'])}</p>
      <div class="ctas" data-intro>
        <a href="https://t.me/GuroArtem" class="btn btn-lg magnetic" data-tg data-cursor="Telegram" target="_blank" rel="noopener"><span>{e(D['cta_discuss'])}</span></a>
        <a href="#price" class="btn btn-lg btn-ghost magnetic" data-cursor="{e(D['cursor_view'])}"><span>{e(U['price'])}</span></a>
      </div>
    </div>
    <aside class="live glass svc-card" data-intro>
      <div class="live-head"><span class="live-dot"></span>{e(C['card_h'])}</div>
      {card_body}
      <p class="live-note">{e(C['card_note'])}</p>
    </aside>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><h2 class="display" data-words>{e(C['signs_h'])}</h2><p class="sub" data-reveal>{e(C['signs_sub'])}</p></div>
    <div class="tiles tiles-{len(C['signs'])}">{tiles(C['signs'])}</div>
  </div>
</section>

<section class="sec sec-line">
  <div class="wrap">
    <div class="sec-head"><h2 class="display" data-words>{e(C['areas_h'])}</h2><p class="sub" data-reveal>{e(C['areas_sub'])}</p></div>
    <div class="areas">{tiles(C['areas'], 'area')}</div>
  </div>
</section>
{codes}
<section class="sec sec-line">
  <div class="wrap">
    <div class="sec-head"><h2 class="display" data-words>{e(C['out_h'])}</h2><p class="sub" data-reveal>{e(C['out_sub'])}</p></div>
    <div class="tiles tiles-4">{tiles(C['out'], 'tile tile-out')}</div>
  </div>
</section>

<section class="proc-sec sec-line" id="process">
  <div class="wrap">
    <div class="sec-head"><h2 class="display" data-words>{e(D['proc_h'])}</h2><p class="sub" data-reveal>{e(D['proc_sub'])}</p></div>
    <div class="steps-wrap" id="steps"><div class="steps-rail" aria-hidden="true"><i></i></div><ol class="steps">{steps}</ol></div>
  </div>
</section>

<section class="price-sec" id="price">
  <div class="wrap">
    <div class="sec-head"><h2 class="display" data-words>{e(D['price_h'])}</h2><p class="sub" data-reveal>{e(D['price_sub'])}</p></div>
    <div class="price">
      <div class="pbox tilt" data-reveal><span class="pbox-lbl">{e(D['pb1l'])}</span><strong>{e(D['pb1v'])}</strong><p>{e(D['pb1p'])}</p></div>
      <div class="pbox pbox-hl tilt" data-reveal><span class="pbox-lbl">{e(D['pb2l'])}</span><strong class="metal">{e(D['pb2v'])}</strong><p>{e(D['pb2p'])}</p></div>
    </div>
  </div>
</section>

<section class="faq-sec" id="faq">
  <div class="wrap">
    <div class="sec-head"><h2 class="display" data-words>{e(U['faq'])}</h2></div>
    <div class="faq-list">{faq}</div>
  </div>
</section>

<section class="sec sec-line">
  <div class="wrap">
    <div class="sec-head"><h2 class="display" data-words>{e(U['other'])}</h2></div>
    <div class="rels">{rel}</div>
  </div>
</section>

<section class="cta-sec" id="contact">
  <div class="cta-glow" aria-hidden="true"></div>
  <div class="wrap cta">
    <h2 class="display cta-title" data-words>{e(D['cta_h'])}</h2>
    <p class="sub" data-reveal>{e(D['cta_p'])}</p>
    <div data-reveal><a href="https://t.me/GuroArtem" class="btn btn-xl magnetic" data-tg data-cursor="Telegram" target="_blank" rel="noopener"><span>{e(D['cta_tg'])}</span></a></div>
  </div>
</section>

</main>
''' + chrome_bottom(lang, D, ver)
