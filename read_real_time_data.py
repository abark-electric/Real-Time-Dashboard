# Read live data using mongodb changestreams
from constants import MONGODB_CONN

import os
import pymongo
from bson.json_util import dumps
x=[]
client = pymongo.MongoClient(MONGODB_CONN)
print('Working 1')
change_stream = client.changestream.collection.watch()
print('Working 2')
for change in change_stream:
    # print('Working 3')
    # print(change['fullDocument']['hello'])
    x.append(change['fullDocument']['hello'])
    print(x)
    # print('Working 4')
    print('') # for readability only
print('Worked\5')