"""GURO ecosystem page (/ecosystem/ and /ru/ecosystem/): GURO PSP, GURO ID, Private Gambling Community, iGaming School.
Facts only from the live product sites and the owner. No invented numbers. OstrovUA is deliberately NOT part of this."""
import json
from layout import chrome_top, chrome_bottom, prefix, redirect_js, SITE, e

SLUG = 'ecosystem'
L_ID = 'https://guroid.com/'
L_SCHOOL = 'https://igaming-school.com/'
L_COMMUNITY = 'https://t.me/GamblingCommunitybot'
L_OWNER = 'https://t.me/GuroArtem'

T = {
 'en': dict(
  title='GURO ecosystem: GURO PSP, GURO ID, community and iGaming School | GURO PSP',
  og='GURO — one team, four products for iGaming',
  desc='GURO PSP is part of GURO: a 5,000+ member iGaming community, the GURO ID reputation platform, iGaming School and payments consulting.',
  nav='Ecosystem', crumb='GURO ecosystem', kicker='GURO ecosystem',
  h1=('One team.', 'Four products.', 'One industry.'),
  lead='GURO PSP is part of GURO, a group of products built for people who work in iGaming. A community where the industry talks, a reputation platform where deals are confirmed by both sides, a school that trains new people, and payments consulting for operators.',
  c_main='Explore products', c_talk='Talk to the founder',
  orbit_core='GURO', orbit_aria='GURO ecosystem: GURO PSP, GURO ID, Private Gambling Community and iGaming School connected to one core',
  grid_h='Four products, one network', grid_sub='Each product works on its own. Together they cover the whole path of a person and a company in iGaming.',
  open='Open', more='Details',
  p_psp=('GURO PSP', 'Payments consulting', 'Audits of the cashier and PSPs, smart routing and cascading, monitoring. For operators that lose deposits.'),
  p_id=('GURO ID', 'Reputation platform', 'A work profile where every deal and hire is confirmed by the other side. Reputation you cannot buy.'),
  p_pgc=('Private Gambling Community', 'Industry community', 'A private Telegram community of 5,000+ people from gambling, betting, fintech, crypto and other verticals.'),
  p_school=('iGaming School', 'Education', 'Courses on how the industry works, from an introduction to iGaming to C-level tracks, with a verifiable certificate.'),
  path_h='How the pieces connect', path_sub='A typical path through GURO. You can enter at any point.',
  path=[('Learn', 'iGaming School gives newcomers and managers a map of the industry.'),
        ('Connect', 'The community is where people find jobs, partners, PSPs and warnings about scammers.'),
        ('Prove', 'GURO ID turns real deals and hires into a confirmed rating that stays with the person.'),
        ('Grow', 'GURO PSP helps operators keep more deposits once the business is running.')],
  pgc_k='Community', pgc_h='Private Gambling Community',
  pgc_p='A closed Telegram community for people who work in iGaming. Instead of one noisy chat, it is split into topics, so a recruiter, a payments manager and an affiliate each find their own thread.',
  pgc_count_l='members', pgc_vert_l='verticals',
  pgc_topics_h='Topics inside',
  pgc_topics=['Jobs and HR', 'Payments', 'Networking', 'Industry events', 'Scammer blacklist', 'General chat'],
  pgc_verts=['Gambling', 'Betting', 'Fintech', 'Crypto', 'Nutra', 'Dating', 'Other'],
  pgc_cta='Join the community',
  sp_h='Become a sponsor', sp_p='Brands that sponsor the community get in front of people who make decisions in the industry. Sponsorship is also how a brand gets verified in GURO ID.',
  sp_tiers=[('Silver', 'Verified brand badge in GURO ID.'),
            ('Gold', 'Verified brand badge, plus GURO ID brand tags for your team members.'),
            ('Platinum', 'The top tier: verified badge and team brand tags. The full package is in the media kit.')],
  sp_note='Placements, formats and prices are in the media kit. The founder sends it on request and verifies sponsor brands personally.',
  sp_cta='Request the media kit',
  id_k='Reputation', id_h='GURO ID',
  id_p='In iGaming, a CV says what a person claims. GURO ID shows what was confirmed. You name the counterparty, they confirm in Telegram, and only then the record appears in both profiles.',
  id_feats=[('Confirmed by both sides', 'Without the second side the record stays a draft, so a rating cannot be inflated alone.'),
            ('Private by default', 'Counterparty names and amounts are hidden. Public is the fact that two sides confirmed a partnership.'),
            ('Rating that stays yours', 'It belongs to the person, not the company, and survives a change of job.'),
            ('Jobs board', 'Official vacancies from verified companies, search by vertical and role.')],
  id_card_ok='Partnership confirmed', id_card_both='both sides', id_card_cp='Counterparty', id_card_sum='Amount', id_card_hidden='hidden',
  id_card_deal='Deal', id_card_hire='Hire', id_card_pts='pts',
  id_cta='Open GURO ID',
  sc_k='Education', sc_h='iGaming School',
  sc_p='A school about how the iGaming business actually works. It starts with an introduction to the industry and continues with tracks for leaders of different types of companies.',
  sc_courses=['Introduction to iGaming', 'CEO: casino operator', 'CEO: CPA network', 'CEO: media buying team', 'CEO: game provider', 'CEO: casino platform'],
  sc_cert='After a course the student gets a certificate that anyone can verify by its number on the school website.',
  sc_lang='Courses are taught in Russian.',
  sc_cta='Open iGaming School',
  psp_k='Payments', psp_h='GURO PSP',
  psp_p='This site. We audit the cashier, PSP stack, routing and monitoring of iGaming operators and show where deposits are lost and what it costs.',
  psp_cta='See services',
  end_h='Partner with GURO', end_p='Sponsorship, a partnership between products or a payments project. Write to the founder, Artem.',
  end_cta='Message Artem on Telegram',
  ext='opens in a new tab',
 ),
 'ru': dict(
  title='Экосистема GURO: GURO PSP, GURO ID, комьюнити и iGaming School | GURO PSP',
  og='GURO — одна команда, четыре продукта для iGaming',
  desc='GURO PSP — часть GURO: iGaming-комьюнити на 5 000+ человек, платформа репутации GURO ID, iGaming School и консалтинг по платежам.',
  nav='Экосистема', crumb='Экосистема GURO', kicker='Экосистема GURO',
  h1=('Одна команда.', 'Четыре продукта.', 'Одна индустрия.'),
  lead='GURO PSP — часть GURO, группы продуктов для тех, кто работает в iGaming. Комьюнити, где общается индустрия. Платформа репутации, где сделки подтверждает вторая сторона. Школа, которая готовит новых людей. И консалтинг по платежам для операторов.',
  c_main='Смотреть продукты', c_talk='Написать основателю',
  orbit_core='GURO', orbit_aria='Экосистема GURO: GURO PSP, GURO ID, Private Gambling Community и iGaming School вокруг одного ядра',
  grid_h='Четыре продукта, одна сеть', grid_sub='Каждый продукт работает сам по себе. Вместе они закрывают весь путь человека и компании в iGaming.',
  open='Открыть', more='Подробнее',
  p_psp=('GURO PSP', 'Консалтинг по платежам', 'Аудит кассы и PSP, умный роутинг и каскадинг, мониторинг. Для операторов, которые теряют депозиты.'),
  p_id=('GURO ID', 'Платформа репутации', 'Рабочий профиль, где каждую сделку и найм подтверждает вторая сторона. Репутация, которую нельзя купить.'),
  p_pgc=('Private Gambling Community', 'Комьюнити индустрии', 'Закрытое Telegram-сообщество на 5 000+ человек из гемблинга, беттинга, финтеха, крипты и других вертикалей.'),
  p_school=('iGaming School', 'Обучение', 'Курсы о том, как устроена индустрия: от введения в iGaming до программ для руководителей. С сертификатом, который можно проверить.'),
  path_h='Как всё связано', path_sub='Типичный путь внутри GURO. Зайти можно с любой точки.',
  path=[('Учиться', 'iGaming School даёт новичкам и менеджерам карту индустрии.'),
        ('Общаться', 'В комьюнити ищут работу, партнёров, PSP и узнают о скамерах.'),
        ('Подтверждать', 'GURO ID превращает реальные сделки и наймы в подтверждённый рейтинг, который остаётся с человеком.'),
        ('Расти', 'GURO PSP помогает операторам сохранять больше депозитов, когда бизнес уже работает.')],
  pgc_k='Комьюнити', pgc_h='Private Gambling Community',
  pgc_p='Закрытое Telegram-сообщество для тех, кто работает в iGaming. Вместо одного шумного чата — разделы по темам: рекрутер, платёжник и аффилиат находят каждый свою ветку.',
  pgc_count_l='участников', pgc_vert_l='вертикалей',
  pgc_topics_h='Разделы внутри',
  pgc_topics=['Вакансии и HR', 'Платежи', 'Нетворкинг', 'Ивенты индустрии', 'Чёрный список скамеров', 'Общий чат'],
  pgc_verts=['Гемблинг', 'Беттинг', 'Финтех', 'Крипта', 'Нутра', 'Дейтинг', 'Другое'],
  pgc_cta='Вступить в комьюнити',
  sp_h='Стать спонсором', sp_p='Бренды-спонсоры видны людям, которые принимают решения в индустрии. А ещё через спонсорство бренд получает верификацию в GURO ID.',
  sp_tiers=[('Silver', 'Верифицированный бейдж бренда в GURO ID.'),
            ('Gold', 'Верифицированный бейдж и бренд-теги GURO ID для сотрудников.'),
            ('Platinum', 'Максимальный уровень: бейдж и бренд-теги для команды. Полный пакет — в медиаките.')],
  sp_note='Размещения, форматы и цены — в медиаките. Основатель присылает его по запросу и лично верифицирует бренды спонсоров.',
  sp_cta='Запросить медиакит',
  id_k='Репутация', id_h='GURO ID',
  id_p='В iGaming резюме говорит о том, что человек заявляет. GURO ID показывает то, что подтверждено. Вы указываете контрагента, он подтверждает в Telegram — и только тогда запись появляется в обоих профилях.',
  id_feats=[('Подтверждает вторая сторона', 'Без ответа партнёра запись остаётся черновиком — накрутить рейтинг в одиночку нельзя.'),
            ('Приватно по умолчанию', 'Имена контрагентов и суммы скрыты. Публичен сам факт: партнёрство подтвердили обе стороны.'),
            ('Рейтинг остаётся вашим', 'Он принадлежит человеку, а не компании, и сохраняется при смене работы.'),
            ('Доска вакансий', 'Официальные вакансии верифицированных компаний, поиск по вертикали и должности.')],
  id_card_ok='Партнёрство подтверждено', id_card_both='обе стороны', id_card_cp='Контрагент', id_card_sum='Сумма', id_card_hidden='скрыто',
  id_card_deal='Сделка', id_card_hire='Найм', id_card_pts='баллов',
  id_cta='Открыть GURO ID',
  sc_k='Обучение', sc_h='iGaming School',
  sc_p='Школа о том, как на самом деле устроен бизнес в iGaming. Начинается с введения в индустрию и продолжается программами для руководителей разных типов компаний.',
  sc_courses=['Введение в iGaming', 'CEO: оператор казино', 'CEO: CPA-сеть', 'CEO: арбитражная команда', 'CEO: игровой провайдер', 'CEO: платформа казино'],
  sc_cert='После курса студент получает сертификат, который любой может проверить по номеру на сайте школы.',
  sc_lang='Обучение на русском языке.',
  sc_cta='Открыть iGaming School',
  psp_k='Платежи', psp_h='GURO PSP',
  psp_p='Этот сайт. Мы проверяем кассу, набор PSP, роутинг и мониторинг iGaming-операторов и показываем, где теряются депозиты и сколько это стоит.',
  psp_cta='Смотреть услуги',
  end_h='Партнёрство с GURO', end_p='Спонсорство, партнёрство между продуктами или проект по платежам — напишите основателю, Артёму.',
  end_cta='Написать Артёму в Telegram',
  ext='откроется в новой вкладке',
 ),
}


def url(lang):
    return SITE + prefix(lang) + SLUG + '/'


def orbit(C, lang):
    h = prefix(lang)
    # 4 nodes around a core; links pulse from the core outwards
    nodes = [('psp', 'GURO PSP', 300, 70), ('id', 'GURO ID', 520, 250), ('pgc', 'COMMUNITY', 300, 430), ('school', 'iGAMING SCHOOL', 80, 250)]
    links = ''.join(f'<path class="eo-l" d="M300 250 L{x} {y}"/><circle class="eo-p eo-p{i}" r="4"><animateMotion dur="{2.6 + i * .4}s" repeatCount="indefinite" path="M300 250 L{x} {y}"/></circle>' for i, (k, n, x, y) in enumerate(nodes))
    node = ''.join(f'<a href="#{k}" class="eo-n eo-{k}"><circle cx="{x}" cy="{y}" r="44"/><circle class="eo-n-in" cx="{x}" cy="{y}" r="7"/><text x="{x}" y="{y + 68}">{n}</text></a>' for k, n, x, y in nodes)
    return f'''<svg class="eco-orbit" viewBox="0 0 600 520" role="img" aria-label="{e(C['orbit_aria'])}">
  <circle class="eo-ring" cx="300" cy="250" r="180"/><circle class="eo-ring eo-ring2" cx="300" cy="250" r="118"/>
  {links}
  <g class="eo-core"><circle cx="300" cy="250" r="62"/><circle class="eo-core-ring" cx="300" cy="250" r="30"/><circle class="eo-core-dot" cx="300" cy="250" r="8"/></g>
  {node}
</svg>'''


def jsonld(lang, C):
    u = url(lang); org = SITE + '/#org'
    items = [(C['p_psp'], SITE + prefix(lang)), (C['p_id'], L_ID), (C['p_pgc'], L_COMMUNITY), (C['p_school'], L_SCHOOL)]
    g = [
        {'@type': 'Organization', '@id': org, 'name': 'GURO PSP', 'alternateName': 'GuroPSP', 'url': SITE + '/',
         'logo': {'@type': 'ImageObject', 'url': SITE + '/icon-512.png', 'width': 512, 'height': 512},
         'founder': {'@type': 'Person', 'name': 'Artem Guro', 'sameAs': [L_OWNER]}},
        {'@type': 'WebPage', '@id': u + '#webpage', 'url': u, 'name': C['title'], 'description': C['desc'], 'inLanguage': lang,
         'isPartOf': {'@id': SITE + '/#website'}, 'breadcrumb': {'@id': u + '#breadcrumb'}, 'mainEntity': {'@id': u + '#products'}},
        {'@type': 'BreadcrumbList', '@id': u + '#breadcrumb', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'GURO PSP', 'item': SITE + prefix(lang)},
            {'@type': 'ListItem', 'position': 2, 'name': C['crumb'], 'item': u}]},
        {'@type': 'ItemList', '@id': u + '#products', 'name': C['crumb'], 'itemListElement': [
            {'@type': 'ListItem', 'position': i, 'item': {'@type': 'Brand', 'name': p[0], 'description': p[2], 'url': link}}
            for i, (p, link) in enumerate(items, 1)]},
    ]
    return json.dumps({'@context': 'https://schema.org', '@graph': g}, ensure_ascii=False).replace('</', '<\\/')


def ext_btn(href, text, C, ghost=False):
    return (f'<a href="{href}" class="btn btn-lg{" btn-ghost" if ghost else ""} magnetic" target="_blank" rel="noopener" '
            f'data-cursor="{e(C["open"])}" aria-label="{e(text)} ({e(C["ext"])})"><span>{e(text)}</span></a>')


def render(lang, D, ver):
    C = T[lang]; h = prefix(lang)
    u = url(lang)
    cards = ''
    for k, p, link, ext in [('psp', C['p_psp'], h + '#services', False), ('id', C['p_id'], L_ID, True),
                            ('pgc', C['p_pgc'], L_COMMUNITY, True), ('school', C['p_school'], L_SCHOOL, True)]:
        cards += (f'<a class="eco-card tilt eco-c-{k}" href="#{k}" data-reveal data-cursor="{e(C["more"])}">'
                  f'<span class="eco-glyph" aria-hidden="true"><i></i></span><span class="rel-k">{e(p[1])}</span>'
                  f'<strong>{e(p[0])}</strong><p>{e(p[2])}</p><span class="rel-arrow" aria-hidden="true">→</span></a>')
    path = ''.join(f'<li><span class="n">{i}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(C['path'], 1))
    topics = ''.join(f'<span class="chip">#{e(t)}</span>' for t in C['pgc_topics'])
    verts = ''.join(f'<span class="mk">{e(t)}</span>' for t in C['pgc_verts'])
    tiers = ''.join(f'<div class="tier tier-{n.lower()} tilt" data-reveal><span class="tier-n">{e(n)}</span><p>{e(t)}</p></div>' for n, t in C['sp_tiers'])
    feats = ''.join(f'<div class="ef" data-reveal><span class="ef-i" aria-hidden="true">✓</span><div><h3>{e(a)}</h3><p>{e(b)}</p></div></div>' for a, b in C['id_feats'])
    courses = ''.join(f'<li data-reveal><span class="cn">{i:02d}</span>{e(c)}</li>' for i, c in enumerate(C['sc_courses'], 1))
    redirect = redirect_js('/ru/' + SLUG + '/') if lang == 'en' else ''
    return chrome_top(lang, D, ver, C['title'], C['desc'], C['og'], u, url('en'), url('ru'), jsonld(lang, C), redirect, 'site_eco', cur=SLUG) + f'''<main class="eco">
<section class="hero hero-svc hero-eco" id="top">
  <div class="wrap hero-grid">
    <div class="hero-in">
      <nav class="crumbs" aria-label="Breadcrumb" data-intro><a href="{h}">GURO PSP</a><span aria-hidden="true">/</span><span aria-current="page">{e(C['crumb'])}</span></nav>
      <p class="kicker" data-intro><b></b>{e(C['kicker'])}</p>
      <h1 class="display hero-title" id="heroTitle">
        <span class="ln" data-chars>{e(C['h1'][0])}</span>
        <span class="ln" data-chars>{e(C['h1'][1])}</span>
        <span class="ln ln-metal"><span class="metal">{e(C['h1'][2])}</span></span>
      </h1>
      <p class="lead" data-intro>{e(C['lead'])}</p>
      <div class="ctas" data-intro>
        <a href="#products" class="btn btn-lg magnetic" data-cursor="{e(C['more'])}"><span>{e(C['c_main'])}</span></a>
        <a href="{L_OWNER}" class="btn btn-lg btn-ghost magnetic" target="_blank" rel="noopener" data-cursor="Telegram"><span>{e(C['c_talk'])}</span></a>
      </div>
    </div>
    <div class="eco-stage" data-intro>{orbit(C, lang)}</div>
  </div>
</section>

<section class="sec" id="products">
  <div class="wrap">
    <div class="sec-head"><h2 class="display" data-words>{e(C['grid_h'])}</h2><p class="sub" data-reveal>{e(C['grid_sub'])}</p></div>
    <div class="eco-grid">{cards}</div>
  </div>
</section>

<section class="proc-sec sec-line" id="process">
  <div class="wrap">
    <div class="sec-head"><h2 class="display" data-words>{e(C['path_h'])}</h2><p class="sub" data-reveal>{e(C['path_sub'])}</p></div>
    <div class="steps-wrap" id="steps"><div class="steps-rail" aria-hidden="true"><i></i></div><ol class="steps steps-4">{path}</ol></div>
  </div>
</section>

<section class="sec sec-line eco-sec" id="pgc">
  <div class="wrap eco-split">
    <div class="eco-txt">
      <p class="kicker" data-reveal><b></b>{e(C['pgc_k'])}</p>
      <h2 class="display" data-words>{e(C['pgc_h'])}</h2>
      <p class="eco-p" data-reveal>{e(C['pgc_p'])}</p>
      <div class="eco-stats" data-reveal>
        <div><strong class="metal"><span data-count="5000">5000</span>+</strong><span>{e(C['pgc_count_l'])}</span></div>
        <div><strong class="metal"><span data-count="7">7</span></strong><span>{e(C['pgc_vert_l'])}</span></div>
      </div>
      <div class="markets" data-reveal>{verts}</div>
      <div class="ctas" data-reveal>{ext_btn(L_COMMUNITY, C['pgc_cta'], C)}</div>
    </div>
    <div class="eco-vis glass" data-reveal>
      <div class="live-head"><span class="live-dot"></span>{e(C['pgc_topics_h'])}</div>
      <div class="chips">{topics}</div>
    </div>
  </div>
  <div class="wrap sp" id="sponsors">
    <div class="sec-head"><h2 class="display" data-words>{e(C['sp_h'])}</h2><p class="sub" data-reveal>{e(C['sp_p'])}</p></div>
    <div class="tiers">{tiers}</div>
    <p class="price-free" data-reveal>{e(C['sp_note'])}</p>
    <div class="ctas ctas-c" data-reveal><a href="{L_OWNER}" class="btn btn-lg magnetic" target="_blank" rel="noopener" data-cursor="Telegram"><span>{e(C['sp_cta'])}</span></a></div>
  </div>
</section>

<section class="sec sec-line eco-sec" id="id">
  <div class="wrap eco-split eco-rev">
    <div class="eco-txt">
      <p class="kicker" data-reveal><b></b>{e(C['id_k'])}</p>
      <h2 class="display" data-words>{e(C['id_h'])}</h2>
      <p class="eco-p" data-reveal>{e(C['id_p'])}</p>
      <div class="efs">{feats}</div>
      <div class="ctas" data-reveal>{ext_btn(L_ID, C['id_cta'], C)}</div>
    </div>
    <div class="eco-vis idcard glass" data-reveal aria-hidden="true">
      <div class="idc-ok"><span class="idc-check">✓</span><b>{e(C['id_card_ok'])}</b><em>· {e(C['id_card_both'])}</em></div>
      <div class="idc-row"><span>{e(C['id_card_cp'])}</span><span class="idc-blur">████████</span></div>
      <div class="idc-row"><span>{e(C['id_card_sum'])}</span><span class="idc-tag">{e(C['id_card_hidden'])}</span></div>
      <div class="idc-pts"><div><strong>+10</strong><span>{e(C['id_card_deal'])} · {e(C['id_card_pts'])}</span></div><div><strong>+15</strong><span>{e(C['id_card_hire'])} · {e(C['id_card_pts'])}</span></div></div>
      <div class="idc-bar"><i></i></div>
    </div>
  </div>
</section>

<section class="sec sec-line eco-sec" id="school">
  <div class="wrap eco-split">
    <div class="eco-txt">
      <p class="kicker" data-reveal><b></b>{e(C['sc_k'])}</p>
      <h2 class="display" data-words>{e(C['sc_h'])}</h2>
      <p class="eco-p" data-reveal>{e(C['sc_p'])}</p>
      <p class="eco-p eco-dim" data-reveal>{e(C['sc_cert'])} {e(C['sc_lang'])}</p>
      <div class="ctas" data-reveal>{ext_btn(L_SCHOOL, C['sc_cta'], C)}</div>
    </div>
    <ol class="eco-vis courses glass">{courses}</ol>
  </div>
</section>

<section class="sec sec-line eco-sec" id="psp">
  <div class="wrap eco-psp" data-reveal>
    <div><p class="kicker"><b></b>{e(C['psp_k'])}</p><h2 class="display">{e(C['psp_h'])}</h2></div>
    <p class="eco-p">{e(C['psp_p'])}</p>
    <a href="{h}#services" class="btn btn-lg btn-ghost magnetic" data-cursor="{e(C['more'])}"><span>{e(C['psp_cta'])}</span></a>
  </div>
</section>

<section class="cta-sec" id="contact">
  <div class="cta-glow" aria-hidden="true"></div>
  <div class="wrap cta">
    <h2 class="display cta-title" data-words>{e(C['end_h'])}</h2>
    <p class="sub" data-reveal>{e(C['end_p'])}</p>
    <div data-reveal><a href="{L_OWNER}" class="btn btn-xl magnetic" data-cursor="Telegram" target="_blank" rel="noopener"><span>{e(C['end_cta'])}</span></a></div>
  </div>
</section>
</main>
''' + chrome_bottom(lang, D, ver)
