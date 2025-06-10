from pymongo import MongoClient

# Wrapper object for interacting with database
class MongoWrapper:
    def __init__(self, uri):
        self.client = MongoClient(uri)

    def getDatabase(self, dbName):
        db = self.client[dbName]
        return db

    def getCollection(self, dbName, colName):
        col = self.getDatabase(dbName)[colName]
        return col

    # Insert a single document into the specified collection in the specified collection
    # The dict that is passed in will have an ObjectID added to it
    def insertDocument(self, dbName, colName, jsonObj):
        return self.getCollection(dbName, colName).insert_one(jsonObj)

    # Find a singe document in the specified collection in the specified collection
    # Returns with a the first matching document
    # A document is a match if all keys:value pairs in the query dict are present and match
    def findDocument(self, dbName, colName, jsonObj={}):
        return self.getCollection(dbName, colName).find_one(jsonObj)

    # Find all documents in the specified collection in the specified collection
    # Returns with an iterable containing matching documents
    # A document is a match if all keys:value pairs in the query dict are present and match
    def searchDocument(self, dbName, colName, jsonObj={}):
        return self.getCollection(dbName, colName).find(jsonObj)

    # Update a singe document in the specified collection in the specified collection
    # Updates with a the first matching document
    # A document is a match if all keys:value pairs in the query dict are present and match
    # All key:value pairs in the values dict will be added or override those in the document
    def updateDocument(self, dbName, colName, valuesToSet, jsonObj={}):
        update_operation = {"$set": valuesToSet}
        return self.getCollection(dbName, colName).update_one(jsonObj, update_operation)

    # Finds a item based on a sorting field
    def findDocumentSorted(self, dbName, colName, jsonObj={}, sort_field=None):
        return self.getCollection(dbName, colName).find_one(jsonObj, sort=[sort_field])

