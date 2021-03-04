#!/usr/bin/python

"""
Para ejecutar el script
py fixCableN.py pathToFileCsv
"""

# -*- encoding: utf-8 -*-
import pymongo
import sys

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# conexión
con = MongoClient('server2.monadic.solutions', 27017, authSource='cablenetworks_test',
                  username='freyjaUser', password='freyjaPass', authMechanism='SCRAM-SHA-1')
db = con.cablenetworks_test
collection = db.products

csvFile = open(sys.argv[1], 'r')
for line in csvFile.read().split('\n')[1:-1]:
  values = line.split(',')
  # print(values[0], values[1])
  result = collection.find_one({'sku': values[0]})
  if (result):
    updated = collection.update_one({'_id': result["_id"]}, {'$set': {'buyPrice': float(values[1][1:])}}, upsert=False)
    print(result['code'], result['sku'], result['name'], values[1])
  else:
    print(values[0], "Error")
