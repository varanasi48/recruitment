from flask import Flask, request, jsonify
from pymongo import MongoClient
from jsonschema import validate, ValidationError
import json
import os
from flask_cors import CORS  # Import CORS
from crud import crud  # Import the crud blueprint
from urllib.parse import quote_plus  # Import quote_plus
from dotenv import load_dotenv  # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) # Enable CORS for the entire app
app.register_blueprint(crud, url_prefix='/api')  # Register the blueprint

# Encode the username and password
username = quote_plus(os.getenv('MONGO_USERNAME'))
password = quote_plus(os.getenv('MONGO_PASSWORD'))
cluster = os.getenv('MONGO_CLUSTER')

# Connect to MongoDB
client = MongoClient(f'mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=prachi')
db = client['prachi']
collection = db['candidates']

# Load the JSON schema using a relative path
schema_path = os.path.join(os.path.dirname(__file__), 'schema.json')
with open(schema_path) as f:
    schema = json.load(f)

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Flask server!"

@app.route('/data', methods=['GET'])
def get_data():
    # Fetch data from MongoDB
    documents = collection.find({})
    data = [{"name": doc.get("name"), "experience": doc.get("experience"), "salary": doc.get("salary")} for doc in documents]
    return jsonify(data)

@app.route('/submit_application', methods=['POST'])
def submit_application():
    # Collect data from the form
    applicant_data = request.form.to_dict()

    # Validate the data against the schema
    try:
        validate(instance=applicant_data, schema=schema)
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    # Insert the validated data into MongoDB
    collection.insert_one(applicant_data)
    return jsonify({"message": "Application submitted successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
