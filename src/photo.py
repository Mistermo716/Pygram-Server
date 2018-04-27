import uuid
import datetime
from common.database import Database
from comments import Comment


class Photo(object):
    def __init__(self, username, url, description, date=datetime.datetime.utcnow(),  id=None):
        self.username = username
        self.url = url
        self.date = date
        self.description = description
        self.id = uuid.uuid4().hex if id is None else id

    def new_comment(self, username, content, date=datetime.datetime.utcnow()):
        comment = Comment(photo_id=self.id,
                          content=content,
                          username=self.username,
                          date=date)
        comment.save_to_mongo()

    def get_posts(self):
        return Comment.from_blog(self.id)

    @staticmethod
    def find_in_mongo():
        return [photo for photo in Database.find_all(collection='photos')]

    def save_to_mongo(self):
        Database.insert(collection='photos', data=self.json())
        return self.json()

    def json(self):
        return {
            'username': self.username,
            'url': self.url,
            'description': self.description,
            'id': self.id,
            'date': self.date
        }

    @classmethod
    def from_mongo(cls, id):
        photo_data = Database.find_one(collection='photos',
                                       query={'id': id})
        return cls(**photo_data)
