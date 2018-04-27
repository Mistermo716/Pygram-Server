from server.src.common.database import Database
from server.src.models.photo import Photo
from flask import session
import datetime
import uuid


class User(object):
    def __init__(self, username, password, _id=None):
        self.username = username
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_username(cls, username):
        data = Database.find_one('users', {'username': username})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one('users', {'_id': _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(username, password):
        user = User.get_by_username(username)
        if user is not None:
            return user.password == password
        return False

    @classmethod
    def register(cls, username, password):
        user = cls.get_by_username(username)
        if user is None:
            # user does not exist create it
            new_user = cls(username, password)
            new_user.save_to_mongo()
            session['username'] = username
            return True
        else:
            return False

    @staticmethod
    def login(username):
        session['username'] = username

    @staticmethod
    def logout():
        session['username'] = None

    def get_photos(self):
        return Photo.find_by_author_id(self._id)

    def new_photo(self, url, content):
        photo = Photo(author=self.username,
                      url=url,
                      content=content,
                      author_id=self._id)
        photo.save_to_mongo()

    @staticmethod
    def new_comment(photo_id, content, date=datetime.datetime.utcnow()):
        photo = Photo.from_mongo(photo_id)
        photo.new_comment(content=content,
                          date=date)

    def json(self):
        return {
            "username": self.username,
            "_id": self._id,
            "password": self.password
        }

    def save_to_mongo(self):
        Database.insert('users', self.json())
