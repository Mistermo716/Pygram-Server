import uuid
import datetime
from common.database import Database


class Comment(object):
    def __init__(self, photo_id, content, username, date=datetime.datetime.utcnow(), id=None):
        self.content = content
        self.username = username
        self.photo_id = photo_id
        # generate new id random hex else get the id passed in
        self.id = uuid.uuid4().hex if id is None else id
        self.date = date

    def save_to_mongo(self):
        # pass self into database class
        # which contains the jsonified data from function below
        Database.insert(collection='comments', data=self.json())

    def json(self):
        return {
            'id': self.id,
            'photo_id': self.photo_id,
            'content': self.content,
            'username': self.username,
            'date': self.date
        }

    def from_blog(self):
        return [comment for comment in Database.find(collection='comments', query={'photo_id': self.photo_id})]

    @classmethod
    def from_mongo(cls, id):
        comment_data = Database.find_one(
            collection='comments', query={'id': id})
        return cls(**comment_data)
