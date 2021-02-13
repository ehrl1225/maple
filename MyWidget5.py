from PyQt5.QtWidgets import *

class MyWIdget5(QWidget):

    def __init__(self, guild):
        super().__init__()
        self.guild = guild
        self.initUI()

    def initUI(self):
        self.lb=[QLabel() for i in range(2)]

        self.le = [QLineEdit() for i in range(2)]

        self.btn = QPushButton("저장")

        self.lb[0].setText("서버")
        self.lb[1].setText("길드 이름")


        self.setGeometry(450, 300, 250, 100)
