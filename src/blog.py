"""Blog hub, article pages and RSS feeds."""
import json, re, datetime, html as H
from blog_content import ARTICLES, BLOG_UI
from services_content import PAGES as SVC
from layout import chrome_top, chrome_bottom, prefix, redirect_js, SITE, e

MONTHS_RU = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']


def fdate(iso, lang):
    d = datetime.date.fromisoformat(iso)
    return f'{d.day} {MONTHS_RU[d.month - 1]} {d.year}' if lang == 'ru' else d.strftime('%-d %B %Y')


def inline(t):
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', e(t))


def plain(t):
    return t.replace('**', '')


def art_url(a, lang):
    return SITE + prefix(lang) + 'blog/' + a['slug'] + '/'


def hub_url(lang):
    return SITE + prefix(lang) + 'blog/'


def svc_by_slug(slug):
    return next(p for p in SVC if p['slug'] == slug)


def org():
    return {'@type': 'Organization', '@id': SITE + '/#org', 'name': 'GURO PSP', 'url': SITE + '/',
            'logo': {'@type': 'ImageObject', 'url': SITE + '/icon-512.png', 'width': 512, 'height': 512}}


def ld_dump(g):
    return json.dumps({'@context': 'https://schema.org', '@graph': g}, ensure_ascii=False).replace('</', '<\\/')


def cta_box(slug, lang, U):
    p = svc_by_slug(slug); C = p[lang]
    return (f'<aside class="art-cta" data-reveal><span class="rel-k">{e(U["related"])}</span>'
            f'<strong>{e(C["crumb"])}</strong><p>{e(C["desc"])}</p>'
            f'<a class="btn btn-sm btn-ghost magnetic" href="{prefix(lang)}services/{p["slug"]}/" data-cursor="{e(U["read"])}"><span>{e(U["more"])}</span></a></aside>')


def render_body(blocks, lang, U):
    out = []
    for b in blocks:
        t = b[0]
        if t == 'h2': out.append(f'<h2 id="{b[1]}">{e(b[2])}</h2>')
        elif t == 'p': out.append(f'<p>{inline(b[1])}</p>')
        elif t in ('ul', 'ol'): out.append(f'<{t}>' + ''.join(f'<li>{inline(x)}</li>' for x in b[1]) + f'</{t}>')
        elif t == 'table':
            head = ''.join(f'<th>{e(c)}</th>' for c in b[1])
            rows = ''.join('<tr>' + ''.join(f'<td>{"<code>" + e(c) + "</code>" if i == 0 else e(c)}</td>' for i, c in enumerate(r)) + '</tr>' for r in b[2])
            out.append(f'<div class="codes-wrap art-table"><table class="codes"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>')
        elif t == 'cta': out.append(cta_box(b[1], lang, U))
    return '\n'.join(out)


def render_article(a, lang, D, ver):
    C = a[lang]; U = BLOG_UI[lang]; url = art_url(a, lang); home = prefix(lang)
    alt_en, alt_ru = art_url(a, 'en'), art_url(a, 'ru')
    words = len(H.unescape(re.sub(r'<[^>]+>', ' ', render_body(C['body'], lang, U))).split())
    g = [org(),
         {'@type': 'BlogPosting', '@id': url + '#article', 'headline': C['title'], 'description': C['desc'], 'inLanguage': lang,
          'datePublished': a['date'], 'dateModified': a['updated'], 'mainEntityOfPage': url, 'url': url,
          'image': {'@type': 'ImageObject', 'url': f'{SITE}/og-{lang}.jpg', 'width': 1200, 'height': 630},
          'author': {'@id': SITE + '/#org'}, 'publisher': {'@id': SITE + '/#org'}, 'wordCount': words,
          'articleSection': C['tag'], 'isPartOf': {'@id': hub_url(lang) + '#blog'},
          'about': {'@id': SITE + prefix(lang) + 'services/' + a['service'] + '/#service'}},
         {'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
             {'@type': 'ListItem', 'position': 1, 'name': 'GURO PSP', 'item': SITE + home},
             {'@type': 'ListItem', 'position': 2, 'name': U['crumb'], 'item': hub_url(lang)},
             {'@type': 'ListItem', 'position': 3, 'name': C['title'], 'item': url}]},
         {'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
             {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': ans}} for q, ans in C['faq']]}]
    extra = (f'<meta property="article:published_time" content="{a["date"]}T08:00:00+00:00">\n'
             f'<meta property="article:modified_time" content="{a["updated"]}T08:00:00+00:00">\n'
             f'<meta property="article:section" content="{e(C["tag"])}">\n')
    redirect = redirect_js('/ru/blog/' + a['slug'] + '/') if lang == 'en' else ''
    toc = ''.join(f'<li><a href="#{b[1]}">{e(b[2])}</a></li>' for b in C['body'] if b[0] == 'h2')
    faq = ''.join(f'<details class="qa"><summary><h3>{e(q)}</h3><i aria-hidden="true"></i></summary><div class="qa-a"><p>{e(ans)}</p></div></details>' for q, ans in C['faq'])
    others = [x for x in ARTICLES if x is not a]
    rel = ''.join(card(x, lang, U) for x in others)
    svc = svc_by_slug(a['service'])
    rel += (f'<a class="rel tilt" href="{home}services/{svc["slug"]}/" data-reveal data-cursor="{e(U["read"])}"><span class="rel-k">{e(U["related"])}</span>'
            f'<strong>{e(svc[lang]["crumb"])}</strong><p>{e(svc[lang]["desc"])}</p><span class="rel-arrow" aria-hidden="true">→</span></a>')

    body = f'''<main>
<article class="art">
<header class="art-hero">
  <div class="wrap art-wrap">
    <nav class="crumbs" aria-label="Breadcrumb" data-intro><a href="{home}">GURO PSP</a><span aria-hidden="true">/</span><a href="{home}blog/">{e(U['crumb'])}</a><span aria-hidden="true">/</span><span aria-current="page">{e(C['tag'])}</span></nav>
    <p class="art-meta" data-intro><span class="art-tag">{e(C['tag'])}</span><time datetime="{a['date']}">{fdate(a['date'], lang)}</time><span>{e(C['read'])}</span></p>
    <h1 class="display art-title" data-intro>{e(C['title'])}</h1>
    <p class="lead art-lead" data-intro>{e(C['lead'])}</p>
  </div>
</header>
<div class="wrap art-grid">
  <aside class="art-toc" aria-label="{e(U['toc'])}"><p>{e(U['toc'])}</p><ol>{toc}</ol></aside>
  <div class="prose">
{render_body(C['body'], lang, U)}
    <section class="art-faq" aria-labelledby="faq-h"><h2 id="faq-h">{e(U['faq'])}</h2><div class="faq-list">{faq}</div></section>
    <p class="art-upd">{e(U['published'])}: <time datetime="{a['date']}">{fdate(a['date'], lang)}</time> · {e(U['updated'])}: <time datetime="{a['updated']}">{fdate(a['updated'], lang)}</time> · GURO PSP</p>
  </div>
</div>
</article>

<section class="sec sec-line">
  <div class="wrap">
    <div class="sec-head"><h2 class="display" data-words>{e(U['other'])}</h2><p class="sub" data-reveal><a class="svc-link" href="{home}blog/">{e(U['back'])}<span aria-hidden="true">→</span></a></p></div>
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
'''
    return chrome_top(lang, D, ver, C['seo_title'], C['desc'], C['title'], url, alt_en, alt_ru, ld_dump(g), redirect,
                      'blog-' + a['slug'].split('-')[0], cur='blog', og_type='article', extra_head=extra) + body + chrome_bottom(lang, D, ver)


def card(a, lang, U):
    C = a[lang]
    return (f'<a class="rel post tilt" href="{prefix(lang)}blog/{a["slug"]}/" data-reveal data-cursor="{e(U["read"])}">'
            f'<span class="rel-k">{e(C["tag"])} · <time datetime="{a["date"]}">{fdate(a["date"], lang)}</time> · {e(C["read"])}</span>'
            f'<strong>{e(C["title"])}</strong><p>{e(C["desc"])}</p><span class="rel-arrow" aria-hidden="true">→</span></a>')


def render_hub(lang, D, ver):
    U = BLOG_UI[lang]; url = hub_url(lang); home = prefix(lang)
    g = [org(),
         {'@type': 'Blog', '@id': url + '#blog', 'url': url, 'name': U['h1'], 'description': U['desc'], 'inLanguage': lang, 'publisher': {'@id': SITE + '/#org'},
          'blogPost': [{'@type': 'BlogPosting', 'headline': a[lang]['title'], 'url': art_url(a, lang), 'datePublished': a['date']} for a in ARTICLES]},
         {'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
             {'@type': 'ListItem', 'position': 1, 'name': 'GURO PSP', 'item': SITE + home},
             {'@type': 'ListItem', 'position': 2, 'name': U['crumb'], 'item': url}]}]
    redirect = redirect_js('/ru/blog/') if lang == 'en' else ''
    cards = ''.join(card(a, lang, U) for a in sorted(ARTICLES, key=lambda x: x['date'], reverse=True))
    body = f'''<main>
<section class="hero hero-svc hero-blog" id="top">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb" data-intro><a href="{home}">GURO PSP</a><span aria-hidden="true">/</span><span aria-current="page">{e(U['crumb'])}</span></nav>
    <h1 class="display art-title" data-intro>{e(U['h1'])}</h1>
    <p class="lead" data-intro>{e(U['sub'])}</p>
  </div>
</section>
<section class="sec sec-blog">
  <div class="wrap"><div class="rels posts">{cards}</div></div>
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
'''
    return chrome_top(lang, D, ver, U['seo_title'], U['desc'], U['h1'], url, hub_url('en'), hub_url('ru'), ld_dump(g), redirect, 'blog', cur='blog') + body + chrome_bottom(lang, D, ver)


def render_rss(lang):
    U = BLOG_UI[lang]
    def rfc(d): return datetime.datetime.fromisoformat(d + 'T08:00:00+00:00').strftime('%a, %d %b %Y %H:%M:%S +0000')
    items = ''.join(f'''  <item>
    <title>{e(a[lang]['title'])}</title>
    <link>{art_url(a, lang)}</link>
    <guid isPermaLink="true">{art_url(a, lang)}</guid>
    <pubDate>{rfc(a['date'])}</pubDate>
    <category>{e(a[lang]['tag'])}</category>
    <description>{e(a[lang]['desc'])}</description>
  </item>
''' for a in sorted(ARTICLES, key=lambda x: x['date'], reverse=True))
    last = max(a['updated'] for a in ARTICLES)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{e(U['h1'])} — GURO PSP</title>
  <link>{hub_url(lang)}</link>
  <atom:link href="{hub_url(lang)}feed.xml" rel="self" type="application/rss+xml"/>
  <description>{e(U['desc'])}</description>
  <language>{lang}</language>
  <lastBuildDate>{rfc(last)}</lastBuildDate>
{items}</channel>
</rss>
'''
