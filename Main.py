from PyQt5 import QtCore, QtGui, QtWidgets
import cgitb 
cgitb.enable(format = 'text')

from CustomCiphers import magic_square, gamma, combine_cip # Магический квадрат (Перестановка)
from NumpyHill import hill_cip # Хилла (Замены)

def onClick ( self ):
    index = self.comb_cip.currentIndex ( )
    isEnc = self.encCheck.isChecked ( )
    source = self.t_source.text ( )
    if ( len(source) < 4 ):
        QtWidgets.QMessageBox.critical(None, "Ошибка", "Длина исходной строки меньше 4 символов!")
        return
    res = ''
    if (index == 0):
        res = magic_square ( source, isEnc )
    elif (index == 1):
        res = hill_cip ( source, isEnc )
    elif (index == 2):
        res = gamma ( source, isEnc )
    elif (index == 3):
        res = combine_cip ( source, isEnc )

    self.t_enc.setText ( res )


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(340, 150)
        MainWindow.setWindowTitle("Шифрование")
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.t_source = QtWidgets.QLineEdit(self.centralwidget)
        self.t_source.setGeometry(QtCore.QRect(10, 30, 141, 31))
        font = self.t_source.font()
        font.setPointSize(14)
        self.t_source.setFont(font)

        self.t_enc = QtWidgets.QLineEdit(self.centralwidget)
        self.t_enc.setGeometry(QtCore.QRect(180, 30, 141, 31))
        font = self.t_enc.font()
        font.setPointSize(14)
        self.t_enc.setFont(font)

        font.setPointSize(10)

        self.l_source = QtWidgets.QLabel("До преобразования", self.centralwidget)
        self.l_source.setGeometry(QtCore.QRect(10, 0, 141, 31))
        self.l_source.setAlignment(QtCore.Qt.AlignCenter)
        self.l_source.setFont(font)

        self.l_enc = QtWidgets.QLabel("После преобразования", self.centralwidget)
        self.l_enc.setGeometry(QtCore.QRect(180, 0, 141, 31))
        self.l_enc.setAlignment(QtCore.Qt.AlignCenter)
        self.l_enc.setFont(font)

        self.comb_cip = QtWidgets.QComboBox(self.centralwidget)
        self.comb_cip.setGeometry(QtCore.QRect(10, 100, 141, 31))
        self.comb_cip.addItem("Перестановка")
        self.comb_cip.addItem("Замена (RU)")
        self.comb_cip.addItem("Гаммирование")
        self.comb_cip.addItem("Комбинированный (RU)")
        self.comb_cip.addItem("С открытым ключом")
        self.comb_cip.addItem("Хеш-функция (MD5)")
        self.comb_cip.setFont(font)

        self.l_cip = QtWidgets.QLabel("Шифрование", self.centralwidget)
        self.l_cip.setGeometry(QtCore.QRect(10, 70, 141, 31))
        self.l_cip.setAlignment(QtCore.Qt.AlignCenter)
        self.l_cip.setFont(font)

        self.pushButton = QtWidgets.QPushButton("Преобразовать", self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(180, 100, 141, 31))
        self.pushButton.setFont(font)

        self.encCheck = QtWidgets.QCheckBox("Текст зашифрован", self.centralwidget)
        self.encCheck.setGeometry(QtCore.QRect(180, 70, 141, 31))
        self.encCheck.setFont(font)

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect ( lambda: onClick ( self ) )


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
