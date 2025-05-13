import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
import json
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# get the environment variables
mongo_uri = os.getenv('MONGO_URI')
db_name = os.getenv('MONGO_DB_NAME')
collection_name = os.getenv('MONGO_COLLECTION_NAME')

# Initialize Flask app with custom template folder path
app = Flask(__name__, template_folder='../frontend')

########################################################
# Get the absolute path to data.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data.json')

@app.route('/api')
def get_data():
    with open(DATA_FILE) as f:
        return jsonify(json.load(f))
    

########################################################
# MongoDB Connection
########################################################
# MongoDB connection setup using the MONGO_URL environment variable
client = MongoClient(mongo_uri)
db = client[db_name]
collection = db[collection_name]


# Route to render the form page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    name = request.form.get('name')
    age = request.form.get('age')

    # Check if both fields are provided
    if not name or not age:
        return render_template('index.html', error="Both name and age are required!")
    
    # Insert the data into MongoDB (regardless of type)
    collection.insert_one({'name': name, 'age': age})
    
    # Redirect to the success page after successful submission
    return redirect(url_for('success'))

# Route to render success page
@app.route('/success')
def success():
    return render_template('success.html')



if __name__ == '__main__':
    app.run(debug=True)
