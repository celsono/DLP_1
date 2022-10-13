#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/09 23:15
# @Author  : tzh
# @File    : main.py
# @Software: PyCharm
from PyQt5.QtWidgets import *
import sys
from gui import Window


""" JUST RUN IT """
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
