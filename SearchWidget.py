from PyQt5.QtWidgets import *
from RangedSlider import QRangeSlider
from PyQt5.QtCore import Qt


class SearchWidget(QWidget):

    def __init__(self, guild):
        super().__init__()
        self.guild = guild
        self.initUI()

    def initUI(self):
        self.lb = [QLabel() for i in range(7)]
        self.name = QLineEdit()
        self.position = QComboBox()
        self.level = QRangeSlider()
        self.job = QLineEdit()
        self.mureung = QRangeSlider()
        self.activity = QRangeSlider()
        self.contribution = QRangeSlider()

        self.lt = QListWidget()
        self.tb = QTextBrowser()
        self.btn = QPushButton("clear")

        self.lb[0].setText("닉네임")
        self.lb[1].setText("직위")
        self.lb[2].setText("레벨")
        self.lb[3].setText("직업")
        self.lb[4].setText("무릉")
        self.lb[5].setText("활동일")
        self.lb[6].setText("기여도(10000단위)")
        [self.lb[i].setAlignment(Qt.AlignCenter) for i in range(7)]

        self.position.addItem("모두")
        [self.position.addItem(i) for i in self.guild.position_name]
        self.level.setMax(300)
        self.level.setRange(0,300)
        self.mureung.setMax(80)
        self.mureung.setRange(0,80)
        self.activity.setMax(500)
        self.activity.setRange(0,500)
        self.contribution.setMax(300)
        self.contribution.setRange(0,300)

        self.name.textChanged.connect(self.search)
        self.position.currentIndexChanged.connect(self.search)
        self.level.startValueChanged.connect(self.search)
        self.level.endValueChanged.connect(self.search)
        self.job.textChanged.connect(self.search)
        self.mureung.startValueChanged.connect(self.search)
        self.mureung.endValueChanged.connect(self.search)
        self.activity.startValueChanged.connect(self.search)
        self.activity.endValueChanged.connect(self.search)
        self.contribution.startValueChanged.connect(self.search)
        self.contribution.endValueChanged.connect(self.search)
        self.lt.currentItemChanged.connect(self.info)
        self.btn.pressed.connect(self.lt.clear)
        self.lt.setDragEnabled(True)


        hbox = QHBoxLayout()
        [hbox.addWidget(i) for i in self.lb[:4]]

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.name)
        hbox2.addWidget(self.position)
        hbox2.addWidget(self.level)
        hbox2.addWidget(self.job)

        hbox3 = QHBoxLayout()
        [hbox3.addWidget(i) for i in self.lb[4:]]

        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.mureung)
        hbox4.addWidget(self.activity)
        hbox4.addWidget(self.contribution)

        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.lt)
        hbox5.addWidget(self.tb)

        hbox6=QHBoxLayout()
        hbox6.addWidget(self.btn,1)
        hbox6.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox, 1)
        vbox.addLayout(hbox2, 1)
        vbox.addLayout(hbox3, 1)
        vbox.addLayout(hbox4, 1)
        vbox.addLayout(hbox5, 5)
        vbox.addLayout(hbox6,1)

        self.setLayout(vbox)

    def search(self):
        self.lt.clear()
        data = [[] for i in range(7)]
        for i in self.guild.member:
            text = self.name.text().replace(" ", "")
            if text:
                if text == i.name:
                    data[0].append(i.name)
                else:
                    if text in i.name:
                        data[0].append(i.name)
                    elif i.name in text:
                        data[0].append(i.name)
                    else:
                        rate = 0
                        max_num = min([len(text), len(i.name)])
                        for j in range(max_num):
                            if text[j] == i.name[j]:
                                rate += 1
                        if (rate / max_num) * 100 > 50:
                            data[0].append(i.name)
            else:
                data[0]=self.guild.member_names()

            if self.position.currentIndex() != 0:
                if i.position_id == (self.position.currentIndex() - 1):
                    data[1].append(i.name)
            else:
                data[1]= self.guild.member_names()

            if i.level:
                if self.level.start() < i.level < self.level.end():
                    data[2].append(i.name)
            elif self.level.start()==self.level.min() and self.level.end()==self.level.max():
                data[2]=self.guild.member_names()

            text =self.job.text().replace(" ","")

            if text == i.job:
                data[3].append(i.name)
            elif text=="":
                data[3]=self.guild.member_names()

            if i.mureung:
                if self.mureung.start() < i.mureung < self.mureung.end():
                    data[4].append(i.name)
            elif self.mureung.start()==self.mureung.min() and self.mureung.end()==self.mureung.max():
                data[4]=self.guild.member_names()

            if i.activity:
                text = int(i.activity)
                if self.activity.start() < text < self.activity.end():
                    data[5].append(i.name)
            elif self.activity.start()==self.activity.min() and self.activity.end() == self.activity.max():
                data[5]=self.guild.member_names()

            if i.contribution:
                if self.contribution.start()*10000 < i.contribution < self.contribution.end()*10000:
                    data[6].append(i.name)
            elif self.contribution.start()==self.contribution.min() and self.contribution.end()==self.contribution.max():
                data[6]=self.guild.member_names()

        data2 = list(set(data[0]) & set(data[1]) & set(data[2]) & set(data[3]) & set(data[4]) & set(data[5])
                     & set(data[6]))

        for i in data2:
            self.lt.addItem(i)

    def info(self):
        self.tb.clear()
        if self.lt.currentItem():
            useful = ["닉네임", "직위", "레벨", "직업", "무릉", "활동일", "기여도"]
            member = self.guild[self.lt.currentItem().text()]
            self.tb.append("%s : %s" % (useful[0], member.get_list()[0]))
            self.tb.append("%s : %s" % (useful[1], self.guild.position_name[member.position_id]))
            for i in range(2, 7):
                self.tb.append("%s : %s" % (useful[i], member.get_list()[i]))

    def reset_position(self):
        self.position.clear()
        self.position.addItem("모두")
        for i in self.guild.position_name:
            self.position.addItem(i)

    def set_font(self,font):
        [self.lb[i].setFont(font) for i in range(7)]
        self.name.setFont(font)
        self.position.setFont(font)
        self.level.setFont(font)
        self.job.setFont(font)
        self.mureung.setFont(font)
        self.activity.setFont(font)
        self.contribution.setFont(font)
        self.lt.setFont(font)
        self.tb.setFont(font)
        self.btn.setFont(font)


if __name__ == '__main__':
    from Guild import Guild
    import sys

    guild = Guild()
    guild.name = "미리"
    guild.server = "arcane"
    guild.get_guild_data(guild.server, guild.name)
    app = QApplication(sys.argv)
    ex = SearchWidget(guild)
    ex.show()
    sys.exit(app.exec_())
