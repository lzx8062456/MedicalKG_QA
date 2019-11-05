#!/usr/bin/env python
# coding:utf-8

import os
import ahocorasick


class Test:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath('__file__').split('//')[:-1])
        self.disease_path = os.path.join(cur_dir, './dict/disease.txt')
        self.department_path = os.path.join(cur_dir, './dict/department.txt')
        self.check_path = os.path.join(cur_dir, './dict/check.txt')
        self.drug_path = os.path.join(cur_dir, './dict/drug.txt')
        self.food_path = os.path.join(cur_dir, './dict/food.txt')
        self.producer_path = os.path.join(cur_dir, './dict/producer.txt')
        self.symptom_path = os.path.join(cur_dir, './dict/symptoms.txt')
        self.deny_path = os.path.join(cur_dir, './dict/deny.txt')

        self.disease_wds = [i.strip() for i in open(self.disease_path) if i.strip()]
        self.department_wds = [i.strip() for i in open(self.department_path) if i.strip()]
        self.check_wds = [i.strip() for i in open(self.check_path) if i.strip()]
        self.drug_wds = [i.strip() for i in open(self.drug_path) if i.strip()]
        self.food_wds = [i.strip() for i in open(self.food_path) if i.strip()]
        self.producer_wds = [i.strip() for i in open(self.producer_path) if i.strip()]
        self.symptom_wds = [i.strip() for i in open(self.symptom_path) if i.strip()]
        self.region_words = set(self.department_wds + self.disease_wds
                                + self.check_wds + self.drug_wds +
                                self.food_wds + self.producer_wds +
                                self.symptom_wds)

    def test_region_words(self):
        print(self.region_words)
        print(len(self.region_words))

    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.disease_wds:
                wd_dict[wd].append('disease')
            if wd in self.department_wds:
                wd_dict[wd].append('department')
            if wd in self.check_wds:
                wd_dict[wd].append('check')
            if wd in self.drug_wds:
                wd_dict[wd].append('drug')
            if wd in self.food_wds:
                wd_dict[wd].append('food')
            if wd in self.symptom_wds:
                wd_dict[wd].append('symptom')
            if wd in self.producer_wds:
                wd_dict[wd].append('producer')
            print(wd_dict)
            break
        return wd_dict

    # 构造actree,加速过滤
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree


t = Test()
# t.test_region_words()
world_list=['javi','levy','thomas','manu','frank','arjen']
#t.build_wdtype_dict()
actree=t.build_actree(world_list)
q1='where is javi?'
for i in actree.iter(q1):
    wd=i
    print(wd)