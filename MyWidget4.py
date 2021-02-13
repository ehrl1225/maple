from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class mywidget4(QWidget):

    def __init__(self, guild):
        super().__init__()
        self.guild = guild
        self.initui()

    def initui(self):
        self.le = QLineEdit()
        self.cb = QComboBox()
        self.lt = QListWidget()
        self.tb = QTextBrowser()
        self.lb = QLabel("0명")

        self.le.textChanged.connect(self.search)
        self.cb.addItem("닉네임")
        self.cb.addItem("직위")
        self.cb.addItem("레벨")
        self.cb.addItem("직업")
        self.cb.addItem("무릉 층수")
        self.cb.addItem("활동일")
        self.cb.addItem("기여도")
        self.cb.currentIndexChanged.connect(self.cb_change)
        self.lt.currentItemChanged.connect(self.show_item)
        self.lb.setAlignment(Qt.AlignCenter)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.le, 1)
        hbox1.addWidget(self.cb, 1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.lb, 1)
        hbox2.addStretch(1)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.lt, 1)
        hbox3.addWidget(self.tb, 1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        self.setLayout(vbox)

    def cb_change(self):
        self.search()

    def search(self):
        self.lt.clear()
        text = self.le.text().replace(" ", "")
        if text != "":
            if self.cb.currentIndex() == 0:
                if text in self.guild.member_names():
                    self.lt.addItem(text)
                else:
                    for i in self.guild.member_names():
                        if text in i:
                            self.lt.addItem(i)
                        elif i in text:
                            self.lt.addItem(i)
                        else:
                            rate = 0
                            if len(text) > len(i):
                                max_num = len(i)
                            else:
                                max_num = len(text)
                            for j in range(max_num):
                                if text[j] == i[j]:
                                    rate += 1
                            if (rate / max_num) * 100 > 50:
                                self.lt.addItem(i)

            elif self.cb.currentIndex() == 1:
                if text in self.guild.g_po_name():
                    for i in self.guild.guild:
                        if i[1] == text:
                            self.lt.addItem(i[0])
                elif text in ["길드마스터", "부마스터", "길드원1", "길드원2", "길드원3"]:
                    default = ["길드마스터", "부마스터", "길드원1", "길드원2", "길드원3"]
                    for i in self.guild.guild:
                        num1=self.guild.g_po_name().index(i[1])
                        num2=default.index(text)
                        if num1==num2:
                            self.lt.addItem(i[0])
                elif text in ["길마", "부마", "길원1", "길원2", "길원3"]:
                    default = ["길마", "부마", "길원1", "길원2", "길원3"]
                    for i in self.guild.guild:
                        num1 = self.guild.g_po_name().index(i[1])
                        num2 = default.index(text)
                        if num1 == num2:
                            self.lt.addItem(i[0])

            elif self.cb.currentIndex() == 3:
                job = sorted(list(set(self.guild.job())))
                if text in job:
                    for i in self.guild.guild:
                        if i[3] == text:
                            self.lt.addItem(i[0])

            elif self.cb.currentIndex() in [2, 4, 5, 6]:
                cb_num = self.cb.currentIndex()
                text = text.replace("~", ":")
                if text.isdecimal():
                    if self.cb.currentIndex() == 2:
                        if text != "":
                            text = "Lv." + text
                    elif self.cb.currentIndex() == 5:
                        if text != "":
                            text = text + "일 전"
                    for i in self.guild.guild:
                        if text == i[cb_num]:
                            self.lt.addItem(i[0])
                elif ":" in text:
                    text = text.split(":")

                    data = []
                    for i in self.guild.guild:
                        data.append(i[cb_num])

                    for i in [0, 1]:
                        if self.cb.currentIndex() == 2:
                            if text[i] != "":
                                text[i] = "Lv." + text[i]
                        elif self.cb.currentIndex() == 5:
                            if text[i] != "":
                                text[i] = text[i] + "일 전"
                        data.append(text[i])
                    data = list(set(data))
                    data = sorted(data, key=lambda x: int(x.replace("Lv.",
                                                                    "").replace("일 전", "")) if x.replace("Lv.",
                                                                                                         "").replace(
                        "일 전", "").isdecimal() else 0)
                    if text[0] != "":
                        for i in range(len(data)):
                            if text[0] == data[i]:
                                data = data[i:]
                                break
                    if text[1] != "" and text[1] != data[-1].replace("Lv.", "").replace("일 전", ""):
                        for i in range(len(data)):
                            if text[1] == data[i]:
                                data = data[:i + 1]
                                break
                    for i in data:
                        for j in self.guild.guild:
                            if i == j[cb_num]:
                                self.lt.addItem(j[0])
        self.lb.setText("%d 명" % self.lt.count())

    def show_item(self):
        self.tb.clear()
        if self.lt.currentItem():
            if self.lt.currentItem().text() in self.guild.name():
                num = self.guild.number(self.lt.currentItem().text())
                self.tb.append("닉네임 : %s" % self.guild.guild[num][0])
                self.tb.append("직위 : %s" % self.guild.guild[num][1])
                self.tb.append("레벨 : %s" % self.guild.guild[num][2])
                self.tb.append("직업 : %s" % self.guild.guild[num][3])
                self.tb.append("무릉층수 : %s" % self.guild.guild[num][4])
                self.tb.append("활동일 : %s" % self.guild.guild[num][5])
                self.tb.append("기여도 : %s" % self.guild.guild[num][6])

    def set_font(self, font):
        self.le.setFont(font)
        self.cb.setFont(font)
        self.lt.setFont(font)
        self.tb.setFont(font)
        self.lb.setFont(font)
