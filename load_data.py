import gzip
from pymongo import MongoClient
from Callback import Callback
from Parse import parse_DBLP_file  # Adjust the import statement
import xml.etree.ElementTree as ET
import sys


# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['dblp']  # Connect to 'dblp' database
collection = db['papers']  # Collection to store DBLP papers

# Callback function to insert papers into MongoDB collection
def insert_paper_to_mongodb(paper):
    collection.insert_one(paper.__dict__)  # Insert paper as a dictionary

# Function to parse DBLP file and insert papers into MongoDB
def parse_and_load_dblp_to_mongodb(file_path, paper_limit):
    callback = [insert_paper_to_mongodb]  # Callback function to insert paper into MongoDB
    parse_DBLP_file(callback, start_paper=0, count_to=paper_limit)  # Parse and insert papers up to the limit

if __name__ == "__main__":
    # Parse and load 100 DBLP papers into MongoDB
    parse_and_load_dblp_to_mongodb('dblp.xml.gz', paper_limit=100)
