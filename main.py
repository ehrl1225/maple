from PyQt5.QtWidgets import QApplication
from MyMain import MyMain
import sys
import os
import multiprocessing


if __name__=="__main__":
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    if not os.path.isdir("data"):
        os.mkdir("data")
    ex = MyMain()
    sys.exit(app.exec_())
