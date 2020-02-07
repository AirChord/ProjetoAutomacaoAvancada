# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainUi.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pbNext = QtWidgets.QPushButton(self.centralwidget)
        self.pbNext.setGeometry(QtCore.QRect(180, 370, 75, 23))
        self.pbNext.setObjectName("pbNext")
        self.pbReset = QtWidgets.QPushButton(self.centralwidget)
        self.pbReset.setGeometry(QtCore.QRect(100, 370, 75, 23))
        self.pbReset.setObjectName("pbReset")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 60, 341, 251))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/newPrefix/lazer.png"))
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pbNext.setText(_translate("MainWindow", "Next"))
        self.pbReset.setText(_translate("MainWindow", "Reset"))

import ResFile_rc
