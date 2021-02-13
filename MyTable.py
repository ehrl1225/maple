import sys
from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTableWidget, QApplication , QTableWidgetItem, QAbstractItemView

data = {'col1':['1','2','3'], 'col2':['4','5','6'], 'col3':['7','8','9']}

class MyTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.divide_str="\t"
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def keyPressEvent(self, ev):
        if (ev.key() == Qt.Key_C) and (ev.modifiers() & Qt.ControlModifier):
            self.copySelection()

    def copySelection(self):
        selection = self.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * (colcount) for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            text=''
            for i in range(len(table)):
                line=self.verticalHeaderItem(i).text()+self.divide_str
                for j in table[i]:
                    if j:
                        line+=j+self.divide_str
                line=line.strip(self.divide_str)
                text += line+'\n'
            QApplication.clipboard().setText(text)


def main(args):
    app = QApplication(args)
    table = MyTable(data, 5, 3)
    table.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main(sys.argv)