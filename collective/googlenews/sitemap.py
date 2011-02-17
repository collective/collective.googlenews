from datetime import date
from zope import component
from Products.Five import BrowserView
from DateTime import DateTime

class GoogleNewsSiteMap(BrowserView):
    """Google News sitemap view generate an xml file you can submit to google
    news services to have greater refresh news"""
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.state = component.getMultiAdapter((self.context, self.request),
                                               name="plone_portal_state")

    def news(self):
        constraints = {'sort_limit':1000,
                      'sort_on':'effective', 'sort_order':'reverse',
                      'effective': {'query': (DateTime()-2, DateTime()),
                                    'range': 'min:max'}
                      } #<1000 URLS and published in the last two days.
        brains = self.context.queryCatalog(**constraints)
        news = [self.brain2news(brain, name=self.state.portal_title) \
                for brain in brains]
        return news

    def brain2news(self, brain, name=""):
        #get language and check googlenews language constraints
        language = self.state.language()
        if len(language)>2 and language not in ('zh-cn', 'zh-tw'):
            language = language[0:2]
        #date format must be AAAA-MM-JJ
        date_str = brain.EffectiveDate
        d = date(int(date_str[0:4]), int(date_str[5:7]), int(date_str[8:10]))
        keywords = ','.join(brain.Subject)
        return {'loc':brain.getURL(),
                'name':name,
                'language':language,
                'access':'',
                'genres':'', #must be in PressRelease,Satire,Blog,OpEd,Opinion,UserGenerated
                'publication_date':d,
                'title':brain.Title,
                'keywords':keywords}
