from factory.mongo_db import MongoDatabase


class model(object):
    def __init__(self):

        self.db = MongoDatabase()
        self.fields = {
            "clientName": "string",
            "clientId"  : "string",
            "fileName"  : "string",
            "fileId"    : "string",
            "activity"  : "int",
            "gridFs_id" : "string",
            "meta_data" : "file_metadata"
        }

    def create(self, req):
        res = self.db.insert(req)
        return  res

    def find(self, clientId): # find all
        return self.db.find(clientId)

    def search_on_field(self,field,value):
        return self.db.searchOnField(field,value)

    def get(self, filename):
        return self.db.getFileContents(filename)

    def update(self, id, todo):
        self.validator.validate(todo, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(id, todo,self.collection_name)

    def delete(self, id):
        return self.db.delete(id, self.collection_name)

