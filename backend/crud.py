from flask import Blueprint, request, jsonify
from jsonschema import validate, ValidationError
from bson.objectid import ObjectId
import json
import os
from database import get_database  # Import the database connection

crud = Blueprint('crud', __name__)

db = get_database()
collection = db['candidates']

# Load the JSON schema using a relative path
schema_path = os.path.join(os.path.dirname(__file__), 'schema.json')
with open(schema_path) as f:
    schema = json.load(f)

@crud.route('/data', methods=['GET'])
def get_data():
    # Fetch data from MongoDB
    documents = collection.find({})
    # Convert ObjectId to string and include all fields
    data = [{key: str(doc[key]) if isinstance(doc[key], ObjectId) else doc[key] for key in doc.keys()} for doc in documents]
    return jsonify(data)

@crud.route('/submit_application', methods=['POST'])
def submit_application():
    # Collect data from the form
    applicant_data = request.form.to_dict()

    # Set the initial status to "applied"
    applicant_data['status'] = 'applied'

    # Validate the data against the schema
    try:
        validate(instance=applicant_data, schema=schema)
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    # Insert the validated data into MongoDB
    collection.insert_one(applicant_data)
    return jsonify({"message": "Application submitted successfully"}), 201