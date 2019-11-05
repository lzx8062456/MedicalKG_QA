#!/usr/bin/env python
#coding:utf-8

from question_classifer import *
from question_parser import *
from answer_search import *

'''问答构建'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionParser()
        self.searcher = AnswerSearcher()
    def chat_main(self, sent):
        answer = '您好，我是小勇医药智能助理，希望可以帮到您。'
        res_classify = self.classifier.classify(sent)
        #print(res_classify)
        if not res_classify:
            answer='不好意思噢这个问题我也不晓得'
            return answer
        res_sql = self.parser.parser_main(res_classify)
        #print(res_sql)
        final_answers = self.searcher.search_main(res_sql)
        print(final_answers)
        if not final_answers:
            answer = '不好意思噢这个问题我也不晓得'
            return answer
        else:
            return '\n'.join(final_answers)

if __name__ == '__main__':
    handler = ChatBotGraph()
    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        print('小勇:', answer)
