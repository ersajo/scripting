#!/usr/bin/python

"""
Para ejecutar el script
py cebethMigration.py
"""

# -*- encoding: utf-8 -*-
import pymongo

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# conexión
con = MongoClient('server2.monadic.solutions', 27017, authSource='cebeth',
                  username='freyjaUser', password='cebethpass', authMechanism='SCRAM-SHA-1')
db = con.cebeth

customerCode = 0
collection = db.customerrecords
lastCustomerCode = collection.find({}, {'code': 1}).sort('code', -1).limit(1)
for doc in lastCustomerCode:
  customerCode = doc['code']

photoCode = 0
collection = db.recordphotos
lastPhotoCode = collection.find({}, {'code': 1}).sort('code', -1).limit(1)
for doc in lastPhotoCode:
  photoCode = doc['code']

# Procesamiento de fotos
collection = db.photocebeths

clientsList = list(collection.find({}, {"client_id": 1}))

clients = set()
for doc in clientsList:
  clients.add(doc['client_id'])

customerRecordCol = db.customerrecords
recordPhotoCol = db.recordphotos
for client in clients:
  val = customerRecordCol.find_one({'customer_id': client})
  if (val):
    customerInserted = val['_id']
  else:
    customerCode += 1
    newRecordDoc = {
      'code': customerCode,
      'recordType_id': ObjectId('5f9a1fe1e69f82e5f9ac09ad'),
      'customer_id': client,
      'name': "Respaldo",
      'enabled': True,
      'createdAt': datetime.now().timestamp(),
      'collectionName': 'CustomerRecord'
    }
    customerInserted = customerRecordCol.insert_one(newRecordDoc)
    customerInserted = customerInserted.inserted_id
  
  res = collection.find({'client_id': client})
  #print(customerInserted.inserted_id)
  for row in res:
    photoCode += 1
    print('IMG ', client, row.get('name'))
    newRecordPhotoDoc = {
      'code': photoCode,
      'customerRecord_id': customerInserted,
      'title': row.get('name'),
      'images': row['images'],
      'collectionName': 'RecordPhoto',
      'createdAt': datetime.now().timestamp(),
      'enabled': True
    }
    recordInserted = recordPhotoCol.insert_one(newRecordPhotoDoc)
    #print(recordInserted.inserted_id)

customerCode = 0
collection = db.customerrecords
lastCustomerCode = collection.find({}, {'code': 1}).sort('code', -1).limit(1)
for doc in lastCustomerCode:
  customerCode = doc['code']

documentCode = 0
collection = db.recorddocuments
lastDocumentCode = collection.find({}, {'code': 1}).sort('code', -1).limit(1)
for doc in lastDocumentCode:
  documentCode = doc['code']

# Procesamiento de documentos
collection = db.filecebeths

clientsList = list(collection.find({}, {"client_id": 1}))

clients = set()
for doc in clientsList:
  clients.add(doc['client_id'])

customerRecordCol = db.customerrecords
recordDocumentCol = db.recorddocuments
for client in clients:
  val = customerRecordCol.find_one({'customer_id': client})
  if (val):
    customerInserted = val['_id']
  else:
    customerCode += 1
    newRecordDoc = {
        'code': customerCode,
        'recordType_id': ObjectId('5f21db52c3cea4527c0fcf08'),
        'customer_id': client,
        'name': "Respaldo",
        'enabled': True,
        'createdAt': datetime.now().timestamp(),
        'collectionName': 'CustomerRecord'
    }
    customerInserted = customerRecordCol.insert_one(newRecordDoc)
    customerInserted = customerInserted.inserted_id
  
  res = collection.find({'client_id': client})
  #print(customerInserted)
  for row in res:
    documentCode += 1
    print('DOC ', client, row.get('name'))
    newRecordDocumentDoc = {
        'code': documentCode,
        'customerRecord_id': customerInserted,
        'title': row.get('name'),
        'files': row['files'],
        'collectionName': 'RecordDocument',
        'createdAt': datetime.now().timestamp(),
        'enabled': True
    }
    recordInserted = recordDocumentCol.insert_one(newRecordDocumentDoc)
    #print(recordInserted.inserted_id)

