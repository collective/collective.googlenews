import logging
from datetime import date
from zope import component
from Products.Five import BrowserView
from DateTime import DateTime
from plone.registry.interfaces import IRegistry
from collective.googlenews.interfaces import GoogleNewsSettings

logger = logging.getLogger('collective.googlenews')


class GoogleNewsSiteMap(BrowserView):
    """Google News sitemap view generate an xml file you can submit to google
    news services to have greater refresh news"""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.portal_state = None
        self.settings = None

    def __call__(self):
        self.update()
        return self.index()

    def update(self):
        if self.portal_state is None:
            self.portal_state = component.getMultiAdapter(
                (self.context, self.request), name="plone_portal_state"
            )
        if self.settings is None:
            registry = component.queryUtility(IRegistry, None)
            self.settings = registry.forInterface(GoogleNewsSettings)

    def news(self):
        constraints = self.get_query_constraints()
        brains = self.context.queryCatalog(**constraints)
        news = [
            self.brain2news(brain, name=self.portal_state.portal_title)
            for brain in brains
        ]
        return news

    def get_query_constraints(self):
        return {
            'sort_limit': 1000,
            'sort_on': 'effective',
            'sort_order': 'reverse',
            'effective': {'query': (DateTime() - 2, DateTime()),
                          'range': 'min:max'}
        }  # <1000 URLS and published in the last two days.

    def brain2news(self, brain, name=""):
        language = self.get_language(brain)
        publication_date = self.get_publication_date(brain)
        keywords = self.get_keywords(brain)
        genres = self.get_genres(brain)
        title = self.get_title(brain)
        url = self.get_url(brain)

        return {'loc': url,
                'name': name,
                'language': language,
                'access': '',
                'genres': genres,
                'publication_date': publication_date,
                'title': title,
                'keywords': keywords}

    def get_genres(self, brain):
        """Return a list of genres for a news brain
        each genre must be in
            * PressRelease
            * Satire
            * Blog
            * OpEd
            * Opinion
            * UserGenerated
        """
        return []

    def get_keywords(self, brain):
        """return a list of keywords
        please check the documentation at
        http://support.google.com/news/publisher/bin/answer.py?
            hl=en&answer=116037
        """
        raw_mapping = self.settings.keywords_mapping
        mapping = {}
        for row in raw_mapping:
            row_splited = row.split('|')
            if not len(row_splited) == 2:
                logger.info('not valid mapping: %s' % row)
                continue
            mapping[row_splited[0]] = row_splited[1]
        if mapping:
            keywords = []
            for keyword in brain.Subject:
                if keyword in mapping:
                    keywords.append(mapping[keyword])
        else:
            keywords = brain.Subject
        return ', '.join(keywords)

    def get_publication_date(self, brain):
        """return a formated date AAAA-MM-JJ
        http://support.google.com/news/publisher/bin/answer.py?
            hl=en&answer=74288
        """
        date_str = brain.EffectiveDate
        d = date(int(date_str[0:4]), int(date_str[5:7]), int(date_str[8:10]))
        return d

    def get_language(self, brain):
        """Return the language of the publication"""
        # language is not in metadata ... so lets take the global site language
        language = self.portal_state.language()
        if len(language) > 2 and language not in ('zh-cn', 'zh-tw'):
            language = language[0:2]
        return language

    def get_title(self, brain):
        return brain.Title

    def get_url(self, brain):
        """Return the url of the publication. override if you want to add
        statistics for example"""
        return brain.getURL()
