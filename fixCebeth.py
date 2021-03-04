#!/usr/bin/python

"""
Para ejecutar el script
py fixCebeth.py
"""

# -*- encoding: utf-8 -*-
import pymongo

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# conexión
con = MongoClient('107.191.125.115', 27017, authSource='cebeth_new',
                  username='freyjaUser', password='cebethPass123', authMechanism='SCRAM-SHA-1')
db = con.cebeth_new

collection = db.customerrecords
clients = db.clients
result = collection.find({"recordType_id": ObjectId("5f21db52c3cea4527c0fcf08")})
size = 0
for doc in result:
  size = size + 1
  client = clients.find_one({"_id": doc["customer_id"]})
  print(size, client["name"])
  newvalues = {"$set": {"recordType_id": "5f9a1fe1e69f82e5f9ac09ad"}}
  collection.update_one({"_id": doc["_id"]}, newvalues)
