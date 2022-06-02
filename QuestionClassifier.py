import json

import jieba
import jieba.posseg as pseg
import joblib
import numpy as np


class PoemQuestionClassifier:
    def __init__(self):
        self.abstractMap = {}
        self.vocab_path = 'model/vocabulary.json'
        self.model_path = 'model/model.model'
        self.poem_classification_path = 'model/poem_classification.json'
        self.vocab = self.load_vocab()
        self.question_class = self.load_question_classification()

    def load_vocab(self):
        with open(self.vocab_path, "r", encoding='utf-8') as f:
            vocab = json.loads(f.read())
        return vocab

    def load_question_classification(self):
        with open(self.poem_classification_path, "r", encoding='utf-8') as f:
            question_classification = json.loads(f.read())
        return question_classification

    def abstract_question(self, question):
        # 加载自定义字典
        jieba.load_userdict('poemData/txt/author.txt')
        jieba.load_userdict('poemData/txt/content.txt')
        jieba.load_userdict('poemData/txt/dynasty.txt')
        jieba.load_userdict('poemData/txt/poem.txt')
        jieba.load_userdict('poemData/txt/tag.txt')

        list_word = pseg.lcut(question)  # 中文分词
        abstractQuery = ''
        nr_count = 0
        for item in list_word:
            word = item.word
            pos = str(item)
            if 'nm' in pos:  # 诗名
                abstractQuery += "nm "
                self.abstractMap['nm'] = word
            elif 'nr' in pos:  # 人名
                abstractQuery += 'nr'
                self.abstractMap['nr'] = word
            elif 'nt' in pos:  # 朝代
                abstractQuery += "nt "
                self.abstractMap['nt'] = word
            elif 'x' in pos:  # 诗句
                abstractQuery += "x "
                self.abstractMap['x'] = word
            else:
                abstractQuery += word + " "
        return abstractQuery

    def query_classify(self, sentence):
        """
        获取模板索引
        :param sentence:
        :RETURN:
        """
        tmp = np.zeros(len(self.vocab))
        list_sentence = sentence.split(' ')
        for word in list_sentence:
            if word in self.vocab:
                tmp[int(self.vocab[word])] = 1
        model = joblib.load(self.model_path)
        index = model.predict(np.expand_dims(tmp, 0))[0]
        return int(index), self.question_class[index]

    def query_extention(self, temp):
        params = []
        for abs_key in self.abstractMap:
            if abs_key in temp:
                params.append(self.abstractMap[abs_key])
        return params

    def analysis_question(self, question):
        # print('原始句子：{}'.format(question))
        abstr = self.abstract_question(question)
        # print('句子抽象化结果：{}'.format(abstr))
        index, strpatt = self.query_classify(abstr)
        print('句子对应的索引{}\t模板：{}'.format(index, strpatt))
        finalpatt = self.query_extention(strpatt)
        return index, finalpatt


if __name__ == "__main__":
    pqc = PoemQuestionClassifier()
    question = input('请输入你想查询的信息：')
    index, params = pqc.analysis_question(question)
    print(index, params)
