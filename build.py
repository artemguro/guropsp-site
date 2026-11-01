import os, re, shutil, html as H

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = ROOT + '/site'
tpl = open(ROOT + '/src/template.html', encoding='utf-8').read()

REDIRECT_EN = ("try{var L=localStorage.getItem('guro_lang');var ls=(navigator.languages&&navigator.languages.length?"
               "navigator.languages:[navigator.language||'']).join(',').toLowerCase();"
               "if(L==='ru'||(!L&&/(^|,)(ru|uk|be|kk)\\b/.test(ls))){location.replace('ru/'+location.search+location.hash);}}catch(e){}")

RU = dict(
 lang='ru', base='../', canonical='https://guropsp.com/ru/', lang_redirect='',
 lang_href='../', lang_set='en', lang_text='EN', lang_label='English version',
 title='Аудит платежей для iGaming: касса, PSP, роутинг и каскадинг | GURO PSP',
 desc='Повышаем проходимость депозитов в iGaming: аудит кассы и PSP, смарт-роутинг, каскадинг, работа с отказами. Tier 1: EU, CA, AU, NZ. Аудит от 600 €.',
 og_title='GURO PSP — больше успешных депозитов с тем же трафиком',
 og_desc='Аудит кассы, провайдеров, роутинга и каскадинга для iGaming-операторов. От диагностики до внедрения.',
 tg_msg='Здравствуйте! Хочу обсудить платёжный сетап (с сайта GuroPSP.com)', tg_ref='. Партнёр: ',
 logo_label='GURO PSP — на главную', nav_label='Разделы сайта',
 nav_check='Что проверяем', nav_services='Услуги', nav_process='Как работаем', nav_price='Стоимость',
 n_cash='Касса', n_router='Роутер', n_router_sub='BIN · гео', menu_open='Открыть меню', menu_close='Закрыть меню',
 cta_tg='Написать в Telegram', cta_discuss='Обсудить проект', cta_services='Смотреть услуги', cursor_view='Смотреть',
 kicker='Аудит и оптимизация платежей для iGaming',
 h1_1='Больше успешных', h1_2='депозитов', h1_3='с тем же трафиком',
 lead='Разбираем кассу, провайдеров, гейтвей, роутинг и каскадинг и находим, где теряются депозиты. Сопровождаем от диагностики до внедрения.',
 live_label='Демонстрация смарт-роутинга', live_title='Смарт-роутинг с каскадом', live_demo='демо',
 live_rate='Проходимость депозитов', live_note='Иллюстрация: отказ у одного провайдера уходит в каскад и проходит у другого.',
 f1='конверсия по игрокам', f3='лет операционного опыта в iGaming', f4='от аудита до внедрения',
 path_h='Проверяем путь депозита целиком',
 path_sub='От регистрационной формы до успешной транзакции. Депозиты теряются на любом шаге, поэтому смотрим каждый.',
 p1h='Регистрация', p1p='Форма и путь игрока до кассы',
 p2h='Касса', p2p='UX, методы по гео, суммы',
 p3h='Гейтвей', p3p='Настройки и функционал шлюза',
 p4h='Роутинг и каскад', p4p='Правила, BIN, коды отказов',
 p5h='Провайдеры', p5p='Цены, комиссии, надёжность',
 p6h='Успешный депозит', p6p='Аналитика и работа с ошибками',
 also='Отдельно смотрим:', also1='Цены и комиссии', also2='Пользовательский флоу', also3='Аналитику', also4='Работу с ошибками',
 svc_h='Что мы делаем', svc_sub='Берём отдельную задачу или закрываем платёжное направление комплексно.',
 g1='Сетап и аудит', g1s='Новый проект или действующий',
 g2='Аналитика и контроль', g2s='Видеть проблему раньше игроков',
 g3='Провайдеры и риски', g3s='Методы, переговоры, банки',
 s1h='Платёжный сетап с нуля или оптимизация текущего', s1p='Для новых проектов подбираем гейт, провайдеров и методы под гео и тип трафика, схема роутинга работает с первого дня. Для действующих пересобираем сетап без остановки приёма платежей.',
 s2h='Аудит кассы, гейтвея, роутинга и каскадинга', s2p='UX кассы, набор методов по гео, настройки гейта, правила роутинга и каскада, коды отказов. Отчёт с приоритетами и сопровождение внедрения.',
 s3h='ТЗ на доработку гейта и смарт-роутинг', s3p='Для in-house решений: sticky routing, каскад после 3DS, роутинг по BIN и банку-эмитенту, роутинг по кодам отказа. Помогаем принять доработку и настроить правила.',
 s4h='Кастомные дашборды аналитики', s4p='Проходимость по провайдерам, методам, гео, BIN и банкам, работа каскада, коды отказов, конверсия FTD. Встраиваются в ваш гейт или работают отдельно в браузере.',
 s5h='Смарт-алертинг в Slack или Telegram', s5p='Не просто уведомления о падении проходимости. Бот каждые 5 минут разбирает отказы по типам: технические сбои провайдера, проблемы кассы, блокировки антифрода, новые неизвестные ошибки. Отказы по конкретным игрокам уходят в саппорт, остальное платёжной команде. Повторы склеиваются, о восстановлении приходит отдельное сообщение, раз в сутки приходит сводка по AR.',
 s6h='Процессы работы с ошибками и эскалациями', s6p='Кто следит за проходимостью, как разбирать отказы, когда и с какой конкретикой эскалировать провайдеру или платформе, как фиксировать результат.',
 s7h='Поиск методов и переговоры о подключении', s7p='Определяем, каких методов не хватает кассе по ключевым гео, подбираем провайдеров и помогаем договориться об условиях.',
 s8h='Снижение платёжных рисков на сложных гео', s8p='Нидерланды, Великобритания, Франция: подбор провайдеров и методов под требования рынка, распределение трафика, резервные провайдеры, контроль чарджбэков.',
 s9h='Банковские счета C2B и B2C', s9p='Подбор банков и EMI под профиль бизнеса, подготовка к онбордингу и сопровождение процесса.',
 exp_h='Практики, а не теоретики',
 exp_p='Смотрим на платежи со стороны оператора. Не продаём оркестраторы и PSP: сравниваем варианты под вашу задачу, а выбор остаётся за вами.',
 tier23='Tier 2–3 по запросу',
 pr1h='Знаем рынок PSP', pr1p='Реальные цены методов и надёжных провайдеров. Учим получать лучшие условия.',
 pr2h='Лет операционного опыта в iGaming', pr2p='Сами настраивали кассы, роутинг и работу с отказами. Своя система смарт-роутинга работает уже в десятках проектов.',
 pr3h='Фокус на картах в Tier 1', pr3p='Там основная прибыль, сложности и риски. Прибыль максимизируем, риски минимизируем.',
 proc_h='Как работаем', proc_sub='Пять шагов от первого звонка до результата в цифрах.',
 st1h='Интро-звонок', st1p='Разбираемся в вашей ситуации и задачах',
 st2h='NDA и доступы', st2p='При необходимости подписываем NDA',
 st3h='Аудит', st3p='Находим и разбираем проблемы',
 st4h='Рекомендации', st4p='План изменений с приоритетами',
 st5h='Внедрение', st5p='Сопровождаем до результата',
 price_h='Цена под вашу задачу', price_sub='Зависит от глубины погружения в продукт (какие доступы готовы выдать) и регионов проверки.',
 pb1l='Первичный аудит, Tier 1', pb1v='от 600 €', pb1p='Аудит сайта, гейтвея и аналитики.',
 pb2l='Средний чек', pb2v='3 000–4 000 €', pb2p='Полный цикл оптимизации с сопровождением внедрения.',
 cta_h='Расскажите о вашем платёжном сетапе', cta_p='Гейт, касса, гео и основные проблемы. Ответим, с чего начать, и оценим объём работ.',
 foot='Аудит платежей, роутинг, аналитика',
 og_locale='ru_RU', og_locale_alt='en_US',
 faq_h='Частые вопросы', faq_sub='Коротко о том, как устроена работа и сколько она стоит.',
 q1='Что такое каскадинг платежей и зачем он нужен?',
 a1='Каскадинг — это повторная отправка отклонённой транзакции через другого провайдера по заданным правилам. Он спасает часть депозитов, которые иначе были бы потеряны из-за технических сбоев, отказов банка-эмитента или ограничений конкретного PSP. Настраивать его нужно по кодам отказа: не каждый отказ имеет смысл повторять.',
 q2='Как вы повышаете проходимость депозитов?',
 a2='Разбираем проходимость по провайдерам, методам, гео, BIN и банкам-эмитентам, находим слабые сегменты и меняем правила роутинга и каскада, набор методов в кассе и её UX. Изменения внедряем поэтапно и сравниваем результат с исходными цифрами.',
 q3='Сколько стоит аудит платежей?',
 a3='Первичный аудит сайта, гейтвея и аналитики по Tier 1 стоит от 600 €. Полный цикл оптимизации с сопровождением внедрения обычно обходится в 3 000–4 000 €. Итоговая цена зависит от глубины доступа к продукту и количества регионов.',
 q4='С какими гео вы работаете?',
 a4='Основная экспертиза — Tier 1: EU, Канада, Австралия и Новая Зеландия. Отдельно работаем со сложными рынками: Нидерланды, Великобритания, Франция. Tier 2–3 — по запросу.',
 q5='Вы продаёте PSP или платёжные оркестраторы?',
 a5='Нет. Мы смотрим на платежи со стороны оператора и сравниваем варианты под вашу задачу. Выбор провайдеров и решений остаётся за вами.',
 q6='Какие доступы нужны для аудита и подписываете ли вы NDA?',
 a6='Объём доступов определяем на интро-звонке: от просмотра кассы и аналитики до настроек гейта. При необходимости подписываем NDA до передачи любых данных.',
 svc_type='Консалтинг по платежам для iGaming',
)

EN = dict(
 lang='en', base='', canonical='https://guropsp.com/', lang_redirect=REDIRECT_EN,
 lang_href='ru/', lang_set='ru', lang_text='RU', lang_label='Русская версия',
 title='iGaming Payments Consulting: PSP Audit, Routing & Cascading | GURO PSP',
 desc='Raise deposit approval rates for iGaming: cashier and PSP audit, smart routing, cascading and decline handling. Tier 1: EU, CA, AU, NZ. Audits from €600.',
 og_title='GURO PSP — more successful deposits from the same traffic',
 og_desc='Cashier, PSP, routing and cascading audits for iGaming operators. From diagnostics to implementation.',
 tg_msg='Hi! I’d like to discuss our payment setup (via GuroPSP.com)', tg_ref='. Referred by: ',
 logo_label='GURO PSP — home', nav_label='Site sections',
 nav_check='What we check', nav_services='Services', nav_process='How we work', nav_price='Pricing',
 n_cash='Cashier', n_router='Router', n_router_sub='BIN · geo', menu_open='Open menu', menu_close='Close menu',
 cta_tg='Message us on Telegram', cta_discuss='Discuss your project', cta_services='See services', cursor_view='View',
 kicker='Payments audit and optimisation for iGaming',
 h1_1='More successful', h1_2='deposits from', h1_3='the same traffic',
 lead='We take apart your cashier, PSPs, gateway, routing and cascading to find where deposits are lost, and stay with you from diagnostics to implementation.',
 live_label='Smart routing demo', live_title='Smart routing with cascading', live_demo='demo',
 live_rate='Deposit approval rate', live_note='Illustration: a decline at one provider cascades and gets approved at another.',
 f1='player conversion', f3='years of iGaming operations', f4='from audit to implementation',
 path_h='We check the entire deposit path',
 path_sub='From the registration form to a successful transaction. Deposits can be lost at any step, so we check every one.',
 p1h='Registration', p1p='The form and the player’s path to the cashier',
 p2h='Cashier', p2p='UX, methods by geo, amounts',
 p3h='Gateway', p3p='Gateway settings and features',
 p4h='Routing and cascading', p4p='Rules, BINs, decline codes',
 p5h='Providers', p5p='Pricing, fees, reliability',
 p6h='Successful deposit', p6p='Analytics and error handling',
 also='We also review:', also1='Pricing and fees', also2='User flow', also3='Analytics', also4='Error handling',
 svc_h='What we do', svc_sub='We take on a single task or run your entire payments function end to end.',
 g1='Setup and audit', g1s='New or live project',
 g2='Analytics and monitoring', g2s='Spot problems before players do',
 g3='Providers and risk', g3s='Methods, negotiations, banks',
 s1h='Payment setup from scratch or optimising your current one', s1p='For new projects we select the gateway, providers and methods for your geos and traffic type, with routing in place from day one. For live projects we rebuild the setup without pausing payment acceptance.',
 s2h='Cashier, gateway, routing and cascading audit', s2p='Cashier UX, methods by geo, gateway settings, routing and cascade rules, decline codes. A prioritised report and support through implementation.',
 s3h='Gateway specs and smart routing', s3p='For in-house solutions: sticky routing, cascading after 3DS, routing by BIN and issuing bank, routing by decline code. We help you sign off the build and configure the rules.',
 s4h='Custom analytics dashboards', s4p='Approval rates by provider, method, geo, BIN and bank, cascade performance, decline codes, FTD conversion. Embedded in your gateway or running standalone in the browser.',
 s5h='Smart alerting in Slack or Telegram', s5p='More than approval-drop notifications. Every 5 minutes the bot sorts declines by type: provider outages, cashier issues, anti-fraud blocks, new unknown errors. Player-specific declines go to support, the rest to the payments team. Repeats are merged, recovery gets its own message, and a daily approval rate summary arrives every day.',
 s6h='Error handling and escalation processes', s6p='Who monitors approval rates, how to analyse declines, when and with what detail to escalate to a provider or platform, and how to record the outcome.',
 s7h='Sourcing methods and negotiating onboarding', s7p='We find which methods your cashier is missing in key geos, select providers and help negotiate terms.',
 s8h='Reducing payment risk in difficult geos', s8p='Netherlands, UK, France: providers and methods that meet market requirements, traffic distribution, backup providers, chargeback control.',
 s9h='C2B and B2C bank accounts', s9p='Selecting banks and EMIs for your business profile, preparing for onboarding and supporting you through it.',
 exp_h='Practitioners, not theorists',
 exp_p='We look at payments from the operator’s side. We don’t sell orchestrators or PSPs: we compare options for your task, and the choice stays with you.',
 tier23='Tier 2–3 on request',
 pr1h='We know the PSP market', pr1p='Real method pricing and reliable providers. We show you how to get the best terms.',
 pr2h='Years of iGaming operations experience', pr2p='We’ve set up cashiers, routing and decline handling ourselves. Our own smart routing system already runs in dozens of projects.',
 pr3h='Focus on cards in Tier 1', pr3p='That’s where most of the profit, complexity and risk sits. We maximise the profit and minimise the risk.',
 proc_h='How we work', proc_sub='Five steps from the first call to measurable results.',
 st1h='Intro call', st1p='We get to know your situation and goals',
 st2h='NDA and access', st2p='We sign an NDA if needed',
 st3h='Audit', st3p='We find and analyse the issues',
 st4h='Recommendations', st4p='A prioritised plan of changes',
 st5h='Implementation', st5p='We stay with you until the results are in',
 price_h='Pricing that fits your task', price_sub='Depends on how deep we go into the product (what access you can give us) and which regions we review.',
 pb1l='Initial audit, Tier 1', pb1v='from €600', pb1p='Website, gateway and analytics audit.',
 pb2l='Typical engagement', pb2v='€3,000–4,000', pb2p='Full optimisation cycle with implementation support.',
 cta_h='Tell us about your payment setup', cta_p='Gateway, cashier, geos and main issues. We’ll tell you where to start and estimate the scope.',
 foot='Payments audit, routing, analytics',
 og_locale='en_US', og_locale_alt='ru_RU',
 faq_h='Frequently asked questions', faq_sub='How the work is organised and what it costs.',
 q1='What is payment cascading and why does it matter?',
 a1='Cascading re-sends a declined transaction through another provider according to set rules. It recovers deposits that would otherwise be lost to technical failures, issuer declines or the limits of a single PSP. It should be tuned by decline code: not every decline is worth retrying.',
 q2='How do you increase deposit approval rates?',
 a2='We break approval rates down by provider, method, geo, BIN and issuing bank, find the weak segments and change routing and cascade rules, the cashier’s method set and its UX. Changes are rolled out step by step and measured against the baseline.',
 q3='How much does a payments audit cost?',
 a3='An initial audit of the website, gateway and analytics for Tier 1 starts at €600. A full optimisation cycle with implementation support typically costs €3,000–4,000. The final price depends on how much product access you can give and how many regions we review.',
 q4='Which geos do you work with?',
 a4='Our core expertise is Tier 1: EU, Canada, Australia and New Zealand. We also handle difficult markets such as the Netherlands, the UK and France. Tier 2–3 on request.',
 q5='Do you sell PSPs or payment orchestrators?',
 a5='No. We look at payments from the operator’s side and compare options for your task. The choice of providers and tools stays with you.',
 q6='What access do you need for an audit, and do you sign an NDA?',
 a6='We agree on the scope of access on the intro call: from viewing the cashier and analytics to gateway settings. We sign an NDA before any data is shared if needed.',
 svc_type='Payments consulting for iGaming',
)

RAW = {'lang_redirect', 'base', 'canonical', 'lang_href', 'jsonld', 'ver', 'u_audit', 'u_routing', 'u_blog'}
import sys; sys.path.insert(0, ROOT + '/src')
import services as SV
from services_content import AUDIT, ROUTING
for D in (RU, EN):
    pre = '/ru/' if D is RU else '/'
    D['u_audit'] = pre + 'services/payments-audit/'; D['u_routing'] = pre + 'services/routing-cascading/'
    D['u_blog'] = pre + 'blog/'; D['l_blog'] = 'Блог' if D is RU else 'Blog'
    D['l_audit'] = AUDIT[D['lang']]['crumb']; D['l_routing'] = ROUTING[D['lang']]['crumb']

import json, hashlib, glob, datetime
def jsonld(d):
    org = 'https://guropsp.com/#org'; site = 'https://guropsp.com/#website'; svc = d['canonical'] + '#service'
    services = [d['s%dh' % i] for i in range(1, 10)]
    g = [
        {'@type': 'Organization', '@id': org, 'name': 'GURO PSP', 'alternateName': 'GuroPSP', 'url': 'https://guropsp.com/',
         'logo': {'@type': 'ImageObject', 'url': 'https://guropsp.com/icon-512.png', 'width': 512, 'height': 512},
         'sameAs': ['https://t.me/GuroPSPbot'],
         'contactPoint': {'@type': 'ContactPoint', 'contactType': 'sales', 'url': 'https://t.me/GuroPSPbot', 'availableLanguage': ['English', 'Russian']}},
        {'@type': 'WebSite', '@id': site, 'url': 'https://guropsp.com/', 'name': 'GURO PSP', 'alternateName': 'GuroPSP', 'publisher': {'@id': org}, 'inLanguage': ['en', 'ru']},
        {'@type': 'WebPage', '@id': d['canonical'] + '#webpage', 'url': d['canonical'], 'name': d['title'], 'description': d['desc'],
         'inLanguage': d['lang'], 'isPartOf': {'@id': site}, 'about': {'@id': svc}, 'primaryImageOfPage': 'https://guropsp.com/og-%s.jpg' % d['lang']},
        {'@type': 'Service', '@id': svc, 'name': d['og_title'], 'serviceType': d['svc_type'], 'description': d['desc'], 'provider': {'@id': org},
         'areaServed': [{'@type': 'Place', 'name': n} for n in ['European Union', 'United Kingdom', 'Canada', 'Australia', 'New Zealand']],
         'offers': [{'@type': 'Offer', 'name': d['pb1l'], 'priceCurrency': 'EUR', 'priceSpecification': {'@type': 'PriceSpecification', 'minPrice': 600, 'priceCurrency': 'EUR'}},
                    {'@type': 'Offer', 'name': d['pb2l'], 'priceCurrency': 'EUR', 'priceSpecification': {'@type': 'PriceSpecification', 'minPrice': 3000, 'maxPrice': 4000, 'priceCurrency': 'EUR'}}],
         'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': d['svc_h'], 'itemListElement': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n}} for n in services]}},
        {'@type': 'FAQPage', '@id': d['canonical'] + '#faq', 'mainEntity': [{'@type': 'Question', 'name': d['q%d' % i], 'acceptedAnswer': {'@type': 'Answer', 'text': d['a%d' % i]}} for i in range(1, 7)]},
    ]
    return json.dumps({'@context': 'https://schema.org', '@graph': g}, ensure_ascii=False).replace('</', '<\\/')

def render(d):
    def sub(m):
        k = m.group(1)
        assert k in d, 'missing key ' + k
        return d[k] if k in RAW else H.escape(d[k], quote=True)
    out = re.sub(r'\{\{(\w+)\}\}', sub, tpl)
    assert '{{' not in out
    return out

h = hashlib.sha1()
for f in sorted(glob.glob(ROOT + '/src/assets/*')) + [ROOT + '/src/template.html', ROOT + '/src/services.py', ROOT + '/src/services_content.py', ROOT + '/src/blog.py', ROOT + '/src/blog_content.py', ROOT + '/src/blog_articles.py', ROOT + '/src/layout.py']: h.update(open(f, 'rb').read())
VER = h.hexdigest()[:8]
assert set(RU) == set(EN), set(RU) ^ set(EN)
for D in (RU, EN): D['ver'] = VER; D['jsonld'] = jsonld(D)
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT + '/ru'); os.makedirs(OUT + '/assets')
open(OUT + '/index.html', 'w', encoding='utf-8').write(render(EN))
open(OUT + '/ru/index.html', 'w', encoding='utf-8').write(render(RU))
SVC_URLS = []
for P in SV.PAGES:
    for D in (EN, RU):
        d = OUT + ('/ru' if D is RU else '') + '/services/' + P['slug']
        os.makedirs(d, exist_ok=True)
        open(d + '/index.html', 'w', encoding='utf-8').write(SV.render(P, D['lang'], D, VER))
    SV_alt = (SV.page_url(P, 'en'), SV.page_url(P, 'ru'))
    SVC_URLS += [(SV_alt[0], SV_alt), (SV_alt[1], SV_alt)]
for f in ['site.css', 'site.js', 'hero.js']:
    shutil.copy(ROOT + '/src/assets/' + f, OUT + '/assets/' + f)
for f in ['gsap.min.js', 'ScrollTrigger.min.js', 'three.min.js']:  # vendored libs (three.min.js already patched)
    shutil.copy(ROOT + '/src/vendor/' + f, OUT + '/assets/' + f)
for f in glob.glob(ROOT + '/src/static/*'): shutil.copy(f, OUT + '/' + os.path.basename(f))
today = datetime.date.today().isoformat()
open(OUT + '/robots.txt', 'w').write('User-agent: *\nAllow: /\nDisallow: /tg/\n\nSitemap: https://guropsp.com/sitemap.xml\n')
import blog as BL
INDEXNOW_KEY = '5f3c9e2a7b1d4c8e9a6f0b2d3c4e5f61'
for D in (EN, RU):
    pre = OUT + ('/ru' if D is RU else '')
    os.makedirs(pre + '/blog', exist_ok=True)
    open(pre + '/blog/index.html', 'w', encoding='utf-8').write(BL.render_hub(D['lang'], D, VER))
    open(pre + '/blog/feed.xml', 'w', encoding='utf-8').write(BL.render_rss(D['lang']))
    for A in BL.ARTICLES:
        os.makedirs(pre + '/blog/' + A['slug'], exist_ok=True)
        open(pre + '/blog/' + A['slug'] + '/index.html', 'w', encoding='utf-8').write(BL.render_article(A, D['lang'], D, VER))
BLOG_URLS = [(BL.hub_url(l), (BL.hub_url('en'), BL.hub_url('ru'))) for l in ('en', 'ru')]
for A in BL.ARTICLES:
    BLOG_URLS += [(BL.art_url(A, l), (BL.art_url(A, 'en'), BL.art_url(A, 'ru')), A['updated']) for l in ('en', 'ru')]
open(OUT + '/' + INDEXNOW_KEY + '.txt', 'w').write(INDEXNOW_KEY)
open(OUT + '/404.html', 'w', encoding='utf-8').write(open(ROOT + '/src/404.html', encoding='utf-8').read().replace('{{ver}}', VER))
altx = lambda en, ru: '<xhtml:link rel="alternate" hreflang="en" href="%s"/><xhtml:link rel="alternate" hreflang="ru" href="%s"/><xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % (en, ru, en)
URLS = [(u, ('https://guropsp.com/', 'https://guropsp.com/ru/')) for u in ['https://guropsp.com/', 'https://guropsp.com/ru/']] + SVC_URLS + BLOG_URLS
open(OUT + '/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + ''.join('  <url><loc>%s</loc><lastmod>%s</lastmod>%s</url>\n' % (x[0], x[2] if len(x) > 2 else today, altx(*x[1])) for x in URLS)
    + '</urlset>\n')
open(OUT + '/.htaccess', 'w').write('''# GURO PSP
Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html
<IfModule mod_headers.c>
  <FilesMatch "\\.(css|js)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>
  <FilesMatch "\\.(png|jpg|svg|ico|webmanifest)$">
    Header set Cache-Control "public, max-age=604800"
  </FilesMatch>
  <FilesMatch "\\.(html|xml|txt)$">
    Header set Cache-Control "public, max-age=300"
  </FilesMatch>
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
''')
en_txt = open(OUT + '/index.html', encoding='utf-8').read() + ''.join(open(OUT + '/services/' + P['slug'] + '/index.html', encoding='utf-8').read() for P in SV.PAGES)
print('Cyrillic in EN:', sorted(set(re.findall(r'[А-Яа-яЁё]+', en_txt))))
open(OUT + '/VERSION', 'w').write(VER + '-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d%H%M%S') + '\n')
print('built')
