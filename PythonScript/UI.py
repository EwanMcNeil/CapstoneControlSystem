##code for the UI for Capstone
import sys
import os
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')

import threading

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from PyQt5.uic import loadUi

from SwapDockUI import Ui_MainWindow



class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        updateThread = threading.Thread(target =self.updateGUIloop)
        updateThread.start()



    def connectSignalsSlots(self):
       print("ran")
      # self.action_Exit.triggered.connect(self.close)
       #self.action_Find_Replace.triggered.connect(self.findAndReplace)
      # self.action_About.triggered.connect(self.about)

    def findAndReplace(self):
        dialog = FindReplaceDialog(self)
        dialog.exec()

    #def run(self):



    #########################
    ###UPDATING UI
    #########################
    def updateGUIloop(self):
        pastStage = 0
        update = False
        print("startedLoop")
        while(True):
            try:
                f = open("currentStage.txt", "r")
                currentStage =  int(f.read())        ##not converting correctly
                if(pastStage != currentStage):
                    update = True
                    pastStage = currentStage
                if(currentStage == 0 and update):
                    print("0")
                    self.droneSearchText.setStyleSheet("background-color: red")
                    self.centerTaskTextEdit.setStyleSheet("background-color: red")
                    self.RotatingDroneTextEdit.setStyleSheet("background-color: red")
                    update = False
                if(currentStage == 1 and update):
                    print("1")
                    self.droneSearchText.setStyleSheet("background-color: yellow")
                    self.centerTaskTextEdit.setStyleSheet("background-color: red")
                    self.RotatingDroneTextEdit.setStyleSheet("background-color: red")
                    update = False
                if(currentStage == 2 and update):
                    print("2")
                    self.droneSearchText.setStyleSheet("background-color: green")
                    self.centerTaskTextEdit.setStyleSheet("background-color: yellow")
                    self.RotatingDroneTextEdit.setStyleSheet("background-color: red")
                    update = False
                if(currentStage == 3 and update):
                    print("3")
                    self.droneSearchText.setStyleSheet("background-color: green")
                    self.centerTaskTextEdit.setStyleSheet("background-color: green")
                    self.RotatingDroneTextEdit.setStyleSheet("background-color: yellow")
                    update = False
            except:
                os.execv("UI.py", sys.argv)


class FindReplaceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("ui/find_replace.ui", self)
    
    app = QApplication(sys.argv)
    win = Window()
    uiCreation = True
    win.show()
    app.exec()
    win.updateGUIloop()
    sys.exit(app.exec())

