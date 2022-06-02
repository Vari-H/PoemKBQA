from tkinter import *
from tkinter.scrolledtext import ScrolledText

from PIL import Image, ImageTk

from QuestionClassifier import PoemQuestionClassifier
from get_answer import GetAnswer


def resize(w, h, w_box, h_box, pil_image):
    """对一个pil_image对象进行缩放，让它在一个规定的矩形框内保持比例"""
    f1 = 1.0 * w_box / w
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    # print(f1, f2, factor)
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)


class MainWindow:
    def __init__(self):
        # 期望图像显示的大小
        self.w_box = 520
        self.h_box = 320

        # 初始化Tk()
        self.myWindow = Tk()
        self.myWindow.withdraw()
        self.myWindow.iconbitmap(default=r'poemData/favicon.ico')
        self.myWindow.wm_deiconify()

        # 设置标题
        self.myWindow.title('古诗词问答')

        # 设置窗口大小
        self.width = 600
        self.height = 800

        # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        self.screenwidth = self.myWindow.winfo_screenwidth()
        self.screenheight = self.myWindow.winfo_screenheight()
        self.alignstr = '%dx%d+%d+%d' % (self.width, self.height, (self.screenwidth - self.width) / 2, (self.screenheight - self.height) / 2)
        self.myWindow.geometry(self.alignstr)

        # 设置窗口是否可变长、宽，True：可变，False：不可变
        self.myWindow.resizable(width=False, height=False)

        # 创建一个标签，显示图片
        img = Image.open('poemData/cover.jpg')
        w, h = img.size
        img_resize = resize(w, h, self.w_box, self.h_box, img)
        img = ImageTk.PhotoImage(img_resize)
        la1 = Label(self.myWindow, image=img)
        la1.place(x=40, y=20, width=self.w_box)

        la2 = Label(self.myWindow, text='输入你的问题：', font=('宋体 14'))
        la2.place(x=38, y=290)
        self.te1 = ScrolledText(self.myWindow)
        self.te1.place(x=40, y=310, width=self.w_box, height=100)

        la3 = Label(self.myWindow, text='答案：', font=('宋体 14'))
        la3.place(x=38, y=460)
        self.te2 = ScrolledText(self.myWindow)
        self.te2.place(x=40, y=480, width=self.w_box, height=280)

        btn_str = StringVar()
        btn_str.set("开始提问")
        btn = Button(self.myWindow, textvariable=btn_str, command=lambda: self.predict(self.gettext()))
        btn.place(x=250, y=430)
        # 进入消息循环
        self.myWindow.mainloop()

    def gettext(self):
        question = self.te1.get("0.0", END)  # 获取文本框内容
        question = question.replace('\n', '').replace('\r', '').replace(' ', '').strip()
        return question

    def predict(self, question):
        self.te2.delete("0.0", END)
        if not question:
            self.te2.insert("0.0", "请输入问题")
        else:
            print(question)
            index, params = pqc.analysis_question(question)
            try:
                answers = ga.get_data(index, params[0])
            except IndexError:
                self.te2.insert("0.0", "暂时不知道答案")
            else:
                if answers:
                    if index == 0:
                        result = list(set([answer['p.name'] + "\n" for answer in answers]))
                    elif index == 1:
                        result = answers[0]['a.name']
                    elif index == 2:
                        result = list(set([answer['a.name'] + "\n" for answer in answers]))
                    elif index == 3:
                        result = answers[0]['d.name']
                    elif index == 4:
                        lis = []
                        for i in answers:  # 循环list里的每一个元素
                            if i not in lis:  # 判断元素是否存在新列表中，不存在则添加，存在则跳过，以此去重
                                lis.append(i)
                        result = []
                        for item in lis:
                            # 将结果格式化
                            result_str = "《" + item['p.name'] + "》\n\n" + \
                                         item['d.name'] + "·" + item['a.name'] + "\n\n" + \
                                         item['p.content'].replace('。', '。\n').replace('，', '，\n') \
                                             .replace(')', ')\n').replace('？', '？\n') \
                                             .replace('！', '！\n') + "\n" + 30 * "-" + "\n"
                            result.append(result_str)
                    elif index == 5:
                        result = list(set([answer['t.name'] + "\n" for answer in answers]))
                    elif index == 6:
                        lis = []
                        for i in answers:  # 循环list里的每一个元素
                            if i not in lis:  # 判断元素是否存在新列表中，不存在则添加，存在则跳过，以此去重
                                lis.append(i)
                        result = []
                        for item in lis:
                            # 将结果格式化
                            result_str = "出自" + item['d.name'] + "诗人" + item['a.name'] + \
                                         "写作的：" + "《" + item['p.name'] + "》\n\n" + \
                                         "完整内容：\n" + item['p.content'] \
                                             .replace('。', '。\n').replace('，', '，\n') \
                                             .replace(')', ')\n').replace('？', '？\n') \
                                             .replace('！', '！\n') + "\n" + 30 * "-" + "\n"
                            result.append(result_str)
                    else:
                        result = False

                    if result:
                        if isinstance(result, list):
                            for item in result:
                                self.te2.insert(END, item)
                        else:
                            self.te2.insert("0.0", result)
                    else:
                        self.te2.insert("0.0", "暂时不知道答案")
                else:
                    self.te2.insert("0.0", "暂时不知道答案")


if __name__ == '__main__':
    pqc = PoemQuestionClassifier()
    ga = GetAnswer()
    main = MainWindow()


