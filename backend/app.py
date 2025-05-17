import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Get environment variables
mongo_uri = os.getenv('MONGO_URI')
db_name = os.getenv('MONGO_DB_NAME')
users_collection_name = os.getenv('MONGO_USERS_COLLECTION')
todos_collection_name = os.getenv('MONGO_TODOS_COLLECTION')

# Initialize Flask app
backend_app = Flask(__name__)

# MongoDB connection setup
client = MongoClient(mongo_uri)
db = client[db_name]
users_collection = db[users_collection_name]
todos_collection = db[todos_collection_name]

# Route to handle user data submission
@backend_app.route('/submit', methods=['POST'])
def submit_user_data():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')

    if not name or not age:
        return jsonify({'error': 'Both name and age are required!'}), 400

    users_collection.insert_one({'name': name, 'age': age})
    return jsonify({'message': 'Data submitted successfully!'}), 200

# Route to handle todo item submission
@backend_app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    data = request.get_json()
    item_name = data.get('itemName')
    item_description = data.get('itemDescription')

    if not item_name or not item_description:
        return jsonify({'error': 'Both item name and description are required!'}), 400

    todos_collection.insert_one({'itemName': item_name, 'itemDescription': item_description})
    return jsonify({'message': 'To-Do item added successfully!'}), 200

if __name__ == '__main__':
    backend_app.run(debug=True, port=3000)
