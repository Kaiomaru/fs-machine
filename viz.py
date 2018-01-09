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

        label = QLabel(self)
        pixmap = QPixmap(img_name)
        label.setPixmap(pixmap)
 
        if pixmap.width() > self.width() or pixmap.height() > self.height():
            self.resize(pixmap.width(),pixmap.height())