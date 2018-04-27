import pymongo
import os


class Database(object):
    URI = os.environ.get("MONGOLAB_URI")
    DATABASE = None

    @staticmethod  # static method to access URI and Database of class
    def initialize():
        # static URI accessed through class
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

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
