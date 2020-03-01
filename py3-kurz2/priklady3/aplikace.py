# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aplikace.ui'
#
# Created: Wed Jun 27 11:39:41 2018
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(476, 559)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(70, 110, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(190, 110, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtGui.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(320, 110, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.listWidget = QtGui.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(20, 170, 441, 361))
        self.listWidget.setObjectName("listWidget")
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(30, 30, 411, 51))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL("clicked()"), Dialog.close)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.vloz)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL("clicked()"), self.smaz)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def vloz(self):
        if len(self.lineEdit.text()): 
          self.listWidget.addItem(self.lineEdit.text())
          self.lineEdit.clear()

    def smaz(self):
        self.listWidget.takeItem(self.listWidget.currentRow())

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Pridej", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Dialog", "Smaz", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("Dialog", "Konec", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

