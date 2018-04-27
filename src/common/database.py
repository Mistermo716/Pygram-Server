import pymongo
import os
from .keys import Key

# Mongolab uri set in heroku with dyno


class Database(object):
    URI = Key
    DATABASE = None

    @staticmethod  # static method to access URI and Database of class
    def initialize():
        # static URI accessed through class
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['heroku_bzlbb14n']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_all(collection):
        return Database.DATABASE[collection].find({})

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
