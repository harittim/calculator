import sqlite3
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QComboBox, QApplication, QLabel, QLCDNumber
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys


con = sqlite3.connect('db.sqlite')
cur = con.cursor()

correct_num = 'ABCDEF1234567890'
typesys = ["2.Двоичная", "3.Троичная", "4.Четверичная", "5.Пятиричная", "6.Шестиричная", "7.Семеричная",
           "8.Восьмиричн", "9.Девятиричная", "10.Десятиричная", "11.Одинадцатиричная",
           "12.Двенадцатиричная", "13.Тренадцатиричная","14.Четырнадцатиричная", "15.Пятнадцатиричная",
           "16.Шестнадцатиричная", '17.Другое']

class Example(QWidget):
    def __init__(self):
        self.first_base = 2
        self.second_base = 2
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setGeometry(300, 300, 380, 130)
        self.setWindowTitle('Калькулятор СС')

        self.b = QPushButton('->', self)
        self.b.resize(self.b.sizeHint())
        self.b.move(165, 41)
        self.b.resize(50, 20)
        self.b.clicked.connect(self.shift)

        self.word1 = QLineEdit(self)
        self.word1.move(5, 42)
        self.word1.resize(155, 20)

        self.word2 = QLineEdit(self)
        self.word2.move(220, 42)
        self.word2.resize(155, 20)
        self.word2.setEnabled(False)

        self.name_label = QLabel(self)
        self.name_label.setText("Первая СС:")
        self.name_label.move(40, 65)

        self.name_label = QLabel(self)
        self.name_label.setText("Вторая СС:")
        self.name_label.move(270, 65)

        self.name_label = QLabel(self)
        self.name_label.setText("Самый крутой калькулятор СС!:")
        self.name_label.move(120, 5)

        self.combo1 = QComboBox(self)
        self.combo1.addItems(typesys)
        self.combo1.move(5, 80)
        self.combo1.activated[str].connect(self.first_onActivated)

        self.combo2 = QComboBox(self)
        self.combo2.addItems(typesys)
        self.combo2.move(220, 80)
        self.combo2.activated[str].connect(self.second_onActivated)

        self.pixmap = QPixmap('calculate.jpg')
        self.image = QLabel(self)
        self.image.move(300, 2)
        self.image.setPixmap(self.pixmap)

        self.pixmap = QPixmap('calculate.jpg')
        self.image = QLabel(self)
        self.image.move(80, 2)
        self.image.setPixmap(self.pixmap)

        self.word3 = QLineEdit(self)
        self.word3.move(5, 105)
        self.word3.resize(50, 20)
        self.word3.setEnabled(False)

        self.word4 = QLineEdit(self)
        self.word4.move(220, 105)
        self.word4.resize(50, 20)
        self.word4.setEnabled(False)




    def shift(self):
        if self.first_base == 'waiting':
            result = str(self.start_extra(self.word1.text()))
        else:
            result = str(self.start(self.word1.text()))
        if result.isdigit():
            if self.second_base == 'waiting':
                self.word2.setText(str(self.end_extra(result)))
            else:
                self.word2.setText(str(self.end(result)))
                a = str(self.word1.text()).upper()
                ret = ''
                for i in range(len(a)):
                    if a[i] == 'O':
                        ret += '0'
                    else:
                        ret += a[i]
                self.word1.setText(ret)
        else:
            self.word2.setText(result)


    def first_onActivated(self, text):
        if int(text.split('.')[0]) == 17:
            self.first_base = 'waiting'
            self.word3.setEnabled(True)
        else:
            self.first_base = int(text.split('.')[0])
            self.word3.setEnabled(False)


    def second_onActivated(self, text):
        if int(text.split('.')[0]) == 17:
            self.second_base = 'waiting'
            self.word4.setEnabled(True)
        else:
            self.second_base = int(text.split('.')[0])
            self.word4.setEnabled(False)



    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Backspace:
            self.word1.setText('')
            self.word2.setText('')


    def end(self, num):
        # Из десятичной в нужную
        base = self.second_base
        num = int(num)
        newNum = ''
        if num:
            while num > 0:
                result = cur.execute("SELECT * FROM Analog_in_16 WHERE input = '{}'".format(str(num % base))).fetchall()
                newNum = str(result[0][1]) + newNum
                num //= base
            return newNum
        else:
            return 0


    def start(self, num):
        # Из данной в десятичную
        base = self.first_base
        base = int(base)
        num = str(num).upper()
        newNum = 0
        k = len(num) - 1
        for i in num:
            if not(1040 <= ord(i) <= 1072):
                result = cur.execute("SELECT * FROM Analog_in_16 WHERE output = '{}'".format(i)).fetchall()
                try:
                    if int(result[0][0]) < base:
                        newNum += int(result[0][0]) * base ** k
                        k -= 1
                    else:
                        return 'Есть недопустимые символы!'
                except:
                    return 'Есть недопустимые символы!'
            else:
                return 'Смените раскладку'
        return str(newNum)

    def start_extra(self, num):
        if self.word3.text().isdigit():
            base = int(self.word3.text())
        else:
            return 'Неверная СС'
        a = num
        if '(' in a and ')' in a:
            a = a.replace("(", "")
            a = a.replace(")", "")
        else:
            return 'Неверные скобки'
        if a.isdigit():
            r = 0
            l = 0
            for i in num:
                if i == '(':
                    r += 1
                elif i == ')':
                    l += 1
                if r < l or r - l > 1:
                    return 'Неверные скобки'
            num = num[1:]
            num = num[:-1]
            try:
                num = num.split(')(')
            except:
                num = [num]
            for i in range(len(num)):
                num[i] = int(num[i])
            if max(num) >= base:
                return 'Неверная степень'
            newNum = 0
            k = len(num) - 1
            for i in num:
                newNum += int(i) * base ** k
                k -= 1
            return newNum

        else:
            return 'Неверные символы'

    def end_extra(self, num):
        print(1)
        if self.word4.text().isdigit() and int(self.word4.text()) >= 2:
            base = int(self.word4.text())
        else:
            return 'Неверная СС'
        num = int(num)
        newNum = ''
        if num:
            while num > 0:
                newNum = ')(' + str(num % base) + newNum
                num //= base
            newNum = newNum[1:]
            newNum += ')'
            return newNum
        else:
            return 0

if __name__ == '__main__':
    focus = QApplication(sys.argv)
    s = Example()
    s.show()
    sys.exit(focus.exec())

