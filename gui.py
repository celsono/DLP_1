#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/10/10 20:23
# @Author  : tzh
# @File    : gui.py
# @Software: PyCharm
"""
    this module is designed for GUI, coded with QyPt5. It mainly contains several elementary widgets,including buttons,
    text boxes,a list and a table.It will cooperate with the 'crawler', receive the inputs from the user and transmit to
    the 'crawl' module,finally present the results in the list and table
"""
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import crawler


class Window:
    """ 'object' window is the main widget,others are its subclasses  """
    def __init__(self):
        self.surprise = None
        self.crawl = None
        self.button_seq = None
        self.textEdit_seq = None
        self.table = None
        self.listwidget = None
        self.button_name = ''
        self.textEdit_name = ''  # initialize the attributes
        self.window = QMainWindow()
        self.window.setWindowTitle("Search Articles!")
        self.window.resize(980, 490)
        self.window.central_widget = QWidget(self.window)
        self.window.setCentralWidget(self.window.central_widget)
        self.bgd_init()
        self.input_name()
        self.input_seq()
        self.button_name_init()
        self.button_seq_init()
        self.qt_list()
        self.qt_table()
        self.appeal_init()  # initialize all the widgets
        self.window.show()  # show up the window

    """ Add a background image """
    def bgd_init(self):
        palette = QtGui.QPalette()
        palette.setBrush(self.window.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('./background.jpg')))
        self.window.setPalette(palette)
        self.window.setAutoFillBackground(True)

    """ add an EditText get the scientist 's name entered by the user """
    def input_name(self):
        self.textEdit_name = QPlainTextEdit(self.window)
        self.textEdit_name.setPlaceholderText("请输入您想要查询的科学家姓名")
        self.textEdit_name.move(10, 150)
        self.textEdit_name.resize(250, 30)

    """ add an EditText get the serial number entered by the user """
    def input_seq(self):
        self.textEdit_seq = QPlainTextEdit(self.window)
        self.textEdit_seq.setPlaceholderText("请输入您想要查询的科学家的序号")
        self.textEdit_seq.move(270, 20)
        self.textEdit_seq.resize(250, 30)

    """ add a button associated with the first EditText  """
    def button_name_init(self):
        self.button_name = QPushButton('查询', self.window)
        self.button_name.move(10, 200)
        self.button_name.clicked.connect(self.button_name_handle)

    """ add a button associated with the second EditText """
    def button_seq_init(self):
        self.button_seq = QPushButton('查询', self.window)
        self.button_seq.move(560, 20)
        self.button_seq.clicked.connect(self.button_seq_handle)

    """ the handle method responds to the first button's click event """
    def button_name_handle(self):
        name = self.textEdit_name.toPlainText().strip()
        self.crawl = crawler.Crawler(name)
        self.crawl.get_url()
        self.crawl.stop_the_war()
        self.listwidget.clear()
        self.listwidget.addItem("以下为检索到的科学家：")
        if len(self.crawl.author) == 0:
            tip = "很遗憾没有搜索到相关人物，检查下姓名重新试试？"
            self.listwidget.addItem("无")
            QMessageBox.information(self.window.central_widget, 'Bad News!', tip, QMessageBox.Ok)
        else:
            for i in range(len(self.crawl.author)):
                item = '第' + str(i+1) + '位:' + self.crawl.author[i]
                self.listwidget.addItem(item)

    """ the handle method responds to the second button's click event """
    def button_seq_handle(self):
        try:
            seq = eval(self.textEdit_seq.toPlainText().strip())
            self.crawl.get_article(seq-1)
            self.table.model.clear()
            self.table.model.setHorizontalHeaderLabels(['PublishedDate', 'ArticleTitle'])
            row = 0
            for key, value in self.crawl.year_article.items():
                for article in value:
                    item_year = QStandardItem(key)
                    self.table.model.setItem(row, 0, item_year)
                    item_article = QStandardItem(article)
                    self.table.model.setItem(row, 1, item_article)
                    self.table.model.item(row, 1).setForeground(QBrush(QColor(255, 0, 0)))
                    self.table.model.item(row, 1).setFont(QFont("Times", 10, QFont.Black))
                    row += 1
            self.crawl.year_article = {}
        except IndexError:
            tip = '一共只有' + str(len(self.crawl.author)) + '位科学家噢，不要超出范围哩'
            QMessageBox.warning(self.window.central_widget, 'WARNING', tip, QMessageBox.Ok)
        except NameError:
            tip = "输入数字就可以了噢，可不要火星文哩"
            QMessageBox.warning(self.window.central_widget, 'WARNING', tip, QMessageBox.Ok)
        except SyntaxError:
            tip = "请先输入科学家姓名再来查找对应的文章欧"
            QMessageBox.warning(self.window.central_widget, 'WARNING', tip, QMessageBox.Ok)
        except Exception:
            tip = "未知小bug？等待后续测试QAQ"
            QMessageBox.warning(self.window.central_widget, 'WARNING', tip, QMessageBox.Ok)

    """ create a list displays the scientists' name searched """
    def qt_list(self):
        self.listwidget = QListWidget(self.window)
        self.listwidget.move(10, 250)
        self.listwidget.resize(250, 190)

    """ create a table display the specified scientist's article titles and their dates of publication """
    def qt_table(self):
        self.table = QTableWidget(self.window.central_widget)
        self.table.move(270, 50)
        self.table.resize(700, 400)
        self.table.model = QStandardItemModel(0, 2)
        self.table.model.setHorizontalHeaderLabels(['PublishedDate', 'ArticleTitle'])
        self.table.tableView = QTableView()
        self.table.tableView.setModel(self.table.model)
        self.table.tableView.horizontalHeader().setStretchLastSection(True)
        # self.table.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.tableView.setColumnWidth(0, 150)
        self.table.tableView.setColumnWidth(1, 470)
        dlgLayout = QVBoxLayout()
        dlgLayout.addWidget(self.table.tableView)
        self.table.setLayout(dlgLayout)

    """ the following two methods just present the peaceful appeal """
    def appeal_init(self):
        self.surprise = QPushButton("It's a surprise!", self.window)
        self.surprise.resize(200, 25)
        self.surprise.move(10, 20)
        self.surprise.clicked.connect(self.surprise_handle)

    def surprise_handle(self):
        try:
            QMessageBox.information(self.window.central_widget, 'PEACE!', self.crawl.appeal, QMessageBox.Yes)
        except Exception:
            tip = "亲亲，这边建议您搜索完再点击噢◐/v/◐"
            QMessageBox.warning(self.window.central_widget, 'WARNING', tip, QMessageBox.Ok)


