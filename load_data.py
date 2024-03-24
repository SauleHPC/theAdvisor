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
    batch_size = 100  # Adjust batch size to 100
    start_paper = 0
    total_processed = 0
    limit = 1000  # Limit to test on 1000 papers

    while True:
        # Adjust the batch size if the remaining papers are fewer than the batch size
        if total_processed + batch_size > limit:
            batch_size = limit - total_processed

        processed_papers = parse_and_load_dblp_to_mongodb(file_path, start_paper, batch_size)
        if processed_papers == 0 or total_processed >= limit:
            # No more papers processed or limit reached, end the loop
            print("No more papers to process or limit reached.")
            break
        total_processed += processed_papers
        print(f"Processed {total_processed} papers so far...")
        start_paper += processed_papers

        if total_processed >= limit:
            # Break the loop if the total processed papers have reached the limit
            break

    print(f"Finished processing. Total papers processed: {total_processed}.")
