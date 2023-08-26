from factory.grid_db import GridFsDatabase


class model(object):
    def __init__(self):
        self.db = GridFsDatabase()

    def insert(self, file_content, filename):
        res = self.db.insert(file_content, filename)
        return  res

    def getFile(self, filename): # find all
        return self.db.getFileContents(filename)

