import sys
from pymongo import MongoClient
from Parse import parse_DBLP_file, parse_MAG_file, Paper

# Setup MongoDB connection
client = MongoClient('localhost', 27017)
db = client['dblp']
collection = db['papers']

def insert_into_mongodb(paper):
    try:
        paper_dict = paper.__dict__
        collection.insert_one(paper_dict)
        print(f"Inserted: {paper.title}")
    except Exception as e:
        print(f"Error inserting {paper.title} into MongoDB: {e}")

def main():
    # Clear the collection before loading new data
    collection.drop()
    print("Collection cleared.")

    # Callback functions to apply to each paper
    callbacks = [insert_into_mongodb]

    # Load papers from DBLP dataset
    print("Starting to load papers from DBLP...")
    dblp_paper_count = parse_DBLP_file(callbacks, 0, 100)  # Adjust as needed
    print(f"Finished loading {dblp_paper_count} papers from DBLP.")

    # Optional: Load papers from MAG dataset
    # print("Starting to load papers from MAG...")
    # mag_paper_count = parse_MAG_file(callbacks, 0, 100)  # Adjust as needed
    # print(f"Finished loading {mag_paper_count} papers from MAG.")

if __name__ == "__main__":
    main()
