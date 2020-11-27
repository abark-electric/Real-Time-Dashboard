from pymongo import MongoClient
from constants import MONGODB_CONN

cluster = MongoClient(MONGODB_CONN)
db = cluster['vip_parser']

# Create collection
# db.create_collection('ct_data_live')

#collection = db['ct_data_live']

# Drop collection
# print('Dropping . . .')
# collection.drop()
