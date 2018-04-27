from flask import Flask, request, jsonify
from bson import json_util, ObjectId
from flask_cors import CORS
import os
import json
from common.database import Database
from comments import Comment
from photo import Photo

app = Flask(__name__)
CORS(app)


@app.before_first_request
def initialize_database():
    Database.initialize()

# get all photos


@app.route('/photos')
def get_photos():
    newArr = []
    item = {}
    photos = Photo.find_in_mongo()
    for photo in photos:
        for key in photo:
            if key != '_id':
                item[key] = photo[key]
        if len(newArr) < len(photos):
            newArr.append(item)
        item = {}

    return jsonify(newArr)


@app.route('/photos/new', methods=['POST'])
def create_new_photo():
    user = request.json['username']
    description = request.json['description']
    url = request.json['url']

    photo = Photo(user, url, description)
    photo = photo.save_to_mongo()
    return jsonify(photo)


@app.route('/comments', methods=['POST', 'GET'])
def get_comments():
    photo_id = request['photo_id']
    item = {}
    newArr = []
    photo = Photo.from_mongo(photo_id)
    comments = photo.from_blog(photo_id)
    for comment in comments:
        for key in photo:
            if key != '_id':
                item[key] = comment[key]
        if len(newArr) < len(comments):
            newArr.append(item)
        item = {}

    return jsonify(newArr)


@app.route('/comments/new', methods=['POST'])
def create_new_comment():
    photo_id = request.json['photo_id']
    content = request.json['content']
    user = request.json['user']

    new_comment = Comment(photo_id=photo_id, content=content, username=user)
    new_comment.save_to_mongo()

    return jsonify(get_comments(photo_id))


if __name__ == "__main__":
    try:
        app.run(host=os.environ.get('IP', ''),
                port=int(os.environ.get('PORT', '8080')))
    except:
        raise
