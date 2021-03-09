#!/usr/bin/python

"""
Para ejecutar el script
py fixLapi.py pathToFileCsv
"""

# -*- encoding: utf-8 -*-
import pymongo
import sys

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# conexión
con = MongoClient('server2.monadic.solutions', 27017, authSource='adn_test',
                  username='freyjaUser', password='B12030103', authMechanism='SCRAM-SHA-1')
db = con.adn_test
collection = db.products

brands = {
  "1": {
    "code": 1,
    "brand_id": ObjectId("5f15fa0055b2282c29284b24"),
    "name": "Con Cita"
  },
  "2": {
    "code": 2,
    "brand_id": ObjectId("603e93ef27473c7b900b5fd9"),
    "name": "Sin Cita"
  }
}

csvFile = open(sys.argv[1], 'r')
for line in csvFile.read().split('\n')[1:-1]:
  values = line.split(',')
  # print(values[0], values[1])
  result = collection.find_one({'code': int(values[0])})
  if (result):
    updated = collection.update_one({'_id': result["_id"]}, {
      '$set': {
        'brand': brands[values[1]]
      }
    }, upsert=False)
    print(result['code'], values[1], brands[values[1]], result['name'])
  else:
    print(values, "Error")
