#!/usr/bin/env python
#coding:utf-8

import requests
import urllib.request
import urllib.parse
from lxml import etree
import pymongo
import re

'''基于寻医问药的医疗数据采集'''
class MedicalSpider:
    def __init__(self):
        self.conn=pymongo.MongoClient()
        self.db=self.conn['medical']
        self.col=self.db['data']

    '''根据url,请求html'''
    def get_html(self,url):
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

    '''url解析'''
    def url_parser(self,content):
        selector=etree.HTML(content)
        urls=['http://www.anliguan.com'+i for i in selector.xpath('//h2[@class="item-title"]/a/@href')]
        return urls

    '''主要的爬取的链接'''
    def spider_main(self):
        # 收集页面
        for page in range(1,11000):
            try:
                basic_url='http://jib.xywy.com/il_sii/gaishu/%s.htm'%page # 疾病描述
                cause_url='http://jib.xywy.com/il_sii/cause/%s.htm'%page # 疾病起因
                prevent_url='http://jib.xywy.com/il_sii/prevent/%s.htm'%page # 疾病预防
                symptom_url='http://jib.xywy.com/il_sii/symptom/%s.htm'%page #疾病症状
                inspect_url='http://jib.xywy.com/il_sii/inspect/%s.htm'%page # 疾病检查
                treat_url='http://jib.xywy.com/il_sii/treat/%s.htm'%page # 疾病治疗
                food_url = 'http://jib.xywy.com/il_sii/food/%s.htm' % page # 饮食治疗
                drug_url = 'http://jib.xywy.com/il_sii/drug/%s.htm' % page # 药物治疗
                data={}
                data['url'] = basic_url
                data['basic_info'] = self.basicinfo_spider(basic_url)
                data['cause_info'] = self.common_spider(cause_url)
                data['prevent_info'] = self.common_spider(prevent_url)
                data['symptom_info'] = self.symptom_spider(symptom_url)
                data['inspect_info'] = self.inspect_spider(inspect_url)
                data['treat_info'] = self.treat_spider(treat_url)
                data['food_info'] = self.food_spider(food_url)
                data['drug_info'] = self.drug_spider(drug_url)
                print(page, basic_url)
                self.col.insert(data)
            except Exception as e:
                print(e,page)

    '''基本信息解析'''
    def basicinfo_spider(self,url):
        html=self.get_html(url)
        selector=etree.HTML(html)
        title = selector.xpath('//title/text()')[0]
        # 获取当前疾病的所属目录,比如感冒的目录:['疾病百科', '内科', '呼吸内科']
        category=selector.xpath('//div[@class="wrap mt10 nav-bar"]/a/text()')
        # 获取疾病的描述
        desc=selector.xpath('//div[@class="jib-articl-con jib-lh-articl"]/p/text()')
        # 获取医疗网页上的温馨提示
        # 由于后面需要继续使用lxml.etree._Element属性值,并且去除里面多余的符号,所以这里不加text()提取值
        ps=selector.xpath('//div[@class="mt20 articl-know"]/p')
        infobox=[]
        for p in ps:
            info=p.xpath('string(.)').replace('\r','').replace('\n','').replace('\xa0','').\
                replace('   ', '').replace('\t','')
            infobox.append(info)
        # 使用dict格式存储对应的数据
        basic_data = {}
        basic_data['category'] = category
        basic_data['name'] = title.split('的简介')[0]
        basic_data['desc'] = desc
        basic_data['attributes'] = infobox
        return basic_data

    '''treat_infobox治疗信息解析'''
    def treat_spider(self,url):
        html=self.get_html(url)
        selector=etree.HTML(html)
        ps=selector.xpath('//div[starts-with(@class,"mt20 articl-know")]/p')
        infobox=[]
        for p in ps:
            info = p.xpath('string(.)').replace('\r','').replace('\n','').replace('\xa0', '').replace('   ', '').replace('\t','')
            infobox.append(info)
        return infobox

    '''drug_infobox药物治疗信息解析'''
    def drug_spider(self,url):
        html=self.get_html(url)
        selector=etree.HTML(html)
        ps=selector.xpath('//div[starts-with(@class,"fl drug-pic-rec mr30")]/p/a')
        infobox=[]
        for p in ps:
            info=p.xpath('string(.)').replace('\r','').replace('\n','').replace('\xa0', '').replace('   ', '')\
                .replace('\t','').replace(' ','')
            infobox.append(info)
        return infobox

    '''food_infobox食物治疗信息解析'''
    def food_spider(self,url):
        html=self.get_html(url)
        selector=etree.HTML(html)
        divs=selector.xpath('//div[@class="diet-img clearfix mt20"]')
        # 这个标签下有三种食物,宜吃/忌吃/推荐,所以用标号分别进行区分
        try:
            food_data={}
            food_data['good']=divs[0].xpath('./div/p/text()')
            food_data['bad']=divs[1].xpath('./div/p/text()')
            food_data['recommond']=divs[2].xpath('./div/p/text()')
        except:
            return {}
        return food_data

    '''症状信息解析'''
    def symptom_spider(self,url):
        html = self.get_html(url)
        selector = etree.HTML(html)
        symptoms = selector.xpath('//a[@class="gre"]/text()')
        ps = selector.xpath('//p')
        detail = []
        for p in ps:
            info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ', '') \
                .replace('\t', '').replace(' ', '')
            detail.append(info)
        symptoms_data = {}
        symptoms_data['symptoms'] = symptoms
        symptoms_data['symptoms_details'] = detail
        #print(symptoms_data)
        return symptoms,detail

    '''信息检查解析'''
    def inspect_spider(self,url):
        html=self.get_html(url)
        selector=etree.HTML(html)
        inspects=selector.xpath('//li[@class="check-item"]/a/@href')
        return inspects

    '''通用模块解析'''
    def common_spider(self,url):
        # 通用模块下面包含了疾病预防和疾病起因的内容
        html=self.get_html(url)
        selector=etree.HTML(html)
        ps=selector.xpath('//p')
        infobox=[]
        for p in ps:
            info=p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ', '') \
                .replace('\t', '').replace(' ', '')
            if info:
                infobox.append(info)
        return '\n'.join(infobox)

    '''检查项抓取模块'''
    def inspect_crawl(self):
        for page in range(1,3685):
            try:
                data={}
                url='http://jck.xywy.com/jc_%s.html'%page
                html = self.get_html(url)
                data['url'] = url
                data['html'] = html
                self.db['jc'].insert(data)
                print(url)
            except Exception as e:
                print(e)
        return data

handler=MedicalSpider()
# 获取检查信息
#handler.inspect_crawl()
# 爬取完整的医疗数据并进行存储
handler.spider_main()
print('Spider done.')

