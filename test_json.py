#!/usr/bin/env python
#coding:utf-8
# 测试用法文件

import json

file=open('./data/medical.json',encoding='utf-8')
data=file.readline()
count=0
while data:
    print(json.loads(data).keys())
    data=file.readline()
    count+=1
    break
print(count)