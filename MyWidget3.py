from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class mywidget3(QWidget):

    def __init__(self, guild):
        super().__init__()

        self.lb = QLabel("길드마스터")
        self.lb2 = QLabel("부마스터")
        self.lb3 = QLabel("길드원1")
        self.lb4 = QLabel("길드원2")
        self.lb5 = QLabel("길드원3")
        self.guild = guild
        self.le = QLineEdit()
        self.le2 = QLineEdit()
        self.le3 = QLineEdit()
        self.le4 = QLineEdit()
        self.le5 = QLineEdit()
        self.le6 = QLineEdit()
        self.cb = QComboBox()
        self.lt = QListWidget()
        self.btn = QPushButton("적용")
        self.btn2 = QPushButton("add")
        self.btn3 = QPushButton("del")

        self.initui()

    def initui(self):
        self.le.returnPressed.connect(self.add)
        self.le2.returnPressed.connect(self.add)
        self.le3.returnPressed.connect(self.add)
        self.le4.returnPressed.connect(self.add)
        self.le5.returnPressed.connect(self.add)
        self.btn.pressed.connect(self.add)

        self.le6.returnPressed.connect(self.add_std)
        self.btn2.pressed.connect(self.add_std)

        self.btn3.pressed.connect(self.del_std)

        self.lt.itemDoubleClicked.connect(self.get_std)

        for i in self.guild.g_po_name():
            self.cb.addItem(i)

        if self.guild.g_po_std():
            for i in self.guild.g_po_std():
                self.lt.addItem("닉네임 : %s\n직위 : %s" % (i[0], i[1]))

        self.le.setText(self.guild.g_po_name()[0])
        self.le2.setText(self.guild.g_po_name()[1])
        self.le3.setText(self.guild.g_po_name()[2])
        self.le4.setText(self.guild.g_po_name()[3])
        self.le5.setText(self.guild.g_po_name()[4])

        hbox1_1 = QHBoxLayout()
        hbox1_1.addWidget(self.lb)
        hbox1_1.addWidget(self.le)

        hbox1_2 = QHBoxLayout()
        hbox1_2.addWidget(self.lb2)
        hbox1_2.addWidget(self.le2)

        hbox1_3 = QHBoxLayout()
        hbox1_3.addWidget(self.lb3)
        hbox1_3.addWidget(self.le3)

        hbox1_4 = QHBoxLayout()
        hbox1_4.addWidget(self.lb4)
        hbox1_4.addWidget(self.le4)

        hbox1_5 = QHBoxLayout()
        hbox1_5.addWidget(self.lb5)
        hbox1_5.addWidget(self.le5)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1_1)
        vbox.addLayout(hbox1_2)
        vbox.addLayout(hbox1_3)
        vbox.addLayout(hbox1_4)
        vbox.addLayout(hbox1_5)
        vbox.addWidget(self.btn)

        hbox2_2 = QHBoxLayout()
        hbox2_2.addWidget(self.le6)
        hbox2_2.addWidget(self.cb)

        hbox2_3 = QHBoxLayout()
        hbox2_3.addWidget(self.btn2)
        hbox2_3.addWidget(self.btn3)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.lt)
        vbox2.addLayout(hbox2_2)
        vbox2.addLayout(hbox2_3)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addLayout(vbox2)
        hbox.addLayout(vbox2)

        self.setLayout(hbox)
        self.setGeometry(450, 300, 400, 200)

    def add(self):
        if self.le.text() != "" and self.le2.text() != "" and self.le3.text() != "" and self.le4.text() != "" and self.le5.text() != "":
            self.guild.guild_info[7] = "%s %s %s %s %s" % (
                self.le.text(), self.le2.text(), self.le3.text(), self.le4.text(), self.le5.text())
            self.cb.clear()
            for i in self.guild.g_po_name():
                self.cb.addItem(i)
            self.guild.save_info()

    def reset_lt(self):
        self.lt.clear()
        if self.guild.g_po_std():
            for i in self.guild.g_po_std():
                self.lt.addItem("닉네임 : %s\n직위 : %s" % (i[0], i[1]))

    def add_std(self):
        if self.le6.text()!="":
            if self.guild.g_po_std():
                self.guild.guild_info[8] = "%s %s:%s" % (
                    self.guild.guild_info[8], self.le6.text(), self.cb.currentText())
            else:
                self.guild.guild_info[8] = "%s:%s" % (self.le6.text(), self.cb.currentText())
            self.guild.save_info()
            self.reset_lt()

    def del_std(self):
        std_name = []
        if self.guild.g_po_std():
            for i in self.guild.g_po_std():
                std_name.append(i[0])
            if self.le6.text() in std_name:
                std = self.guild.guild_info[8].split(" ")
                del std[std_name.index(self.le6.text())]
                new_std = ""
                if std != []:
                    for i in std:
                        new_std += i + " "
                    self.guild.guild_info[8] = new_std.strip(" ")
                else:
                    self.guild.guild_info[8] = "?"
                self.guild.save_info()
            self.reset_lt()

    def get_std(self):
        self.le6.setText(self.lt.currentItem().text().split("\n")[0].split(" : ")[1])

    def set_font(self, font):
        self.lb.setFont(font)
        self.lb2.setFont(font)
        self.lb3.setFont(font)
        self.lb4.setFont(font)
        self.lb5.setFont(font)
        self.le.setFont(font)
        self.le2.setFont(font)
        self.le3.setFont(font)
        self.le4.setFont(font)
        self.le5.setFont(font)
        self.cb.setFont(font)
        self.lt.setFont(font)
        self.btn.setFont(font)
        self.btn2.setFont(font)
        self.btn3.setFont(font)