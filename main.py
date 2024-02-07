from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Replace this connection string with your MongoDB Atlas connection string
MONGODB_CONNECTION_STRING = 'mongodb+srv://eronni1:HPCSCLOUD@cluster0.hxilhex.mongodb.net/'

# Connect to MongoDB Atlas
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client['mongodbVSCodePlaygroundDB']  # Replace 'main' with your database name
collection = db['sales']  # Replace 'sales' with your collection name
@app.route('/sales', methods=['GET'])
def get_sales():
    # Query MongoDB to retrieve sales data
    sales_data = collection.find()

    # Convert MongoDB cursor to list of dictionaries
    sales_list = []
    for sale in sales_data:
        # Convert ObjectId to string for serialization
        sale['_id'] = str(sale['_id'])
        sales_list.append(sale)

    # Return sales data as JSON response
    return jsonify(sales_list)

if __name__ == '__main__':
    app.run(debug=True)