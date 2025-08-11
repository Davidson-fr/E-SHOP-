import os, json, time
from pymongo import MongoClient

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongo:27017/eshop')

print("Connecting to MongoDB:", MONGO_URI)
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

# wait for mongo to be ready
for _ in range(10):
    try:
        client.admin.command('ping')
        break
    except Exception as e:
        print('Mongo not ready, waiting 1s...', e)
        time.sleep(1)

db = client.eshop

with open('seed_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

if 'products' in data:
    print('Inserting products...')
    db.products.delete_many({})
    db.products.insert_many(data['products'])
    print('Inserted', db.products.count_documents({}), 'products.')

if 'orders' in data:
    print('Inserting orders...')
    db.orders.delete_many({})
    db.orders.insert_many(data['orders'])
    print('Inserted', db.orders.count_documents({}), 'orders.')

print('Seeding finished.')
