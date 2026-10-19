# Example Python Code to Insert a Document

from pymongo import MongoClient
from bson.objectid import ObjectId


class AnimalShelter(object):
    """CRUD operations for Animal collection in MongoDB."""

    def __init__(self, username, password):

        HOST = 'localhost'
        PORT = 27017
        DB = 'aac'
        COL = 'animals'

        self.client = MongoClient(f'mongodb://{username}:{password}@{HOST}:{PORT}')
        self.database = self.client[DB]
        self.collection = self.database[COL]

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

    # Read method to implement the R in CRUD.
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

    # Enhanced search method for finding animals by type and/or breed.
    def search_animals(self, animal_type=None, breed=None):
        query = {}

        if animal_type:
            query["animal_type"] = {"$regex": f"^{animal_type}$", "$options": "i"}

        if breed:
            query["breed"] = {"$regex": breed, "$options": "i"}

        return self.read(query)

    # Enhanced search method for finding animals within an age range.
    # The database stores age_upon_outcome as text such as "2 years"
    # or "6 months", so the values are converted to years for comparison.
    def search_by_age(self, min_age=None, max_age=None):
        animals = self.read({})
        results = []

        for animal in animals:
            age_text = animal.get("age_upon_outcome")

            if not age_text:
                continue

            parts = str(age_text).lower().split()

            try:
                value = float(parts[0])
            except (ValueError, IndexError):
                continue

            unit = parts[1] if len(parts) > 1 else "years"

            if "month" in unit:
                age_years = value / 12
            elif "week" in unit:
                age_years = value / 52
            elif "day" in unit:
                age_years = value / 365
            else:
                age_years = value

            if min_age is not None and age_years < min_age:
                continue

            if max_age is not None and age_years > max_age:
                continue

            results.append(animal)

        return results

    # Enhanced combined search for animal type, breed, and age range.
    def search_animals_advanced(self, animal_type=None, breed=None,
                                min_age=None, max_age=None):
        results = self.search_animals(animal_type, breed)

        if min_age is None and max_age is None:
            return results

        filtered_results = []

        for animal in results:
            age_text = animal.get("age_upon_outcome")

            if not age_text:
                continue

            parts = str(age_text).lower().split()

            try:
                value = float(parts[0])
            except (ValueError, IndexError):
                continue

            unit = parts[1] if len(parts) > 1 else "years"

            if "month" in unit:
                age_years = value / 12
            elif "week" in unit:
                age_years = value / 52
            elif "day" in unit:
                age_years = value / 365
            else:
                age_years = value

            if min_age is not None and age_years < min_age:
                continue

            if max_age is not None and age_years > max_age:
                continue

            filtered_results.append(animal)

        return filtered_results

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
