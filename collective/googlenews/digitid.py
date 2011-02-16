import random

def generateNewId(self):
    newid = self._old_generateNewId()
    if getattr(self,'portal_type') == 'News Item':
        if newid is not None:
            newid += str(random.randint(100, 9999))
    return newid
