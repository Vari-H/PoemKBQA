import re

from utils.read_csv import read_csv


def split_sentences(line):
    line_split = re.split(r'[。！；？，]', line.strip())
    line_split = [line.strip() for line in line_split if
                  line.strip() not in ['。', '！', '？', '；', '，'] and len(line.strip()) > 1]
    return line_split


def export_data(csv_path):
    author, dynasty, tag, poem_name, content, rel_a_d, rel_d_a, rel_a_t, rel_t_a, rel_d_t, rel_t_d, rel_p_t, rel_t_p, \
    rel_p_c, rel_info = read_csv(csv_path)

    author = [x + " 3 nr" for x in list(author)]
    dynasty = [x + " 3 nt" for x in list(dynasty)]
    tag = [x + " 3 nz" for x in list(tag)]
    poem_name = [x + " 3 nm" for x in list(poem_name)]
    content = [x.strip() for x in list(content) if x.strip() != '']
    content_split = []
    for item in content:
        result = split_sentences(item)
        content_split += result
    content_split = [x + " x" for x in content_split]
    file_author = open("poemData/txt/author.txt", 'w+', encoding='utf-8')
    file_poem = open("poemData/txt/poem.txt", 'w+', encoding='utf-8')
    file_dynasty = open("poemData/txt/dynasty.txt", 'w+', encoding='utf-8')
    file_tag = open("poemData/txt/tag.txt", 'w+', encoding='utf-8')
    file_content = open("poemData/txt/content.txt", 'w+', encoding='utf-8')

    file_author.write('\n'.join(author))
    file_poem.write('\n'.join(poem_name))
    file_dynasty.write('\n'.join(dynasty))
    file_tag.write('\n'.join(tag))
    file_content.write('\n'.join(content_split))

    file_author.close()
    file_poem.close()
    file_tag.close()
    file_dynasty.close()

# if __name__ == '__main__':
#     path = '../poemData/csv/all.csv'
#     export_data(path)
