import json
import os

class MySQL:
    def __init__(self):
        self.tables = {}
        self.transaction_stack = []

    def create_table(self, table_name, columns):
        self.tables[table_name] = {'columns': columns, 'data': []}

    def insert(self, table_name, values):
        table = self.tables[table_name]
        if len(values) != len(table['columns']):
            raise ValueError("Invalid number of values")
        table['data'].append(values)

    def select(self, table_name, columns, where=None):
        table = self.tables[table_name]
        result = []
        for row in table['data']:
            if where is None or where(row):
                result.append([row[table['columns'].index(col)] for col in columns])
        return result

    def update(self, table_name, values, where=None):
        table = self.tables[table_name]
        for i, row in enumerate(table['data']):
            if where is None or where(row):
                for col, val in values.items():
                    row[table['columns'].index(col)] = val

    def delete(self, table_name, where=None):
        table = self.tables[table_name]
        table['data'] = [row for row in table['data'] if not where or not where(row)]

    def begin(self):
        self.transaction_stack.append(self.tables.copy())

    def rollback(self):
        if not self.transaction_stack:
            return False
        self.tables = self.transaction_stack.pop()
        return True

    def commit(self):
        self.transaction_stack.clear()

    def save(self):
        with open('mysql.json', 'w') as f:
            json.dump(self.tables, f)

    def load(self):
        if os.path.exists('mysql.json'):
            with open('mysql.json', 'r') as f:
                self.tables = json.load(f)

