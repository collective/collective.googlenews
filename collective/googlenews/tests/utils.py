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

    def generateNewId(self):
        from collective.googlenews import digitid
        newid = digitid.generateNewId(self)
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
