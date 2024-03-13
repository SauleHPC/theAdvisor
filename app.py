from flask import Flask, jsonify
from pymongo import MongoClient
from bson import ObjectId
import json

app = Flask(__name__)

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['dblp']  # Connect to 'dblp' database
collection = db['papers']  # Collection to store DBLP papers

# Custom JSON encoder to handle ObjectId serialization
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

@app.route('/papers', methods=['GET'])
def get_papers():
    papers_list = []
    # Use MongoDB's $sample to randomly select 50 documents
    for paper in collection.aggregate([{"$sample": {"size": 50}}]):
        paper['_id'] = str(paper['_id'])  # Convert ObjectId to string for JSON serialization
        papers_list.append(paper)
    return jsonify(papers_list)

if __name__ == '__main__':
    app.json_encoder = CustomJSONEncoder  # Set custom JSON encoder for the app
    app.run(debug=True)
