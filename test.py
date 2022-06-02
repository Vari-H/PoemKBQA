from QuestionClassifier import PoemQuestionClassifier
from get_answer import GetAnswer

if __name__ == "__main__":
    pqc = PoemQuestionClassifier()
    ga = GetAnswer()
    while True:
        question = input('请输入你想查询的信息：')
        index, params = pqc.analysis_question(question)
        # print(index, params)
        try:
            answers = ga.get_data(index, params[0])
        except IndexError:
            print("暂时不知道答案")
            continue
        print('答案:')
        if index == 0:
            result = list(set([answer['p.name'] for answer in answers]))
        elif index == 1:
            result = answers[0]['a.name']
        elif index == 2:
            result = list(set([answer['a.name'] for answer in answers]))
        elif index == 3:
            result = answers[0]['d.name']
        elif index == 4:
            result = answers[0]['p.content']
        elif index == 5:
            result = list(set([answer['t.name'] for answer in answers]))
        elif index == 6:
            lis = []
            for i in answers:  # 循环list里的每一个元素
                if i not in lis:  # 判断元素是否存在新列表中，不存在则添加，存在则跳过，以此去重
                    lis.append(i)
            result = []
            for item in lis:
                dic = {
                    "Dynasty": item['d.name'],
                    "Author": item['a.name'],
                    "poem_name": item['p.name'],
                    "poem_content": item['p.content']
                }
                result.append(dic)
        else:
            result = False

        if result:
            print(result)
        else:
            print("暂时不知道答案")
