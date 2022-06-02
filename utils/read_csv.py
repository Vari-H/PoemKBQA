import csv


def read_csv(path):
    csvFile = open(path, "r", encoding='utf-8')
    reader = csv.reader(csvFile)

    author_to_dynasty = []  # 作者与朝代的关系
    dynasty_to_author = []  # 朝代与作者的关系

    author_to_title = []  # 作者和诗(题目)的关系
    title_to_author = []  # 诗(题目)和作者的关系

    title_to_dynasty = []  # 诗(题目)和朝代的关系
    dynasty_to_title = []  # 朝代和诗(题目)的关系

    poem_to_tag = []  # 诗和标签的关系
    tag_to_poem = []  # 标签和诗的关系

    poem_to_content = []

    poem_info = []  # 诗的info
    author_info = []
    dynasty_info = []
    tag_info = []
    name_info = []
    content_info = []

    for item in reader:
        poem_dict = {"name": item[2], "content": item[3], "tag": item[4]}

        tag_info.append(item[4])
        dynasty_info.append(item[1])
        author_info.append(item[0])
        name_info.append(item[2])
        content_info.append(item[3])

        author_to_dynasty.append([item[0], item[1]])
        dynasty_to_author.append([item[1], item[0]])

        author_to_title.append([item[0], item[2]])
        title_to_author.append([item[2], item[0]])

        dynasty_to_title.append([item[1], item[2]])
        title_to_dynasty.append([item[2], item[1]])

        poem_to_tag.append([item[2], item[4]])
        tag_to_poem.append([item[4], item[2]])

        poem_to_content.append([item[2], item[3]])

        poem_info.append(poem_dict)
    csvFile.close()
    return set(author_info), set(dynasty_info), set(tag_info), set(name_info), set(content_info), \
           author_to_dynasty, dynasty_to_author, author_to_title, title_to_author, \
           dynasty_to_title, title_to_dynasty, poem_to_tag, tag_to_poem, \
           poem_to_content, poem_info
