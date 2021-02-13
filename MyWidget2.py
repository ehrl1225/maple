from PyQt5.QtWidgets import QLabel, QLineEdit, QCheckBox ,QPushButton, QHBoxLayout, QVBoxLayout, QWidget


class mywidget2(QWidget):

    def __init__(self, guild):
        super().__init__()
        self.guild = guild
        self.initui()

    def initui(self):
        self.lb1 = QLabel("ID", self)
        self.lb2 = QLabel("Password", self)

        self.le1 = QLineEdit()
        self.le1.returnPressed.connect(self.saveaccount)
        self.le2 = QLineEdit()
        self.le2.returnPressed.connect(self.saveaccount)
        self.le2.setEchoMode(2)
        if self.guild.g_account() != "?":
            self.le1.setText(self.guild.account)
        if self.guild.g_passwd() != "?":
            self.le2.setText(self.guild.password)

        self.chb1 = QCheckBox('넥슨', self)
        self.chb2 = QCheckBox('메이플', self)
        self.chb3 = QCheckBox("비번 보기")
        self.chb1.released.connect(self.check1)
        self.chb1.toggle()
        self.chb2.released.connect(self.check2)
        self.chb3.released.connect(self.check3)
        self.btn = QPushButton("적용")
        self.btn.pressed.connect(self.saveaccount)

        hbox = QHBoxLayout()
        hbox.addWidget(self.lb1, 1)
        hbox.addWidget(self.le1, 2)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.lb2, 1)
        hbox2.addWidget(self.le2, 2)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(self.chb1, 1)
        hbox3.addWidget(self.chb2, 1)
        hbox3.addWidget(self.chb3,1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.btn)

        self.setLayout(vbox)

        self.setGeometry(450, 300, 250, 100)

    def saveaccount(self):
        stat = None
        if self.chb1.isChecked():
            self.guild.account_type=0
        else:
            self.guild.account_type=1
        if (self.le1.text()!="") and (self.le2.text()!=""):
            self.guild.account = self.le1.text()
            self.guild.password = self.le2.text()
            self.guild.save_as_file()
            self.hide()

    def check1(self):
        self.chb2.toggle()

    def check2(self):
        self.chb1.toggle()
    def check3(self):
        if self.chb3.isChecked():
            self.le2.setEchoMode(0)
        else:
            self.le2.setEchoMode(2)

    def set_font(self, font):
        self.lb1.setFont(font)
        self.lb2.setFont(font)
        self.le1.setFont(font)
        self.le2.setFont(font)
        self.chb1.setFont(font)
        self.chb2.setFont(font)
        self.chb3.setFont(font)
        self.btn.setFont(font)