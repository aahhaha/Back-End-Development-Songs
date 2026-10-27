"""MongoDB-backed Songs REST API."""
import json
import os
from pathlib import Path
from urllib.parse import quote_plus
from flask import abort, jsonify, request
from pymongo import MongoClient
from . import app

host = os.environ.get('MONGODB_SERVICE', 'localhost')
port = int(os.environ.get('MONGODB_PORT', '27017'))
user = os.environ.get('MONGODB_USERNAME')
password = os.environ.get('MONGODB_PASSWORD')
auth = f'{quote_plus(user)}:{quote_plus(password)}@' if user and password else ''
client = MongoClient(f'mongodb://{auth}{host}:{port}', serverSelectionTimeoutMS=5000)
collection = client.songs.songs

def seed_database():
    collection.create_index('id', unique=True)
    if collection.count_documents({}) == 0:
        with (Path(__file__).parent / 'data' / 'songs.json').open(encoding='utf-8') as source:
            collection.insert_many(json.load(source))

@app.get('/health')
def health():
    client.admin.command('ping')
    return jsonify(status='OK'), 200

@app.get('/count')
def count():
    return jsonify(length=collection.count_documents({})), 200

@app.get('/song')
def get_songs():
    return jsonify(songs=list(collection.find({}, {'_id': 0}))), 200

@app.get('/song/<int:id>')
def get_song(id):
    song = collection.find_one({'id': id}, {'_id': 0})
    if song is None:
        abort(404)
    return jsonify(song), 200

@app.post('/song')
def create_song():
    song = request.get_json()
    if not isinstance(song, dict) or not isinstance(song.get('id'), int):
        abort(400)
    if collection.find_one({'id': song['id']}):
        return jsonify(Message=f"song with id {song['id']} already present"), 302
    collection.insert_one(dict(song))
    return jsonify(song), 201

@app.put('/song/<int:id>')
def update_song(id):
    song = request.get_json()
    if not isinstance(song, dict) or song.get('id', id) != id:
        abort(400)
    song.pop('_id', None)
    result = collection.update_one({'id': id}, {'$set': song})
    if not result.matched_count:
        abort(404)
    return jsonify(collection.find_one({'id': id}, {'_id': 0})), 201

@app.delete('/song/<int:id>')
def delete_song(id):
    if not collection.delete_one({'id': id}).deleted_count:
        abort(404)
    return '', 204

@app.cli.command('seed')
def seed():
    seed_database()
    print('Songs database initialized.')
