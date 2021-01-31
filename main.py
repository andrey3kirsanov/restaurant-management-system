
import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
import bson
from mongoengine import *
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'restaurant_management_system',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

class User(db.Document):
    _id = ObjectIdField(primary_key = True)
    name = db.StringField()
    email = db.StringField()
    def to_json(self):
        return {"_id": str(self._id),
                "name": self.name,
                "email": self.email}

@app.route('/users', methods=['GET'])
def query_users():
    users = User.objects
    if not users:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(users)

@app.route('/users/<id>', methods=['GET'])
def query_user(id):
    user = User.objects.get(_id=ObjectId(id))
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(user.to_json())

@app.route('/users', methods=['POST'])
def create_user():
    record = json.loads(request.data)
    user = User(_id=bson.objectid.ObjectId(),
                name=record['name'],
                email=record['email'])
    user.save()
    return jsonify(user.to_json())

@app.route('/users', methods=['PUT'])
def update_user():
    record = json.loads(request.data)
    user = User.objects.get(_id=ObjectId(record['_id']))
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.update(name=record['name'],
                    email=record['email'])
    user = User.objects.get(_id=ObjectId(record['_id']))
    return jsonify(user.to_json())

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.objects.get(_id=ObjectId(id))
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.delete()
    return jsonify(user.to_json())

if __name__ == "__main__":
    app.run(debug=True)