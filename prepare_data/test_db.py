#!/usr/bin/env python
#coding:utf-8

import pymongo

myclient=pymongo.MongoClient()
mydb=myclient['medical']
mycol=mydb['jc']
print(list(mycol.find().limit(1)))
