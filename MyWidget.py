from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Guild import Guild
from SettingWidget import SettingWidget
from SearchWidget import SearchWidget
from Worker import worker
from MyTable import MyTable
import clipboard

class MyWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.guild = Guild()
        self.guild.load_as_file()

        self.setting_wg = SettingWidget(self.guild,self)
        self.search_wg = SearchWidget(self.guild)

        self.updating = False

        # 닉네임 검색용
        self.le = QLineEdit()
        # 클립보드용
        self.le2 = QLineEdit()
        # 캐릭터 표시
        self.lb = QLabel()
        # 길드 이름 표시
        self.lb2 = QLabel("길드 : %s" % self.guild.name)
        self.lb3 = [QLabel() for i in range(3)]
        # 닉네임 검색
        self.cb = QComboBox()
        # 닉네임 검색
        self.tb = QTextBrowser()

        self.tb2 = QTextBrowser()
        self.tb3 = QTextBrowser()
        self.tb4 = QTextBrowser()
        # 업데이트 버튼
        self.btn = QPushButton("길드원 정보 가져오기")
        # 비우기
        self.btn2 = QPushButton("clear")
        #닉네임 복사
        self.btn3= QPushButton("닉네임 복사")
        #정렬
        self.btn4 = [QPushButton() for i in range(7)]
        self.btn5 = QPushButton("↑")
        # 클립보드
        self.copy_btn = QPushButton("복사")
        # 길드 표시
        self.tw = MyTable()
        self.step = 0
        # 표시 범위
        self.chb = [QCheckBox() for i in range(7)]
        #프로그레스
        self.pbar = QProgressBar()
        self.pbar.setMaximum(100)
        self.pbar.setValue(0)

        self.worker = None

        self.initUI()

    def initUI(self):
        useful = ["닉네임", "직위", "레벨", "직업", "무릉", "활동일", "기여도"]
        self.le.textChanged.connect(self.search)
        self.lb.resize(100, 100)
        self.le2.textChanged.connect(self.divide_str)
        self.lb.setStyleSheet("color: blue;"
                              "background-color: #87CEFA;"
                              "border-style: dashed;"
                              "border-width: 3px;"
                              "border-color: #1E90FF")
        self.lb2.setStyleSheet("border-style: dashed;"
                               "border-width: 2px;"
                               "border-radius: 3px")

        self.lb.setAlignment(Qt.AlignCenter)
        self.lb2.setAlignment(Qt.AlignCenter)
        self.btn.pressed.connect(self.update)
        self.btn2.pressed.connect(self.tw_clear)
        self.btn3.pressed.connect(self.copy)
        [self.btn4[i].setText(useful[i]+self.btn5.text()) for i in range(7)]
        [self.btn4[i].pressed.connect(lambda button=self.btn4[i]: self.sort_guild(button)) for i in range(7)]
        self.btn5.pressed.connect(self.up_down)
        self.btn5.setMaximumWidth(20)
        self.cb.currentIndexChanged.connect(self.combo)
        self.reset_tw()
        #self.update()
        #self.guild_info()

        hbox1_1_1 = QHBoxLayout()
        hbox1_1_1.addWidget(self.le, 1)
        hbox1_1_1.addWidget(self.cb, 1)

        hbox1_1_2 = QHBoxLayout()
        hbox1_1_2.addWidget(self.tb, 1)
        hbox1_1_2.addWidget(self.lb, 1)

        vbox1_1 = QVBoxLayout()
        vbox1_1.addLayout(hbox1_1_1, 1)
        vbox1_1.addLayout(hbox1_1_2, 1)

        vbox1_2 = QVBoxLayout()
        vbox1_2.addWidget(self.lb2, 1)
        [vbox1_2.addWidget(i) for i in self.lb3]

        hbox1 = QHBoxLayout()
        hbox1.addLayout(vbox1_1, 2)
        hbox1.addLayout(vbox1_2, 1)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.btn3,1)
        hbox4.addWidget(self.le2, 1)
        hbox4.addWidget(self.btn2, 2)

        hbox5 = QHBoxLayout()
        [hbox5.addWidget(self.btn4[i],4) for i in range(7)]
        hbox5.addWidget(self.btn5,1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1, 2)
        vbox.addWidget(self.btn, 3)
        vbox.addWidget(self.pbar,1)
        vbox.addLayout(hbox5,1)
        vbox.addWidget(self.tw, 3)
        vbox.addLayout(hbox4)
        vbox.addWidget(self.tb2, 1)

        self.setLayout(vbox)
        self.setGeometry(700, 300, 732, 700)
        self.show()

    def search(self):
        self.cb.clear()
        text = self.le.text()
        text = text.replace(" ", "")
        if text in self.guild.member_names() and text != "":
            self.cb.addItem(text)
        elif text!="":
            for i in self.guild.member_names():
                if text in i:
                    self.cb.addItem(i)
                elif i in text:
                    self.cb.addItem(i)
                else:
                    rate = 0
                    max_num = min([len(i), len(text)])
                    for j in range(max_num):
                        if text[j] == i[j]:
                            rate += 1
                        if (rate / max_num) * 100 > 50:
                            self.cb.addItem(i)
    def image(self):
        self.worker = worker(self.guild)
        self.worker.perpose = "img"
        self.worker.name = self.cb.currentText()
        self.worker.finished.connect(self.lb_set)
        self.worker.start()

    @pyqtSlot(list)
    def lb_set(self, data):
        self.lb.setPixmap(data[0])

    def copy(self):
        text =""
        for i in self.guild.member_names():
            text+=i+'\n'
        clipboard.copy(text)

    def reset_tw(self):
        useful = ["직위", "레벨", "직업", "무릉", "활동일", "기여도"]
        self.tw.clear()
        self.tw.setColumnCount(6)
        self.tw.setHorizontalHeaderLabels(useful)
        if self.guild.member:
            self.tw.setRowCount(len(self.guild))
            self.tw.setVerticalHeaderLabels(self.guild.member_names())
            for i in range(len(self.guild)):
                if self.guild[i].position_id is not None and type(self.guild[i].position_id)==int:
                    self.tw.setItem(i,0,QTableWidgetItem(self.guild.position_name[self.guild[i].position_id]))
                else:
                    self.tw.setItem(i, 0, QTableWidgetItem("None"))
                for j in range(1,6):
                    self.tw.setItem(i, j, QTableWidgetItem(str(self.guild[i].get_list()[j+1])))

    def divide_str(self):
        if self.le2.text() != "" and "\\" not in self.le2.text():
            split_text = self.le2.text()
        elif "\\" in self.le2.text():
            split_text = self.le2.text().replace("\\n", "\n").replace("\\t", "\t").replace("\\\\", '\\')
        else:
            split_text = "\t"
        self.tw.divide_str=split_text

    def combo(self):
        self.tb.clear()
        useful = ["닉네임","직위", "레벨", "직업", "무릉", "활동일", "기여도"]
        text = self.cb.currentText()
        if text in self.guild.member_names():
            self.image()
            member=self.guild[text]
            self.tb.append("%s : %s" % (useful[0], member.get_list()[0]))
            self.tb.append("%s : %s" % (useful[1], self.guild.position_name[member.position_id]))
            for i in range(2,7):
                self.tb.append("%s : %s"%(useful[i],member.get_list()[i]))
        else:
            self.lb.clear()

    def tw_clear(self):
        self.tw.clear()
        self.tw.setRowCount(0)
        self.tw.setColumnCount(0)

    def update(self):
        if not self.guild.server:
            self.tb2.append("서버 이름을 적어주세요.")
            return
        if not self.guild.name:
            self.tb2.append("길드 이름을 적어주세요.")
            return


        self.updating=True
        self.pbar.setValue(0)
        self.worker = worker(self.guild)
        self.worker.perpose = "update"
        self.worker.finished.connect(self.updated)
        self.worker.progress.connect(self.progress)
        self.worker.start()

    @pyqtSlot(list)
    def updated(self):
        self.guild.save_as_file()
        self.reset_tw()

        self.updating=False

    def progress(self):
        self.reset_tw()
        self.pbar.setValue(self.pbar.value()+25)

    def guild_info(self):
        self.worker = worker(self.guild)
        self.worker.perpose="guild_info"
        self.worker.finished.connect(self.set_guild_info)
        self.worker.start()

    @pyqtSlot(list)
    def set_guild_info(self,data):
        self.lb3[0].setText("%s등 플래그 : %s"%(str(data[3]),str(data[0])))
        self.lb3[1].setText("%s등 명성치 : %s" % (str(data[4]),str(data[1])))
        self.lb3[2].setText("%s등 지하수로 : %s"%(str(data[5]),str(data[2])))

    def search_widget_set_po(self):
        self.search_wg.reset_position()

    def sort_guild(self,button):
        up=False
        if self.btn5.text()=="↑":
            up=True
        self.guild.sort_guild(button.text().strip(self.btn5.text()),up)
        self.reset_tw()

    def up_down(self):
        useful = ["닉네임", "직위", "레벨", "직업", "무릉", "활동일", "기여도"]
        if self.btn5.text()=="↑":
            self.btn5.setText('↓')
        elif self.btn5.text()=='↓':
            self.btn5.setText('↑')
        [self.btn4[i].setText(useful[i] + self.btn5.text()) for i in range(7)]


    def set_font(self,font):
        self.le.setFont(font)
        self.le2.setFont(font)
        self.lb.setFont(font)
        self.lb2.setFont(font)
        [self.lb3[i].setFont(font) for i in range(3)]
        self.cb.setFont(font)
        self.tb.setFont(font)
        self.tb2.setFont(font)
        self.tb3.setFont(font)
        self.tb4.setFont(font)
        self.btn.setFont(font)
        self.btn2.setFont(font)
        self.btn3.setFont(font)
        [self.btn4[i].setFont(font) for i in range(7)]
        self.copy_btn.setFont(font)
        self.tw.setFont(font)
        [self.chb[i].setFont(font) for i in range(7)]
        self.pbar.setFont(font)

        self.search_wg.set_font(font)
        self.setting_wg.set_font(font)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.exit(app.exec_())
