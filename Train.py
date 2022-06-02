import json
import os
import re

import jieba
import joblib
import numpy as np
from sklearn.naive_bayes import GaussianNB


class GenerPoemClassification:
    def __init__(self):
        self.poem_classification_path = "model/poem_classification.json"
        if not os.path.isfile(self.poem_classification_path):
            self.save_vocab()

    def save_vocab(self):
        """这部分 dict 需要和训练数据顺序对应"""
        dic = {'0': 'nr 某人写过什么诗',
               '1': 'nm 某诗是某人写的',
               '2': 'nt 某朝代有哪些诗人',
               '3': 'nr 某诗人生活在哪个朝代',
               '4': 'nm 按诗名查询某诗内容',
               '5': 'nm 某诗描写某标签',
               '6': 'x 某诗句出自某朝代某诗人写作的某诗',
               }
        with open(self.poem_classification_path, 'w', encoding='utf8') as f:
            json.dump(dic, f, ensure_ascii=False)
        print("保存分类成功")


class GenerVocab:
    """生成所有训练数据的vocab文件, 使用模型的时候需要. 变更数据的时候需要重新生成."""

    def __init__(self):
        self.data_path = "./poemData/trainData"
        self.save_vocab_path = "model/vocabulary.json"
        if not os.path.isfile(self.save_vocab_path):
            self.save_vocab()

    def cut_word(self, file_path):
        result_list = []
        with open(file_path, "r", encoding='utf8') as temp_f:
            for sentence in temp_f.readlines():
                sentence = sentence.strip()
                temp = jieba.lcut(sentence)
                result_list += temp
        return result_list

    def get_all_word(self):
        all_word_list = []
        for path in os.listdir(self.data_path):
            file_path = os.path.join(self.data_path, path)
            result_word_list = self.cut_word(file_path)
            all_word_list += result_word_list
        all_word_set = set(all_word_list)
        result_dict = {}
        for index, cont in enumerate(all_word_set):
            result_dict[cont] = index
        return result_dict

    def save_vocab(self):
        dic = self.get_all_word()
        with open(self.save_vocab_path, 'w', encoding='utf8') as f:
            json.dump(dic, f, ensure_ascii=False)


class Trainer(GenerVocab):
    def __init__(self):
        super().__init__()
        self.vocab = self.load_vocab()

    def load_vocab(self):
        with open(self.save_vocab_path, "r", encoding='utf-8') as f:
            vocab = json.loads(f.read())
        return vocab

    def load_data(self):
        X = []
        Y = []
        list_file = os.listdir(self.data_path)
        for file_name in list_file:
            file_path = os.path.join(self.data_path, file_name)
            result = re.match('【[0-9]*】', file_name).span()
            start = result[0]
            end = result[1]
            with open(file_path, 'r', encoding='utf-8') as fread:
                for line in fread:
                    tmp = np.zeros(len(self.vocab))
                    Y.append(file_name[start + 1:end - 1])  # label
                    list_sentence = jieba.lcut(line.rstrip())
                    for word in list_sentence:
                        if word in self.vocab:
                            tmp[int(self.vocab[word])] = 1
                    X.append(tmp)
        return X, Y

    def train(self):
        X, Y = self.load_data()
        model = GaussianNB().fit(X, Y)
        joblib.dump(model, 'model/model.model')


if __name__ == "__main__":
    gpc = GenerPoemClassification()
    t = Trainer()
    t.train()
