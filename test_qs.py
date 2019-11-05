#!/usr/bin/env python


a={'args': {'白菜': ['food']}, 'question_types': ['food_do_disease']}
dic=a['args']
entity_dict={}
for arg, types in dic.items():
    print(arg)
    for type in types:
        if type not in entity_dict:
            entity_dict[type] = [arg]
        else:
            entity_dict[type].append(arg)
print(entity_dict)