from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import mysql.connector as MySQLdb
import sys


from PyQt5.uic import loadUiType

ui, _ = loadUiType('lab.ui')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handel_ui_changes()
        self.handel_buttons()

        self.show_categoty()
        self.show_author()
        self.show_publisher()
        self.show_category_cb()
        self.show_author_cb()
        self.show_publisher_cb()

    def handel_ui_changes(self):
        self.hide_theme()
        self.tabWidget.tabBar().setVisible(False)

    def handel_buttons(self):
        self.pushButton_5.clicked.connect(self.show_theme)
        self.pushButton_13.clicked.connect(self.hide_theme)

        self.pushButton.clicked.connect(self.open_day_today_tab)
        self.pushButton_2.clicked.connect(self.open_book_tab)
        self.pushButton_3.clicked.connect(self.open_user_tab)
        self.pushButton_4.clicked.connect(self.open_setting_tab)

        self.pushButton_9.clicked.connect(self.add_new_books)
        self.pushButton_11.clicked.connect(self.search_books)
        self.pushButton_7.clicked.connect(self.edit_books)
        self.pushButton_10.clicked.connect(self.delete_books)

        self.pushButton_17.clicked.connect(self.add_category)
        self.pushButton_18.clicked.connect(self.add_author)
        self.pushButton_19.clicked.connect(self.add_publisher)

        self.pushButton_12.clicked.connect(self.add_new_users)
        self.pushButton_16.clicked.connect(self.login)

        self.pushButton_20.clicked.connect(self.dark_q)
        self.pushButton_22.clicked.connect(self.dark_grey)
        self.pushButton_23.clicked.connect(self.dark_blue)
        self.pushButton_21.clicked.connect(self.dark_orange)

    def show_theme(self):
        self.groupBox_4.show()

    def hide_theme(self):
        self.groupBox_4.hide()

    # ===============opening tabs=============
    def open_day_today_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def open_book_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def open_user_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_setting_tab(self):
        self.tabWidget.setCurrentIndex(3)

    # ================Books======================
    def add_new_books(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='lab')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_7.text()
        book_desc = self.textEdit.toPlainText()
        book_code = self.lineEdit_8.text()
        book_category = self.comboBox_8.currentText()
        book_author = self.comboBox_6.currentText()
        book_publisher = self.comboBox_7.currentText()
        book_price = self.lineEdit_9.text()

        self.cur.execute('''INSERT INTO book(book_name, book_desc, book_code, 
        book_category, book_auther, book_publisher, book_price)
        VALUES(%s, %s, %s, %s, %s ,%s, %s)
        ''', (book_title, book_desc, book_code, book_category, book_author, book_publisher, book_price))
        self.db.commit()
        self.statusBar().showMessage("New Book Added..")

        self.lineEdit_7.setText('')
        self.textEdit.setPlainText('')
        self.lineEdit_8.setText('')
        self.comboBox_8.setCurrentText(book_category)
        self.comboBox_6.setCurrentText(book_author)
        self.comboBox_7.setCurrentText(book_publisher)
        self.lineEdit_9.setText('')

    def search_books(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='lab')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_2.text()
        sql = '''SELECT * FROM book WHERE book_name = %s'''
        self.cur.execute(sql, [book_title])
        data = self.cur.fetchone()
        print(data)

        self.lineEdit_3.setText(data[3])
        self.textEdit_2.setPlainText(data[2])
        self.lineEdit_6.setText(str(data[7]))
        self.comboBox_3.setCurrentText(data[4])
        self.comboBox_4.setCurrentText(data[5])
        self.comboBox_5.setCurrentText(data[6])

    def edit_books(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='lab')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_2.text()
        book_desc = self.textEdit_2.toPlainText()
        book_code = self.lineEdit_3.text()
        book_category = self.comboBox_3.currentText()
        book_author = self.comboBox_4.currentText()
        book_publisher = self.comboBox_5.currentText()
        book_price = self.lineEdit_6.text()

        search_book_title = self.lineEdit_2.text()
        print(book_title+book_price+book_publisher+book_category+book_author+book_author+book_desc)

        self.cur.execute('''
        UPDATE book SET book_name=%s ,book_desc=%s ,book_code=%s ,book_category=%s ,book_auther=%s 
        ,book_publisher=%s ,book_price=%s WHERE book_name = %s''',
        (book_title, book_desc, book_code, book_category, book_author, book_publisher, book_price, search_book_title))
        self.db.commit()
        self.statusBar().showMessage("Book Edited...")

    def delete_books(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='lab')
        self.cur = self.db.cursor()

        delete_book_title = self.lineEdit_2.text()
        warning = QMessageBox.warning(self, 'Delete Book ', "Are you sure to delete..?", QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            sql = ''' DELETE FROM book WHERE book_name = %s '''
            self.cur.execute(sql, [(delete_book_title)])
            self.db.commit()
            self.statusBar().showMessage("Book Deleted ==> "+delete_book_title)

    # ================Users========================
    def add_new_users(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='lab')
        self.cur = self.db.cursor()

        username = self.lineEdit_10.text()
        email = self.lineEdit_11.text()
        password = self.lineEdit_12.text()
        password2 = self.lineEdit_13.text()

        if password == password2:
            self.cur.execute('''INSERT INTO users (user_name, user_email, user_password)
            VALUES(%s, %s, %s)''', (username, email, password))
            self.db.commit()
            self.statusBar().showMessage("New User Added ==> "+username)

        else:
            self.label_4.setText("Please enter correct password match twice")

    def login(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='lab')
        self.cur = self.db.cursor()

        username = self.lineEdit_22.text()
        password = self.lineEdit_28.text()

        sql = '''SELECT user_name, user_password FROM users '''
        # for info in self.cur.execute(sql):
        #     print(info)
        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if username == row[0] and password == row[1]:
                print("password match")
                self.statusBar().showMessage("Valid User..!")

    def edit_user(self):
        pass

    # =============== settings=====================
    def add_category(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='lab')
        self.cur = self.db.cursor()
        category_name = self.lineEdit_29.text()

        self.cur.execute('''INSERT INTO category (category_name) VALUES (%s) ''', (category_name, ))
        self.db.commit()
        self.statusBar().showMessage("Category Added ==>"+category_name)
        print('Category Added ==> '+category_name)
        self.lineEdit_29.setText('')
        self.show_categoty()
        self.show_category_cb()

    def show_categoty(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='lab')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT category_name FROM category''')
        data = self.cur.fetchall()
        print(data)
        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)

    def add_author(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='lab')
        self.cur = self.db.cursor()
        author_name = self.lineEdit_30.text()

        self.cur.execute('''INSERT INTO Author (Author_name) VALUES (%s) ''', (author_name, ))
        self.db.commit()
        self.statusBar().showMessage("Author Added ==>"+author_name)
        self.lineEdit_30.setText('')
        print('Author Added ==> '+author_name)
        self.show_author()
        self.show_author_cb()

    def show_author(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='lab')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT Author_name FROM Author''')
        data = self.cur.fetchall()
        print(data)
        if data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)

    def add_publisher(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='lab')
        self.cur = self.db.cursor()
        publisher_name = self.lineEdit_31.text()

        self.cur.execute('''INSERT INTO Publisher (Publisher_name) VALUES (%s) ''', (publisher_name, ))
        self.db.commit()
        self.statusBar().showMessage("Publisher Added ==>"+publisher_name)
        self.lineEdit_31.setText('')
        print('Publisher Added ==> '+publisher_name)
        self.show_publisher()
        self.show_publisher_cb()

    def show_publisher(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='lab')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT Publisher_name FROM Publisher''')
        data = self.cur.fetchall()
        print(data)
        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)

    # showing settings in UI
    def show_category_cb(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='lab')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT category_name FROM category''')
        data = self.cur.fetchall()
        print(data)
        self.comboBox_8.clear()
        for category in data:
            print(category[0])
            self.comboBox_8.addItem(category[0])
            self.comboBox_3.addItem(category[0])

    def show_author_cb(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='lab')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT Author_name FROM Author''')
        data = self.cur.fetchall()
        print(data)
        self.comboBox_6.clear()
        for author in data:
            print(author[0])
            self.comboBox_6.addItem(author[0])
            self.comboBox_4.addItem(author[0])

    def show_publisher_cb(self):

        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='lab')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT Publisher_name FROM Publisher''')
        data = self.cur.fetchall()
        print(data)
        self.comboBox_7.clear()
        for publisher in data:
            print(publisher[0])
            self.comboBox_7.addItem(publisher[0])
            self.comboBox_5.addItem(publisher[0])

    # =========== UI theme =====================
    def dark_blue(self):
        style = open('themes/dark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_grey(self):
        style = open('themes/darkgrey.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_orange(self):
        style = open('themes/darkorange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def dark_q(self):
        style = open('themes/dark1.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
