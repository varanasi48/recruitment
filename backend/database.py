from pymongo import MongoClient
from urllib.parse import quote_plus  # Import quote_plus
from dotenv import load_dotenv  # Import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_database():
    # Encode the username and password
    username = quote_plus(os.getenv('MONGO_USERNAME'))
    password = quote_plus(os.getenv('MONGO_PASSWORD'))
    cluster = os.getenv('MONGO_CLUSTER')

    # Connect to MongoDB
    client = MongoClient(f'mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=prachi')
    db = client['prachi']
    return db
