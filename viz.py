#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class VizWindow(QWidget):

    def __init__(self, img_name):
        super().__init__()
        self._initUI(img_name)

    def _initUI(self, img_name):
        self.setGeometry(750, 200, 200, 200)
        self.setStyleSheet("background-color: white")

        self.label = QLabel(self)
        self.pixmap = QPixmap(img_name)
        self.label.setPixmap(self.pixmap)

        self.resize(self.pixmap.width(), self.pixmap.height())


    def playGif(self, gif_name):
        self.movie = QMovie(gif_name, QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(15)
        self.label.setMovie(self.movie)
        self.movie.start()

    def stopGif(self):
        self.label.clear()
        self.label.setPixmap(self.pixmap)
