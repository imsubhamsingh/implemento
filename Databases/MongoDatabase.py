import pickle
import os

class MongoDB:
    def __init__(self):
        self.data = {}
        self.transaction_stack = []

    def insert(self, collection, document):
        if collection not in self.data:
            self.data[collection] = []
        self.data[collection].append(document)

    def find(self, collection, query={}):
        if collection not in self.data:
            return []
        result = []
        for document in self.data[collection]:
            match = True
            for key, value in query.items():
                if document.get(key) != value:
                    match = False
                    break
            if match:
                result.append(document)
        return result

    def update(self, collection, query, update):
        for i, document in enumerate(self.data[collection]):
            match = True
            for key, value in query.items():
                if document.get(key) != value:
                    match = False
                    break
            if match:
                self.data[collection][i].update(update)

    def delete(self, collection, query={}):
        self.data[collection] = [document for document in self.data[collection] if not all(document.get(key) == value for key, value in query.items())]

    def begin(self):
        self.transaction_stack.append(self.data.copy())

    def rollback(self):
        if not self.transaction_stack:
            return False
        self.data = self.transaction_stack.pop()
        return True

    def commit(self):
        self.transaction_stack.clear()

    def save(self):
        with open('mongodb.pickle', 'wb') as f:
            pickle.dump(self.data, f)

    def load(self):
        if os.path.exists('mongodb.pickle'):
            with open('mongodb.pickle', 'rb') as f:
                self.data = pickle.load(f)

