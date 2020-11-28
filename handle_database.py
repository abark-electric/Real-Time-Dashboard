from pymongo import MongoClient
from constants import MONGODB_CONN


class DatabaseController:
    def __init__(self, database_name, collection_name):
        self.cluster = MongoClient(MONGODB_CONN)
        self.db_nm = database_name
        self.coll_nm = collection_name
        self.db = self.cluster[database_name]
        self.coll = self.db[collection_name]

    def create_collection(self):
        self.db.create_collection(self.coll_nm)

    def drop_collection(self):
        self.coll.drop()

# cluster = MongoClient(MONGODB_CONN)
# db = cluster['vip_parser']

# Create collection
# db.create_collection('ct_data_live')

#collection = db['ct_data_live']

# Drop collection
# print('Dropping . . .')
# collection.drop()


if __name__ == "__main__":
    DatabaseController('vip_parser', 'ct_data_live').drop_collection()
