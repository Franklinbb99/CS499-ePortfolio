# Example Python Code to Insert a Document 

from pymongo import MongoClient 
from bson.objectid import ObjectId 

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """ 

    def __init__(self, username, password):

        HOST = 'localhost'
        PORT = 27017
        DB = 'aac'
        COL = 'animals'

        self.client = MongoClient(f'mongodb://{username}:{password}@{HOST}:{PORT}')
        self.database = self.client[DB]
        self.collection = self.database[COL]

    # Create a method to return the next available record number for use in the create method
            
    # Complete this create method to implement the C in CRUD. 
    def create(self, data):
        try:
            if data is not None:
                self.collection.insert_one(data)
                return True
            else:
                return False
        except Exception as e:
            print("Create failed:", e)
            return False 

    # Create method to implement the R in CRUD.
    def read(self, query):
        try:
            if query is not None:
                cursor = self.collection.find(query)
                return list(cursor)
            else:
                return []
        except Exception as e:
            print("Read failed:", e)
            return []
         
    # Update method to implement the U in CRUD.
    def update(self, query, new_values):
        try:
            if query is not None and new_values is not None:
                result = self.collection.update_many(query, new_values)
                return result.modified_count
            else:
                return 0
        except Exception as e:
            print("Update failed:", e)
            return 0

    # Delete method to implement the D in CRUD.
    def delete(self, query):
        try:
            if query is not None:
                result = self.collection.delete_many(query)
                return result.deleted_count
            else:
                return 0
        except Exception as e:
            print("Delete failed:", e)
            return 0