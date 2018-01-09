#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import networkx as nx
import sys
import matplotlib.pyplot as plt 


class MachineWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.errorMsg = QErrorMessage()
        self.errorMsg.setFixedSize(500,220)
        self.messageBox = QMessageBox()
        self.messageBox.setFixedSize(500,220)
        self.prevStates = []
        self.prevSymbs = []


    def initUI(self):
        self.setGeometry(50, 400, 600, 400)

        grid = QGridLayout()
        grid.setSpacing(10)

        self.alphabetLine = QLineEdit()
        self.alphabetLine.setPlaceholderText("Alphabet")
        self.alphabetLine.textChanged.connect(self.refreshAlphabet)

        self.statesLine = QLineEdit()
        self.statesLine.setPlaceholderText("States")
        self.statesLine.textChanged.connect(self.refreshStates)

        self.endsLine = QLineEdit()
        self.endsLine.setPlaceholderText("Ends")

        self.stateTable = QTableWidget()
        self.stateTable.resizeColumnsToContents()
        tableConfirm = QPushButton("Confirm", self)

        self.enteredWord = QLineEdit()
        self.enteredWord.setPlaceholderText("Enter a word")
        self.enteredWord.setStyleSheet("background-color: #B22222")

        grid.addWidget(self.alphabetLine, 0, 0, 1, 5)

        grid.addWidget(self.statesLine, 1, 0, 1, 3)

        grid.addWidget(self.endsLine, 1, 3, 1, 2)

        grid.addWidget(self.enteredWord, 3, 0, 1, 5)

        grid.addWidget(self.stateTable, 4, 0, 1, 5)

        grid.addWidget(tableConfirm, 5, 0)

        self.setLayout(grid)
        self.show()


    def refreshAlphabet(self):
        symbs = self.alphabetLine.text().split(" ")
        symbs = list(filter(None, symbs))
        
        if len(symbs) > len(self.prevSymbs):                    #Стало больше - добавили
            indexes = self._addedIndex(self.prevSymbs, symbs)   #Получаем индексы вставленных элементов
            for index in sorted(indexes):
                self.stateTable.insertRow(index)

        elif len(symbs) < len(self.prevSymbs):                  #Стало меньше - удалили
            indexes = self._removedIndex(self.prevSymbs, symbs)     #Получаем индексы удаленных элементов
            for index in sorted(indexes, reverse=True):
                self.stateTable.removeRow(index)

        for i in range(len(symbs)):
            self.stateTable.setVerticalHeaderLabels(symbs)

        self.prevSymbs = symbs


    def refreshStates(self):
        states = self.statesLine.text().split(" ")
        states = list(filter(None, states))

        if len(states) > len(self.prevStates):                  #Стало больше - добавили
            indexes = self._addedIndex(self.prevStates, states) #Получаем индексы вставленных элементов
            for index in sorted(indexes):
                self.stateTable.insertColumn(index)

        elif len(states) < len(self.prevStates):                #Стало меньше - удалили
            indexes = self._removedIndex(self.prevStates, states)    #Получаем индексы удаленных элементов
            for index in sorted(indexes, reverse=True):
                self.stateTable.removeColumn(index)

        for i in range(len(states)):
            self.stateTable.setHorizontalHeaderLabels(states)

        self.prevStates = states


    def _addedIndex(self, prevList, currentList):
        added = list(set(currentList) - set(prevList))
        res = []
        for i in range(len(added)):
            res.append(currentList.index(added[i]))
        return res


    def _removedIndex(self, prevList, currentList):
        removed = list(set(prevList) - set(currentList))
        res = []
        for i in range(len(removed)):
            res.append(prevList.index(removed[i]))
        return res


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MachineWindow()
    sys.exit(app.exec_())