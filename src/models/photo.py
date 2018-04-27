import uuid
import datetime
from server.src.common.database import Database
from server.src.models.comments import Comment


class Photo(object):
    def __init__(self, author, url, description, author_id, _id=None):
        self.author = author
        self.url = url
        self.author_id = author_id
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_comment(self, author, content, date=datetime.datetime.utcnow()):
        comment = Comment(photo_id=self._id,
                          content=content,
                          author=self.author,
                          date=date)
        comment.save_to_mongo()

    def get_posts(self):
        return Comment.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection='photos', data=self.json())

    def json(self):
        return {
            'author': self.author,
            'author_id': self.author_id
            'description': self.description,
            '_id': self._id
        }

    @classmethod
    def from_mongo(cls, id):
        photo_data = Database.find_one(collection='photos',
                                       query={'_id': id})
        return cls(**photo_data)

    @classmethod
    def find_by_author_id(cls, author_id):
        photos = Database.find(collection='photos', query={
            'author_id': author_id})
        return [cls(**photo) for photo in photos]
