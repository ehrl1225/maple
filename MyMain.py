from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from MyWidget import MyWidget
from PyQt5.QtCore import *
import os


class MyMain(QMainWindow):

    def __init__(self):
        super().__init__()
        self.wg = MyWidget()
        self.initui()

    def initui(self):

        self.setting = QAction('설정', self)
        self.setting.triggered.connect(self.wg.setting_wg.show)

        self.font = QAction('폰트')
        self.font.triggered.connect(self.setting_font)

        self.deep_search = QAction("검색", self)
        self.deep_search.triggered.connect(self.wg.search_wg.show)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&설정')
        fileMenu.addAction(self.setting)
        fileMenu.addAction(self.font)
        fileMenu.addAction(self.deep_search)

        self.setting_info = None
        if os.path.isfile("data/font.txt"):
            f = open("data/font.txt", "r")
            font_setting = f.readline()
            f.close()
            font1 = QFont()
            font1.fromString(font_setting)
            self.set_font(font1)
        self.setCentralWidget(self.wg)
        self.setGeometry(700, 300, 732, 700)

        self.show()

    def setting_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.set_font(font)
            f = open("data/font.txt", "w")
            f.write(font.toString())
            f.close()

    def set_font(self, font):
        self.setting.setFont(font)
        self.font.setFont(font)
        self.deep_search.setFont(font)
        self.wg.set_font(font)

    def closeEvent(self, *args, **kwargs):
        if self.wg.worker:
            self.wg.worker.quit()
        QCoreApplication.instance().quit()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ex = MyMain()
    sys.exit(app.exec_())
