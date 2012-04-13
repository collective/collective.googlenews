class FakeAcquisition(object):
    def __init__(self):
        self.aq_explicit = None

class FakeContext(object):

    def __init__(self):
        self.portal_type = 'News Item'
        self.id = "myid"
        self.title = "a title"
        self.description = "a description"
        self.creators = ["myself"]
        self.date="a date"
        self.aq_inner = FakeAcquisition()
        self.aq_inner.aq_explicit = self
        self._modified = "modified date"

    def _old_generateNewId(self):
        return 'a-title'

    def generateNewId(self, name=None, object=None):
        from collective.googlenews import digitid
        newid = digitid.generateNewId(self, name, object)
        return newid

    def getId(self):
        return self.id

    def Title(self):
        return self.title

    def Creators(self):
        return self.creators

    def Description(self):
        return self.description

    def Date(self):
        return self.date

    def modified(self):
        return self._modified

    def getPhysicalPath(self):
        return ('/','a','not','existing','path')

    def getFolderContents(self, filter=None):
        catalog = FakeCatalog()
        return catalog.searchResults()

    def absolute_url(self):
        return "http://nohost.com/"+self.id

    def queryCatalog(self, **kwargs): #fake Topic
        catalog = FakeCatalog()
        return catalog.searchResults()

    def getRemoteUrl(self): #fake Link
        return self.remoteUrl

    def modified(self): #for ram cache key
        return "a modification date"

class FakeBrain(object):
    def __init__(self):
        self.Title = ""
        self.Description = ""
        self.getId = ""
        self.EffectiveDate = ""
        self.Subject = []
        self.url = "http://myportal.com/"

    def getURL(self):
        return self.url

    def getObject(self):
        ob = FakeContext()
        ob.title = self.Title

        return ob

class FakeCatalog(object):
    def searchResults(self, **kwargs):
        brain1 = FakeBrain()
        brain1.Title = "My first news"
        brain1.Subject.append("keyword1")
        brain1.Subject.append("keyword2")
        brain1.EffectiveDate = "2010-04-05"
        brain1.url += "/my-first-news"
        brain2 = FakeBrain()
        brain2.Title = "A great news"
        brain2.Description = "you will drink lots of beer"
        brain2.Subject.append("keyword1")
        brain2.Subject.append("keyword3")
        brain2.EffectiveDate = "2011-04-05"
        brain2.url += "/a-great-news"
        return [brain1, brain2]

    def modified(self):
        return '654654654654'

class FakePlonePortalState(object):
    def __init__(self):
        self.portal_title = "portal title"
        self.lang = "fr"

    def language(self):
        return self.lang

class FakeDexterityContext(FakeContext):
    
    def __init__(self):
        self.portal_type = 'News Item'
        self.id = "myid"
        self.title = "a title"
        self.description = "a description"
        self.creators = ["myself"]
        self.date="a date"
        self.aq_inner = FakeAcquisition()
        self.aq_inner.aq_explicit = self
        self.context = self
        self._modified = "modified date"
    
    def _old_chooseName(self, name, object):
        return 'dex-title'
    