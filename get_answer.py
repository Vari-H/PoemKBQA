from py2neo import *


class GetAnswer:
    def __init__(self):
        self.graph = Graph("http://localhost:7474", auth=("neo4j", "123456"))

    def get_data(self, index, param):
        query = ''
        if index == 0:
            # 某人写过什么诗
            query = "MATCH (a:Author)-[:Author_THE_Poem]->(p:Poem) WHERE a.name='{}' RETURN p.name;".format(param)
        elif index == 1:
            # 某诗是某人写的
            query = "MATCH (p:Poem)-[:Poem_IS_Author]->(a:Author) WHERE p.name='{}' RETURN a.name;".format(param)
        elif index == 2:
            # 某朝代有哪些诗人
            query = "MATCH (d:Dynasty)-[:Dynasty_THE_Author]->(a:Author) WHERE d.name='{}' RETURN a.name;".format(param)
        elif index == 3:
            # 某诗人生活在哪个朝代
            query = "MATCH (a:Author)-[:Author_IS_Dynasty]->(d:Dynasty) WHERE a.name='{}' RETURN d.name;".format(param)
        elif index == 4:
            # 按诗名查询某诗内容
            query = "MATCH (p:Poem)-[:Poem_IS_Author]->(a:Author)-[:Author_IS_Dynasty]->(d:Dynasty) " \
                    "WHERE p.name='{}' RETURN p.name,d.name,a.name,p.content;".format(param)
        elif index == 5:
            # 某诗属于某风格
            query = "MATCH (p:Poem)-[:Poem_IS_Tag]->(t:Tag) WHERE p.name='{}' RETURN t.name;".format(param)
        elif index == 6:
            # 某诗句出自某朝代某诗人写作的某诗
            query = "MATCH (p:Poem)-[:Poem_IS_Author]->(a:Author)-[:Author_IS_Dynasty]->(d:Dynasty) " \
                    "WHERE p.content=~'.*{}.*' RETURN d.name,a.name,p.name, p.content;".format(param)
        result = self.graph.run(query).data()
        return result


if __name__ == "__main__":
    ga = GetAnswer()
    answers = ga.get_data(0, '李白')
    for answer in answers:
        print(answer[0])
