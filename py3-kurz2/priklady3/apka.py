# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\skoleni\aplikace.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(476, 559)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(70, 110, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(190, 110, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(320, 110, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(20, 170, 441, 361))
        self.listWidget.setObjectName("listWidget")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(30, 30, 411, 51))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Dialog)
        self.pushButton_3.clicked.connect(Dialog.close)
        self.pushButton.clicked.connect(Dialog.vloz)
        self.pushButton_2.clicked.connect(Dialog.smaz)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Pridej"))
        self.pushButton_2.setText(_translate("Dialog", "Smaz"))
        self.pushButton_3.setText(_translate("Dialog", "Konec"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

