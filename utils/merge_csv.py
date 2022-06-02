import glob

csv_list = glob.glob(r'..\poemData\csv\*.csv')  # 查看同文件夹下的csv文件数
print(u'共发现%s个CSV文件' % len(csv_list))

for i in csv_list:  # 循环读取同文件夹下的csv文件
    fr = open(i, 'rb').read()
    with open(r'..\poemData\csv\all.csv', 'ab') as f:  # 将结果保存为all.csv
        f.write(fr)
print(u'合并完毕！')
