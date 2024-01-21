from flask import Flask
from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
flask_app = os.getenv('FLASK_APP')
flask_env = os.getenv('FLASK_ENV')
database_uri = os.getenv('MONGO_URI')
secret_key = os.getenv('SECRET_KEY')

mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = list(mongo.db.posts.find())
    posts_data = [{'id': str(post['_id']), 'title': post['title'], 'content': post['content']} for post in posts]
    return jsonify({'posts': posts_data})

@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    new_post = {'title': data['title'], 'content': data['content']}
    mongo.db.posts.insert_one(new_post)
    return jsonify({'message': 'Post created successfully'})

if __name__ == '__main__':
    app.run(debug=True)
