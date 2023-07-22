# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'py.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QInputDialog, QLineEdit, QFileDialog
import scrapper
import threading


class Ui_MainWindow(object):
    def __init__(self):
        self.fileName = ''

    #def saveCreds(self):
    #    userName = self.lineEdit.text()
    #    password = self.lineEdit_2.text()
    #    return [userName, password]


    def clicked(self):
        temp_var = self.dateEdit.date()
        date = temp_var.toPyDate()
        date = str(date).split('-')
        year = date[0]
        year = year[2:]
        month = date[1]
        finalDate = year+month
        finalDate = int(finalDate)
        #creds = self.saveCreds()
        th = threading.Thread(target=scrapper.loading_df , args = (finalDate, self.fileName))
        th.start()

    def resumeProcess(self):
        temp_var = self.dateEdit.date()
        date = temp_var.toPyDate()
        date = str(date).split('-')
        year = date[0]
        year = year[2:]
        month = date[1]
        finalDate = year+month
        finalDate = int(finalDate)
        #creds = self.saveCreds()
        th = threading.Thread(target=scrapper.resume_df , args = (finalDate, self.fileName))
        th.start()

    def browse_file(self):
        self.fileName = QFileDialog.getOpenFileName()
        self.fileName = self.fileName[0]
        # return fileName

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(701, 191)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(436, 50, 201, 22))
        font = QtGui.QFont()
        font.setFamily("Modern")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.dateEdit.setFont(font)
        self.dateEdit.setObjectName("dateEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(460, 80, 161, 31))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.clicked)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(436, 20, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(240, 30, 171, 31))
        self.lineEdit.setObjectName("lineEdit")
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(240, 70, 171, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(14)
        self.lineEdit_2.setFont(font)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(120, 30, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(120, 70, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 110, 161, 31))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.pushButton_2.clicked.connect(self.browse_file)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(50, 110, 161, 31))
        font = QtGui.QFont()
        font.setFamily("MV Boli")
        font.setPointSize(14)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.pushButton_3.clicked.connect(self.resumeProcess)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 701, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_File = QtWidgets.QAction(MainWindow)
        self.actionOpen_File.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.actionOpen_File.setObjectName("actionOpen_File")
        self.actionOpen_File.triggered.connect(self.browse_file)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionOpen_File_2 = QtWidgets.QAction(MainWindow)
        self.actionOpen_File_2.setObjectName("actionOpen_File_2")
        self.actionOpen_File.triggered.connect(self.browse_file)
        self.menuFile.addAction(self.actionOpen_File_2)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Start Processing"))
        self.label.setText(_translate("MainWindow", "MM/DD/YYYY"))
        self.label_2.setText(_translate("MainWindow", "Username"))
        self.label_3.setText(_translate("MainWindow", "Password"))
        self.pushButton_2.setText(_translate("MainWindow", "Open File"))
        self.pushButton_3.setText(_translate("MainWindow", "Resume Processing"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen_File.setText(_translate("MainWindow", "Open File"))
        self.actionOpen_File.setStatusTip(_translate("MainWindow", "Open a .csv file"))
        self.actionOpen_File.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setStatusTip(_translate("MainWindow", "Close the program"))
        self.actionOpen_File_2.setText(_translate("MainWindow", "Open File"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
