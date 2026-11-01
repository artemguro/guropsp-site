# Blog articles. Block types: ('h2', id, text) ('p', text) ('ul', [items]) ('ol', [items]) ('table', cols, rows) ('note', text) ('cta', service_slug)
# Inline markup allowed in text: **bold** only.

from blog_articles import ARTICLES  # noqa: F401  (all article content lives in blog_articles.py)

BLOG_UI = {
 'ru': dict(h1='Блог о платежах в iGaming', sub='Практические разборы проходимости, роутинга, каскада и работы с провайдерами — из опыта операционной работы.',
            seo_title='Блог о платежах в iGaming: проходимость, роутинг, каскад | GURO PSP',
            desc='Статьи GURO PSP о платежах в iGaming: как повысить проходимость депозитов, настроить роутинг и каскадинг, работать с кодами отказа и провайдерами.',
            crumb='Блог', toc='Содержание', read='Читать', updated='Обновлено', faq='Коротко', related='Услуга по теме', more='Подробнее об услуге',
            cta_box='Нужна помощь с этим?', back='Все статьи', other='Ещё по теме', published='Опубликовано'),
 'en': dict(h1='iGaming payments blog', sub='Practical breakdowns of approval rates, routing, cascading and provider management — from hands-on operations experience.',
            seo_title='iGaming Payments Blog: Approval Rates, Routing, Cascading | GURO PSP',
            desc='GURO PSP articles on iGaming payments: how to improve deposit approval rates, set up routing and cascading, handle decline codes and manage providers.',
            crumb='Blog', toc='Contents', read='Read', updated='Updated', faq='In short', related='Related service', more='Learn about the service',
            cta_box='Need help with this?', back='All articles', other='More on this topic', published='Published'),
}
