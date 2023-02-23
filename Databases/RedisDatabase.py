import pickle
import os

class RedisDatabase:
    def __init__(self):
        self.data = {}
        self.transaction_stack = []

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def mset(self, mapping):
        self.data.update(mapping)

    def mget(self, keys):
        return [self.data.get(key) for key in keys]

    def incr(self, key):
        self.data[key] = self.data.get(key, 0) + 1
        return self.data[key]

    def decr(self, key):
        self.data[key] = self.data.get(key, 0) - 1
        return self.data[key]

    def delete(self, key):
        del self.data[key]

    def keys(self):
        return list(self.data.keys())

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
        with open('redis.pickle', 'wb') as f:
            pickle.dump(self.data, f)

    def load(self):
        if os.path.exists('redis.pickle'):
            with open('redis.pickle', 'rb') as f:
                self.data = pickle.load(f)

