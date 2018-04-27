import uuid
from server.src.common.database import Database
import datetime


class Comment(object):
    def __init__(self, photo_id, content, author, date=datetime.datetime.utcnow(), _id=None):
        self.content = content
        self.author = author
        self.photo_id = photo_id
        # generate new id random hex else get the id passed in
        self._id = uuid.uuid4().hex if _id is None else _id
        self.date = date

    def save_to_mongo(self):
        # pass self into database class
        # which contains the jsonified data from function below
        Database.insert(collection='comments', data=self.json())

    def json(self):
        return {
            '_id': self._id,
            'photo_id': self.photo_id,
            'content': self.content,
            'author': self.author,
            'date': self.date
        }

    @classmethod
    def from_mongo(cls, id):
        comment_data = Database.find_one(
            collection='comments', query={'_id': id})
        return cls(**comment_data)

    @staticmethod
    def from_blog(id):
        return [comment for comment in Database.find(collection='comments', query={'photo_id': id})]
