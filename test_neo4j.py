#!/usr/bin/env python
# coding:utf-8

from py2neo import Graph, Node,Relationship

g = Graph(
    host='127.0.0.1',
    http_port=7474,
    user='neo4j',
    password='123456')

# 创建节点
node1=Node('Bayern',name='thomas',id='25',location='Munich')
node2=Node('Bayern',name='levy',id='09',location='Munich')
node3=Node('Bayern',name='javi',id='08',location='Munich')

g.create(node1)
g.create(node2)
g.create(node3)

teammate1=Relationship(node1,'teammate',node2)
teammate2=Relationship(node2,'teammate',node3)

g.create(teammate1)
g.create(teammate2)