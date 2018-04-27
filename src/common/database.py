import pymongo
import os

# Mongolab uri set in heroku with dyno


class Database(object):
    URI = 'mongodb://test1234:test1234@ds261429.mlab.com:61429/heroku_bzlbb14n'
    DATABASE = None

    @staticmethod  # static method to access URI and Database of class
    def initialize():
        # static URI accessed through class
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client.get_database('heroku_bzlbb14n')

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
