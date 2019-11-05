#!/usr/bin/env python
#coding:utf-8

import pymongo
from lxml import etree
import os
from max_cut import *

class MedicalGraph:
    def __init__(self):
        # 连接数据库
        self.conn=pymongo.MongoClient()
        # 这里的split 原先是 split('/'),刘老师在Linux实现的,我的平台是windows,所以作修改
        # cur_dir: 当前文件所在路径
        cur_dir='/'.join(os.path.abspath('__file__').split('\\')[:-1])
        self.db=self.conn['medical']
        self.col=self.db['data']
        #first_words=[i.strip() for i in open(os.path.join(cur_dir,'first_name.txt'))]
        alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                     'u', 'v', 'w', 'x', 'y', 'z']
        nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        self.stop_words = alphabets + nums#first_words + alphabets + nums
        self.key_dict={
            '医保比例': 'yibao_status',
            '患病比例': 'get_prob',
            '易感人群': 'easy_get',
            '传染方式': 'get_way',
            '就诊科室': 'cure_department',
            '治疗方式': 'cure_way',
            '治疗周期': 'cure_lasttime',
            '治愈率': 'cured_prob',
            '药品明细': 'drug_detail',
            '药品推荐': 'recommand_drug',
            '推荐': 'recommand_eat',
            '忌食': 'not_eat',
            '宜食': 'do_eat',
            '症状': 'symptom',
            '检查': 'check',
            '成因': 'cause',
            '预防措施': 'prevent',
            '所属类别': 'category',
            '简介': 'desc',
            '名称': 'name',
            '常用药品': 'common_drug',
            '治疗费用': 'cost_money',
            '并发症': 'acompany'
        }
        self.cuter=CutWords()

    # 收集医疗信息
    def collect_medical(self):
        # cates: 所属类别
        cates=[]
        inspects=[]
        count=0
        for item in self.col.find():
            data={}
            basic_info=item['basic_info']
            name=basic_info['name']
            if not name:
                continue
            '''下述存储的信息均对应于data_spider.py中spider_main的命名'''
            # 基本信息
            data['名称']=name
            data['简介']='\n'.join(basic_info['desc']).replace('\r\n\t','')\
                .replace('\r\n\n\n','').replace(' ','').replace('\r\n','\n')
            category=basic_info['category']
            data['所属类别']=category
            cates+=category
            # 获取检查信息
            inspect=item['inspect_info']
            inspects+=inspect
            # 温馨提示
            attributes=basic_info['attributes']
            # 成因及预防
            data['预防措施']=item['prevent_info']
            data['成因']=item['cause_info']
            # 并发症
            data['症状']=list(set([i for i in item["symptom_info"][0] if i[0] not in self.stop_words]))
            '''注意,这段还是不熟悉,需要查表格'''
            for attr in attributes:
                attr_pair=attr.split('：')
                if len(attr_pair)==2:
                    key=attr_pair[0]
                    value=attr_pair[1]
                    data[key]=value

            # 检查
            inspects=item['inspect_info']
            jcs=[]
            for inspect in inspects:
                jc_name=self.get_inspect(inspect)
                if jc_name:
                    jcs.append(jc_name)
            data['检查']=jcs

            # 食物
            food_info=item['food_info']
            '''此处需要检查数据类型'''
            if food_info:
                data['宜食']=food_info['good']
                data['忌食']=food_info['bad']
                data['推荐']=food_info['recommond']

            # 药品
            drug_info=item['drug_info']
            '''此处需要检查数据类型'''
            data['药品推荐']=list(set([i.split('(')[-1].replace(')','') for i in drug_info]))
            data['药品明细']=drug_info
            data_modify={}
            '''这段奇奇怪怪的代码要细看并写清楚注释'''
            for attr,value in data.items():
                # 获取英文表示
                attr_en=self.key_dict.get(attr)
                if attr_en:
                    data_modify[attr_en]=value
                if attr_en in ['yibao_status', 'get_prob', 'easy_get', 'get_way', "cure_lasttime", "cured_prob"]:
                    data_modify[attr_en]=value.replace(' ','').replace('\t','')
                elif attr_en in ['cure_department','cure_way','common_drug']:
                    data_modify[attr_en]=[i for i in value.split(' ') if i]
                elif attr_en in ['acompany']:
                    acompany = [i for i in self.cuter.max_biward_cut(data_modify[attr_en]) if len(i) > 1]
                    data_modify[attr_en]=acompany
            try:
                self.db['medical'].insert(data_modify)
                count+=1
                print(count)
            except Exception as e:
                print(e)
        return

    def get_inspect(self,url):
        res=self.db['jc'].find_one({'url':url})
        if not res:
            return ''
        else:
            return res['name']

    def modify_jc(self):
        for item in self.db['jc'].find():
            url=item['url']
            content=item['html']
            selector=etree.HTML(content)
            name = selector.xpath('//title/text()')[0].split('结果分析')[0]
            desc = selector.xpath('//meta[@name="description"]/@content')[0].replace('\r\n\t', '')
            self.db['jc'].update({'url': url}, {'$set': {'name': name, 'desc': desc}})

if __name__=='__main__':
    handler=MedicalGraph()
    handler.collect_medical()
    #handler.modify_jc()


