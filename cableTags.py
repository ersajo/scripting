#!/usr/bin/python

"""
Para ejecutar el script
py cableTags.py pathToFileCsv
"""

# -*- encoding: utf-8 -*-
import pymongo
import csv
import sys

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# conexión
con = MongoClient('server2.monadic.solutions', 27017, authSource='cablenetworks_test',
                  username='freyjaUser', password='freyjaPass', authMechanism='SCRAM-SHA-1')
db = con.cablenetworks_test

tagCode = 0
tagsCollection = db.tags
lastCode = tagsCollection.find({}, {'code': 1}).sort('code', -1).limit(1)
for doc in lastCode:
  tagCode = doc['code']

productsCollection = db.products
csvFile = open(sys.argv[1], "r")
for line in csvFile.read().split('\n')[2:]:
  product_id, val = line.split(',')
  currentProduct = productsCollection.find_one({'code': int(product_id)})
  if currentProduct:
    tagsArray = []
    for tag in val.split('|'):
      tagFounded = tagsCollection.find_one({'name': tag})
      if not tagFounded:
        tagCode = tagCode + 1
        newTagDoc = {
            'code': tagCode,
            'name': tag,
            'createdAt': datetime.now().timestamp(),
            'collectionName': 'Tag',
            'enabled': True
        }
        tagsCollection.insert_one(newTagDoc)
      tagsArray.append(tag)
    productsCollection.update_one({'_id': currentProduct['_id']}, {'$set': {'tags': tagsArray}}, upsert=False)
