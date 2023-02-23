import json
import os

class DynamoDB:
    def __init__(self):
        self.data = {}
        self.transaction_stack = []

    def put_item(self, table, item):
        if table not in self.data:
            self.data[table] = {}
        self.data[table][item['PK']] = item

    def get_item(self, table, primary_key):
        if table not in self.data:
            return {}
        return self.data[table].get(primary_key, {})

    def update_item(self, table, primary_key, updates):
        item = self.data[table][primary_key]
        item.update(updates)

    def delete_item(self, table, primary_key):
        del self.data[table][primary_key]

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
        with open('dynamodb.json', 'w') as f:
            json.dump(self.data, f)

    def load(self):
        if os.path.exists('dynamodb.json'):
            with open('dynamodb.json', 'r') as f:
                self.data = json.load(f)

