# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SwapDock.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.droneSearchText = QtWidgets.QTextEdit(self.centralwidget)
        self.droneSearchText.setGeometry(QtCore.QRect(10, 60, 131, 51))
        self.droneSearchText.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"alternate-background-color: rgb(0, 255, 127);\n"
"alternate-background-color: rgb(255, 255, 127);")
        self.droneSearchText.setObjectName("droneSearchText")
        self.progressBar_search = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_search.setEnabled(False)
        self.progressBar_search.setGeometry(QtCore.QRect(160, 90, 118, 23))
        self.progressBar_search.setProperty("value", 24)
        self.progressBar_search.setObjectName("progressBar_search")
        self.centerTaskTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.centerTaskTextEdit.setGeometry(QtCore.QRect(10, 130, 131, 51))
        self.centerTaskTextEdit.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"alternate-background-color: rgb(0, 255, 127);\n"
"alternate-background-color: rgb(255, 255, 127);")
        self.centerTaskTextEdit.setObjectName("centerTaskTextEdit")
        self.AlignmentTaskTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.AlignmentTaskTextEdit.setGeometry(QtCore.QRect(10, 200, 131, 51))
        self.AlignmentTaskTextEdit.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"alternate-background-color: rgb(0, 255, 127);\n"
"alternate-background-color: rgb(255, 255, 127);")
        self.AlignmentTaskTextEdit.setObjectName("AlignmentTaskTextEdit")
        self.progressBar_center = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_center.setEnabled(False)
        self.progressBar_center.setGeometry(QtCore.QRect(160, 150, 118, 23))
        self.progressBar_center.setProperty("value", 24)
        self.progressBar_center.setObjectName("progressBar_center")
        self.progressBar_aligment = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_aligment.setEnabled(False)
        self.progressBar_aligment.setGeometry(QtCore.QRect(160, 230, 118, 23))
        self.progressBar_aligment.setProperty("value", 24)
        self.progressBar_aligment.setObjectName("progressBar_aligment")
        self.ArmTaskTestEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.ArmTaskTestEdit.setGeometry(QtCore.QRect(10, 280, 131, 51))
        self.ArmTaskTestEdit.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"alternate-background-color: rgb(0, 255, 127);\n"
"alternate-background-color: rgb(255, 255, 127);")
        self.ArmTaskTestEdit.setObjectName("ArmTaskTestEdit")
        self.progressBar_arm = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_arm.setEnabled(False)
        self.progressBar_arm.setGeometry(QtCore.QRect(160, 300, 118, 23))
        self.progressBar_arm.setProperty("value", 24)
        self.progressBar_arm.setObjectName("progressBar_arm")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 27))
        self.menubar.setObjectName("menubar")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuArduino = QtWidgets.QMenu(self.menubar)
        self.menuArduino.setObjectName("menuArduino")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionPullFromGit = QtWidgets.QAction(MainWindow)
        self.actionPullFromGit.setObjectName("actionPullFromGit")
        self.action_Upload_all = QtWidgets.QAction(MainWindow)
        self.action_Upload_all.setObjectName("action_Upload_all")
        self.actionRun_Centering = QtWidgets.QAction(MainWindow)
        self.actionRun_Centering.setObjectName("actionRun_Centering")
        self.action_Run_Alignment = QtWidgets.QAction(MainWindow)
        self.action_Run_Alignment.setObjectName("action_Run_Alignment")
        self.action_Run_Arm = QtWidgets.QAction(MainWindow)
        self.action_Run_Arm.setObjectName("action_Run_Arm")
        self.menuArduino.addAction(self.action_Upload_all)
        self.menuArduino.addAction(self.actionRun_Centering)
        self.menuArduino.addAction(self.action_Run_Alignment)
        self.menuArduino.addAction(self.action_Run_Arm)
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuArduino.menuAction())
        self.toolBar.addAction(self.actionPullFromGit)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.droneSearchText.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Searching for Drones</span></p></body></html>"))
        self.centerTaskTextEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Centering Task</span></p></body></html>"))
        self.AlignmentTaskTextEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Alignment Task</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\"><br /></p></body></html>"))
        self.ArmTaskTestEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:600;\">Arm task</span></p></body></html>"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuArduino.setTitle(_translate("MainWindow", "Arduino"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionPullFromGit.setText(_translate("MainWindow", "PullFromGit"))
        self.action_Upload_all.setText(_translate("MainWindow", "&Upload all"))
        self.actionRun_Centering.setText(_translate("MainWindow", "&Run Centering"))
        self.action_Run_Alignment.setText(_translate("MainWindow", "&Run Alignment"))
        self.action_Run_Arm.setText(_translate("MainWindow", "&Run Arm"))

