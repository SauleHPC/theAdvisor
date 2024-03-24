import gzip
from pymongo import MongoClient
# Adjust the import statement according to your project structure
from Parse import parse_DBLP_file
import sys

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['dblp']
collection = db['papers']

# Callback function to insert papers into MongoDB collection
def insert_paper_to_mongodb(paper):
    collection.insert_one(paper.__dict__)

def parse_and_load_dblp_to_mongodb(file_path, start_paper, batch_size):
    callback = [insert_paper_to_mongodb]
    # Process a batch of papers and return the number of papers processed
    processed_papers = parse_DBLP_file(file_path, callback, start_paper, batch_size)
    return processed_papers

if __name__ == "__main__":
    # Clear the collection before inputting new data
    collection.drop()
    print("Collection cleared.")

    file_path = 'dblp.xml.gz'
    batch_size = 1000  # You can adjust the batch size based on your system's capabilities
    start_paper = 0
    total_processed = 0

    # Loop to process the dataset in batches until all papers have been processed
    while True:
        processed_papers = parse_and_load_dblp_to_mongodb(file_path, start_paper, batch_size)
        if processed_papers == 0:
            # No more papers processed, end the loop
            print("Finished processing all papers.")
            break
        total_processed += processed_papers
        print(f"Processed {total_processed} papers so far...")
        start_paper += processed_papers

    print(f"Total papers processed: {total_processed}.")
