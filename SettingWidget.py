from PyQt5.QtWidgets import *


class SettingWidget(QWidget):

    def __init__(self, guild,wg):
        super().__init__()
        self.guild = guild
        self.mywidget=wg
        self.initUI()

    def initUI(self):
        self.lb = [QLabel() for i in range(2)]
        self.lb2 = [QLabel() for i in range(2)]
        self.lb3 = [QLabel() for i in range(5)]
        self.lb4 = [QLabel() for i in range(3)]

        self.le = [QLineEdit() for i in range(2)]
        self.le2 = [QLineEdit() for i in range(2)]
        self.le3 = [QLineEdit() for i in range(6)]

        self.btn = QPushButton("저장")
        self.btn2 = QPushButton("적용")
        self.btn3 = [QPushButton() for i in range(3)]

        self.cb = QComboBox()

        self.chb = [QCheckBox() for i in range(3)]

        self.tw = QTableWidget()

        self.lb[0].setText("서버")
        self.lb[1].setText("길드 이름")

        self.lb2[0].setText("ID")
        self.lb2[1].setText("Password")

        self.lb3[0].setText("길드마스터")
        self.lb3[1].setText("부마스터")
        self.lb3[2].setText("길드원1")
        self.lb3[3].setText("길드원2")
        self.lb3[4].setText("길드원3")

        if self.guild.server:
            self.le[0].setText(self.guild.server)
        if self.guild.name:
            self.le[1].setText(self.guild.name)
        for i in range(5):
            if self.guild.position_name[i]:
                self.le3[i].setText(self.guild.position_name[i])

        [self.le[i].returnPressed.connect(self.get_guild_data) for i in range(2)]
        self.le2[1].setEchoMode(2)
        if self.guild.account:
            self.le2[0].setText(self.guild.account)
        if self.guild.password:
            self.le2[1].setText(self.guild.password)

        self.btn.pressed.connect(self.get_guild_data)
        self.btn2.pressed.connect(self.save_account)

        self.tw.setColumnCount(2)
        self.tw.setHorizontalHeaderLabels(["닉네임", "계급"])
        self.reset_tw()

        self.chb[0].setText("넥슨")
        self.chb[1].setText("메이플")
        self.chb[2].setText("비번 보기")
        self.chb[0].toggle()
        self.chb[0].released.connect(self.check1)
        self.chb[1].released.connect(self.check2)
        self.chb[2].released.connect(self.check3)

        [self.le3[i].returnPressed.connect(self.add_po) for i in range(5)]
        self.btn2.pressed.connect(self.save_account)

        self.le3[5].returnPressed.connect(self.add_po_std)
        self.btn3[0].setText("적용")
        self.btn3[1].setText("add")
        self.btn3[2].setText("del")
        self.btn3[0].pressed.connect(self.add_po)
        self.btn3[1].pressed.connect(self.add_po_std)
        self.btn3[2].pressed.connect(self.del_po_std)

        [self.cb.addItem(i) for i in self.guild.position_name]

        #
        hbox = QHBoxLayout()
        [hbox.addWidget(self.lb[i]) for i in range(2)]

        hbox2 = QHBoxLayout()
        [hbox2.addWidget(self.le[i]) for i in range(2)]

        hbox3 = QHBoxLayout()
        [hbox3.addWidget(self.chb[i]) for i in range(2)]

        hbox4 = QHBoxLayout()
        [hbox4.addWidget(self.lb2[i]) for i in range(2)]

        hbox5 = QHBoxLayout()
        [hbox5.addWidget(self.le2[i]) for i in range(2)]

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.btn)
        vbox.addWidget(self.lb4[0])

        #
        vbox2 = QVBoxLayout()
        vbox2.addLayout(hbox3)
        vbox2.addLayout(hbox4)
        vbox2.addWidget(self.chb[2])
        vbox2.addLayout(hbox5)
        vbox2.addWidget(self.btn2)
        vbox2.addWidget(self.lb4[1])

        #
        hbox6 = QHBoxLayout()
        hbox6.addLayout(vbox)
        hbox6.addLayout(vbox2)

        #
        vbox2 = QVBoxLayout()
        [vbox2.addWidget(self.lb3[i]) for i in range(5)]

        vbox3 = QVBoxLayout()
        [vbox3.addWidget(self.le3[i]) for i in range(5)]

        hbox7 = QHBoxLayout()
        hbox7.addLayout(vbox2)
        hbox7.addLayout(vbox3)

        vbox4 = QVBoxLayout()
        vbox4.addLayout(hbox7)
        vbox4.addWidget(self.btn3[0])
        vbox4.addWidget(self.lb4[2])

        #
        hbox8 = QHBoxLayout()
        hbox8.addWidget(self.cb)
        hbox8.addWidget(self.le3[5])

        hbox9 = QHBoxLayout()
        hbox9.addWidget(self.btn3[1])
        hbox9.addWidget(self.btn3[2])

        vbox5 = QVBoxLayout()
        vbox5.addWidget(self.tw)
        vbox5.addLayout(hbox8)
        vbox5.addLayout(hbox9)

        hbox10 = QHBoxLayout()
        hbox10.addLayout(vbox4)
        hbox10.addLayout(vbox5)

        #
        main_vbox = QVBoxLayout()
        main_vbox.addLayout(hbox6)
        main_vbox.addLayout(hbox10)

        self.setLayout(main_vbox)

    def get_guild_data(self):
        if not self.mywidget.updating:
            self.guild.server = self.le[0].text()
            self.guild.name = self.le[1].text()
            if self.guild.get_guild_data(self.le[0].text(), self.le[1].text()):
                self.lb4[0].setText("적용되었습니다.")
            else:
                self.lb4[0].setText("다시 확인해 주세요")
            self.guild.save_as_file()
        else:
            self.lb4[0].setText("잠시 기다려 주세요")

    def save_account(self):
        if not self.mywidget.updating:
            if self.chb[0].isChecked():
                self.guild.account_type = 0
            else:
                self.guild.account_type = 1
            if (self.le2[0].text() != "") and (self.le2[1].text() != ""):
                self.guild.account = self.le2[0].text()
                self.guild.password = self.le2[1].text()
                self.guild.save_as_file()
                self.lb4[1].setText("적용되었습니다.")
            else:
                self.lb4[1].setText("적어놓으세요.")
        else:
            self.lb4[1].setText("잠시 기다려 주세요")

    def check1(self):
        self.chb[1].toggle()

    def check2(self):
        self.chb[0].toggle()

    def check3(self):
        if self.chb[2].isChecked():
            self.le2[1].setEchoMode(0)
        else:
            self.le2[1].setEchoMode(2)

    def add_po(self):
        if not self.mywidget.updating:
            po = [self.le3[i].text() for i in range(5)]
            if "" not in po:
                self.guild.position_name = po
            self.cb.clear()
            for i in self.guild.position_name:
                self.cb.addItem(i)
            self.guild.save_as_file()
            self.mywidget.search_widget_set_po()
            self.lb4[2].setText("적용되었습니다.")
        else:
            self.lb4[2].setText("잠시 기다려 주세요")

    def add_po_std(self):
        if not self.mywidget.updating:
            if self.le3[5].text():
                if self.guild.position_standard:
                    self.guild.position_standard.append([self.le3[5].text(), str(self.cb.currentIndex())])
                else:
                    self.guild.position_standard = [[self.le3[5].text(), str(self.cb.currentIndex())]]
                self.guild.save_as_file()
                self.reset_tw()

    def del_po_std(self):
        if not self.mywidget.updating:
            if self.guild.position_standard:
                for i in range(len(self.guild.position_standard)):
                    if self.guild.position_standard[i][0] == self.le3[5].text():
                        del self.guild.position_standard[i]
                self.guild.save_as_file()
                self.reset_tw()

    def reset_tw(self):
        if self.guild.position_standard:
            self.tw.setRowCount(len(self.guild.position_standard))
            for i in range(len(self.guild.position_standard)):
                self.tw.setItem(i, 0, QTableWidgetItem(self.guild.position_standard[i][0]))
                self.tw.setItem(i, 1, QTableWidgetItem(self.guild.position_name[int(self.guild.position_standard[i][1])]))

    def set_font(self,font):
        [self.lb[i].setFont(font) for i in range(2)]
        [self.lb2[i].setFont(font) for i in range(2)]
        [self.lb3[i].setFont(font) for i in range(5)]
        [self.lb4[i].setFont(font) for i in range(3)]
        [self.le[i].setFont(font) for i in range(2)]
        [self.le2[i].setFont(font) for i in range(2)]
        self.btn.setFont(font)
        self.btn2.setFont(font)
        [self.btn3[i].setFont(font) for i in range(3)]
        self.cb.setFont(font)
        [self.chb[i].setFont(font) for i in range(3)]
        self.tw.setFont(font)

