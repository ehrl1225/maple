from PyQt5.QtWidgets import *
import sys

class mywidget(QWidget):

    def __init__(self):
        super().__init__()
        with open("skills.txt","r",encoding='UTF8') as f:
            self.data = [j for i in f.readlines() for j in i.strip("\n").split("|")]
        self.words = [j for i in self.data for j in i.split(" ")]
        self.initUI()

    def initUI(self):
        self.le = QLineEdit()
        self.tb = QTextEdit()

        self.chb = QCheckBox("단어")
        self.chb2 = QCheckBox("줄")

        self.chb.toggle()
        self.chb.released.connect(self.check1)
        self.chb2.released.connect(self.check2)

        self.le.textChanged.connect(self.search)


        hbox = QHBoxLayout()
        hbox.addWidget(self.chb)
        hbox.addWidget(self.chb2)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.le)
        vbox.addWidget(self.tb)

        self.setLayout(vbox)
        self.show()

    def check1(self):
        self.chb2.toggle()
        self.search()

    def check2(self):
        self.chb.toggle()
        self.search()

    def search(self):
        self.tb.clear()
        data = []
        if self.le.text():
            if self.chb.isChecked():
                for i in self.words:
                    if self.le.text() in i:
                        data.append(i)
            else:
                for i in self.data:
                    if self.le.text() in i:
                        data.append(i)
        data = list(set(data))
        for i in data:
            self.tb.append(i)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mywidget()
    sys.exit(app.exec_())