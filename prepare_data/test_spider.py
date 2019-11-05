#!/usr/bin/env python
# coding:utf-8

import urllib.request
import urllib.parse
import requests
from lxml import etree
import pymongo


def get_html(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    proxies = {
        'http': None,
        'https': None
    }
    html = requests.get(url=url, headers=headers, proxies=proxies)
    html.encoding = 'gbk'
    return html.text


# url = 'http://jib.xywy.com/il_sii/gaishu/38.htm'
# content = get_html(url)
#
#
# def basic_info_spider(url):
#     html = get_html(url)
#     selector = etree.HTML(html)
#     title = selector.xpath('//title/text()')[0].split(',')[0]
#     # print(title)
#     category = selector.xpath('//div[@class="wrap mt10 nav-bar"]/a/text()')
#     # print(category)
#     desc = selector.xpath('//div[@class="jib-articl-con jib-lh-articl"]/p/text()')
#     # print(desc)
#     ps = selector.xpath('//div[@class="mt20 articl-know"]/p')
#     print(ps)
#     infobox = []
#     for p in ps:
#         info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ', '').replace(
#             '\t', '')
#         infobox.append(info)
#     print(infobox)
#
#
# '''treat_infobox治疗信息解析'''
#
#
# def treat_spider(url):
#     html = get_html(url)
#     selector = etree.HTML(html)
#     ps = selector.xpath('//div[starts-with(@class,"mt20 articl-know")]/p')
#     infobox = []
#     for p in ps:
#         info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ', '').replace(
#             '\t', '')
#         infobox.append(info)
#     print(infobox)
#     return infobox
#
#
# # basic_info_spider(url)
# treat_url = 'http://jib.xywy.com/il_sii/treat/38.htm'
# treat_spider(treat_url)
#
# '''drug_infobox药物治疗信息解析'''
#
#
# def drug_spider(url):
#     html = get_html(url)
#     selector = etree.HTML(html)
#     ps = selector.xpath('//div[starts-with(@class,"fl drug-pic-rec mr30")]/p/a')
#     infobox = []
#     for p in ps:
#         info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ', '').replace(
#             '\t', '').replace(' ', '')
#         infobox.append(info)
#     print(infobox)
#     return infobox
#
#
# drug_url = 'http://jib.xywy.com/il_sii/drug/1746.htm'
# drug_spider(drug_url)
#
# '''treat_infobox治疗解析'''
#
#
# def drug_spider_1(url):
#     html = get_html(url)
#     selector = etree.HTML(html)
#     drugs = [i.replace('\n', '').replace('\t', '').replace(' ', '') for i in
#              selector.xpath('//div[@class="fl drug-pic-rec mr30"]/p/a/text()')]
#     print(drugs)
#     return drugs
#
#
# drug_url = 'http://jib.xywy.com/il_sii/drug/1746.htm'
# drug_spider_1(drug_url)
#
#
# '''food_infobox食物治疗信息解析'''
# def food_spider(url):
#     html = get_html(url)
#     selector = etree.HTML(html)
#     divs = selector.xpath('//div[@class="diet-img clearfix mt20"]')
#     # 这个标签下有三种食物,宜吃/忌吃/推荐,所以用标号分别进行区分
#     try:
#         food_data = {}
#         food_data['good'] = divs[0].xpath('./div/p/text()')
#         food_data['bad'] = divs[1].xpath('./div/p/text()')
#         food_data['recommond'] = divs[2].xpath('./div/p/text()')
#     except:
#         return {}
#     print(food_data)
#     return food_data
#
# food_url='http://jib.xywy.com/il_sii/food/1746.htm'
# food_spider(food_url)
#
#
# def symptom_spider(url):
#     html = get_html(url)
#     selector = etree.HTML(html)
#     symptoms = selector.xpath('//a[@class="gre"]/text()')
#     ps = selector.xpath('//p')
#     detail = []
#     for p in ps:
#         info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ', '') \
#             .replace('\t', '').replace(' ', '')
#         detail.append(info)
#     symptoms_data = {}
#     symptoms_data['symptoms'] = symptoms
#     symptoms_data['symptoms_details'] = detail
#     print(symptoms_data)
#     return symptoms_data
#
# symptom_url='http://jib.xywy.com/il_sii/symptom/1746.htm'
# symptom_spider(symptom_url)


# def inspect_spider(url):
#     html=get_html(url)
#     selector=etree.HTML(html)
#     inspects=selector.xpath('//li[@class="check-item"]/a/@href')
#     print(inspects)
#     return inspects
# inspect_url='http://jib.xywy.com/il_sii/inspect/1746.htm'
# inspect_spider(inspect_url)

# def common_spider(url):
#     # 通用模块下面包含了疾病预防和疾病起因的内容
#     html = get_html(url)
#     selector = etree.HTML(html)
#     ps = selector.xpath('//p')
#     infobox = []
#     for p in ps:
#         info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ', '') \
#             .replace('\t', '').replace(' ', '')
#         if info:
#             infobox.append(info)
#     return '\n'.join(infobox)
#
#
# def common_spider_1(url):
#     html = get_html(url)
#     selector = etree.HTML(html)
#     ps = selector.xpath('//p')
#     infobox = []
#     for p in ps:
#         info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ','').replace('\t', '')
#         if info:
#             infobox.append(info)
#     return '\n'.join(infobox)
#
#
# common_url = 'http://jib.xywy.com/il_sii/prevent/1746.htm'
# t=common_spider(common_url)
# print(t)
# t1=common_spider_1(common_url)
# print(t1)


# def inspect_crawl():
#     data = {}
#     for page in range(1, 3685):
#         try:
#             url = 'http://jck.xywy.com/jc_%s.html' % page
#             html = get_html(url)
#             data['url'] = url
#             data['html'] = html
#             #db['jc'].insert(data)
#             print(url)
#         except Exception as e:
#             print(e)
#     return data
#
# inspect_crawl()

def test_mongodb():
    client=pymongo.MongoClient('mongodb://localhost:27017/')
    print(client)
test_mongodb()
