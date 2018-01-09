#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import networkx as nx
import sys
import matplotlib.pyplot as plt 
from machine import Machine
from viz import VizWindow
import imageio


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self._initUI()
        self.errorMsg = QErrorMessage()
        self.errorMsg.setFixedSize(500,220)
        self.messageBox = QMessageBox()
        self.messageBox.setFixedSize(500,220)
        self.prevStates = []
        self.prevSymbs = []
        self.endStates = []
        self.startState = []
        self.machine = Machine()


    def _initUI(self):
        self.setGeometry(50, 400, 600, 400)

        grid = QGridLayout()
        grid.setSpacing(10)

        self.alphabetLine = QLineEdit()
        self.alphabetLine.setPlaceholderText("Alphabet")
        self.alphabetLine.textChanged.connect(self._refreshAlphabet)

        self.statesLine = QLineEdit()
        self.statesLine.setPlaceholderText("States")
        self.statesLine.textChanged.connect(self._refreshStates)

        self.endsLine = QLineEdit()
        self.endsLine.setPlaceholderText("Ends")
        self.endsLine.textChanged.connect(self._refreshEnds)

        self.stateTable = QTableWidget()
        self.stateTable.resizeColumnsToContents()
        self.stateTable.itemChanged.connect(self._createMachine)
        self.stateTable.itemChanged.connect(self._refreshWord)

        self.enteredWord = QLineEdit()
        self.enteredWord.setPlaceholderText("Enter a word")
        self.enteredWord.textChanged.connect(self._refreshWord)

        grid.addWidget(self.alphabetLine, 0, 0, 1, 5)

        grid.addWidget(self.statesLine, 1, 0, 1, 3)

        grid.addWidget(self.endsLine, 1, 3, 1, 2)

        grid.addWidget(self.enteredWord, 3, 0, 1, 5)

        grid.addWidget(self.stateTable, 4, 0, 1, 5)

        self.setLayout(grid)
        self.show()


    def _refreshAlphabet(self):
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

        self._createMachine()


    def _refreshStates(self):
        states = self.statesLine.text().split(" ")
        states = list(filter(None, states))

        if states:
            self.startState = states[0]
        else:
            self.startState = None

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

        self._createMachine()
        self._refreshWord()
        
    
    def _refreshEnds(self):
        self.endStates = []
        ends = self.endsLine.text().split(" ")
        ends = list(filter(None, ends))

        for end in ends:
            if end in self.prevStates:
                self.endStates.append(end)

        self._createMachine()
        self._refreshWord()


    def _createMachine(self):
        dict = {}
        for i in range(self.stateTable.columnCount()):
            hheader = self.stateTable.horizontalHeaderItem(i).text()
            transitions = {}

            for j in range(self.stateTable.rowCount()):
                vheader = self.stateTable.verticalHeaderItem(j).text()
                item = self.stateTable.item(j, i)

                if item and item.text() in self.prevStates:                 #Если в ячейке что-то есть, и это одно из состояний
                    transitions[vheader] = self.stateTable.item(j, i).text()

            dict[hheader] = transitions

        self.machine = Machine(dict, self.startState, self.endStates)
        self.machine.draw('graph.png')
        self._show()


    def _refreshWord(self):
        if not self.machine:
            return

        if self.enteredWord.text():
            if self.machine.checkWord(self.enteredWord.text()):
                self.enteredWord.setStyleSheet("background-color: #4E9C72")
            else:
                self.enteredWord.setStyleSheet("background-color: #FF0038")
            self._animate(len(self.enteredWord.text()))
        else:
            self.enteredWord.setStyleSheet("background-color: #FF0038")
            self.viz.stopGif()

    
    def _show(self):
        self.viz = VizWindow('graph.png')
        self.viz.show()
        self.activateWindow()


    def _animate(self, count):
        filenames = []
        for i in range(count):
            filenames.append("{}.png".format(i))

        images = []
        for filename in filenames:
            images.append(imageio.imread(filename))
            imageio.mimsave("movie.gif", images)

        self.viz.playGif("movie.gif")



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

    
    def _closing(self):
        print("LUL")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())