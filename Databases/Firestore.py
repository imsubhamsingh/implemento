import json

class Collection:
    def __init__(self, name):
        self.name = name
        self.data = {}

    def add_document(self, document_id, data):
        self.data[document_id] = data

    def get_document(self, document_id):
        return self.data.get(document_id)

class Database:
    def __init__(self):
        self.collections = {}

    def add_collection(self, collection_name):
        self.collections[collection_name] = Collection(collection_name)

    def get_collection(self, collection_name):
        return self.collections.get(collection_name)

    def persist(self):
        with open("db.json", "w") as f:
            collections_data = {}
            for collection_name, collection in self.collections.items():
                collections_data[collection_name] = collection.data
            json.dump(collections_data, f)

    def transact(self, callback):
        # Implement transaction mechanism here
        pass

db = Database()
users = db.add_collection("users")
users.add_document("user1", {"name": "John Doe", "age": 30})
print(users.get_document("user1")) # Output: {"name": "John Doe", "age": 30}
db.persist()

