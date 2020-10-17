import datetime
import sys

import mysql.connector as MySQLdb
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from xlsxwriter import *

ui, _ = loadUiType('lab.ui')
login, _ = loadUiType('login.ui')


class Login(QWidget, login):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.window2 = MainApp()
        self.pushButton.clicked.connect(self.handel_login)
        self.dark_q()

    def dark_q(self):
        style = open('themes/dark1.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def handel_login(self):

        self.mysql()

        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        sql = '''SELECT * FROM users '''
        # for info in self.cur.execute(sql):
        #     print(info)
        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if username == row[1] and password == row[3]:
                print("password match")
                self.close()
                self.window2.show()
            else:
                self.label_2.setText("Invalid Credential")

    # mysqli connect
    def mysql(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='lab')
        self.cur = self.db.cursor()


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
        self.show_all_client()
        self.show_all_books()
        self.show_all_operation()

    def handel_ui_changes(self):
        self.hide_theme()
        self.tabWidget.tabBar().setVisible(False)

    def handel_buttons(self):
        self.pushButton_5.clicked.connect(self.show_theme)
        self.pushButton_13.clicked.connect(self.hide_theme)

        self.pushButton.clicked.connect(self.open_day_today_tab)
        self.pushButton_2.clicked.connect(self.open_book_tab)
        self.pushButton_4.clicked.connect(self.open_user_tab)
        self.pushButton_29.clicked.connect(self.open_setting_tab)
        self.pushButton_3.clicked.connect(self.open_client_tab)
        self.pushButton_5.clicked.connect(self.show_theme)

        self.pushButton_9.clicked.connect(self.add_new_books)
        self.pushButton_11.clicked.connect(self.search_books)
        self.pushButton_7.clicked.connect(self.edit_books)
        self.pushButton_10.clicked.connect(self.delete_books)

        self.pushButton_17.clicked.connect(self.add_category)
        self.pushButton_18.clicked.connect(self.add_author)
        self.pushButton_19.clicked.connect(self.add_publisher)

        self.pushButton_12.clicked.connect(self.add_new_users)
        self.pushButton_16.clicked.connect(self.login)
        self.pushButton_14.clicked.connect(self.edit_user)

        self.pushButton_20.clicked.connect(self.dark_q)
        self.pushButton_22.clicked.connect(self.dark_grey)
        self.pushButton_23.clicked.connect(self.dark_blue)
        self.pushButton_21.clicked.connect(self.dark_orange)

        self.pushButton_34.clicked.connect(self.export_clients)
        self.pushButton_27.clicked.connect(self.export_day_operations)
        self.pushButton_33.clicked.connect(self.export_books)

        self.pushButton_85.clicked.connect(self.add_new_client)
        self.pushButton_32.clicked.connect(self.search_client)
        self.pushButton_30.clicked.connect(self.edit_client)
        self.pushButton_31.clicked.connect(self.delete_client)

        self.pushButton_6.clicked.connect(self.handle_day_operation)

    def show_theme(self):
        self.groupBox_4.show()

    def hide_theme(self):
        self.groupBox_4.hide()

    # ===============opening tabs=============
    def open_day_today_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def open_book_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def open_client_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_user_tab(self):
        self.tabWidget.setCurrentIndex(3)

    def open_setting_tab(self):
        self.tabWidget.setCurrentIndex(4)

    # ================Books======================
    def add_new_books(self):

        self.mysql()

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
        self.show_all_books()

    def search_books(self):

        self.mysql()

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

        self.mysql()

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
                         (book_title, book_desc, book_code, book_category,
                          book_author, book_publisher, book_price, search_book_title))
        self.db.commit()
        self.statusBar().showMessage("Book Edited...")
        self.show_all_books()

    def delete_books(self):

        self.mysql()

        delete_book_title = self.lineEdit_2.text()
        warning = QMessageBox.warning(self, 'Delete Book ', "Are you sure to delete..?",
                                      QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            sql = ''' DELETE FROM book WHERE book_name = %s '''
            self.cur.execute(sql, [delete_book_title])
            self.db.commit()
            self.statusBar().showMessage("Book Deleted ==> "+delete_book_title)
            self.show_all_books()

    def show_all_books(self):

        self.mysql()
        self.cur.execute('''
        SELECT book_code, book_name, book_auther, book_publisher, book_desc, book_category, book_price
        FROM book''')
        data = self.cur.fetchall()
        print(data)
        if data:
            self.tableWidget_5.setRowCount(0)
            self.tableWidget_5.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_5.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_5.rowCount()
                self.tableWidget_5.insertRow(row_position)

        self.db.commit()
        self.db.close()

    # ================Users========================
    def add_new_users(self):

        self.mysql()

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

        self.mysql()

        username = self.lineEdit_22.text()
        password = self.lineEdit_28.text()

        sql = '''SELECT * FROM users '''
        # for info in self.cur.execute(sql):
        #     print(info)
        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if username == row[1] and password == row[3]:
                print("password match")
                self.statusBar().showMessage("Valid User..!")
                self.groupBox_5.setEnabled(True)

                self.lineEdit_18.setText(row[1])
                self.lineEdit_20.setText(row[2])
                self.lineEdit_19.setText(row[3])

    def edit_user(self):

        username = self.lineEdit_18.text()
        email = self.lineEdit_20.text()
        password = self.lineEdit_19.text()
        password2 = self.lineEdit_21.text()

        if password == password2:
            self.mysql()
            self.cur.execute('''UPDATE users SET  user_name = %s, user_email = %s,
            user_password  = %s WHERE user_name = %s''', (username, email, password, username))
            self.db.commit()
            self.statusBar().showMessage('User data Updated sussessfully..')
            print('user added ' + username)
        else:
            print("Enter correct password match")

    # =============== settings=====================
    def add_category(self):

        self.mysql()
        category_name = self.lineEdit_29.text()

        self.cur.execute('''INSERT INTO category (category_name) VALUES (%s) ''', (category_name, ))
        self.db.commit()
        self.statusBar().showMessage("Category Added ==>"+category_name)
        print('Category Added ==> '+category_name)
        self.lineEdit_29.setText('')
        self.show_categoty()
        self.show_category_cb()

    def show_categoty(self):

        self.mysql()

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

        self.mysql()
        author_name = self.lineEdit_30.text()

        self.cur.execute('''INSERT INTO Author (Author_name) VALUES (%s) ''', (author_name, ))
        self.db.commit()
        self.statusBar().showMessage("Author Added ==>"+author_name)
        self.lineEdit_30.setText('')
        print('Author Added ==> '+author_name)
        self.show_author()
        self.show_author_cb()

    def show_author(self):

        self.mysql()

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

        self.mysql()
        publisher_name = self.lineEdit_31.text()

        self.cur.execute('''INSERT INTO Publisher (Publisher_name) VALUES (%s) ''', (publisher_name, ))
        self.db.commit()
        self.statusBar().showMessage("Publisher Added ==>"+publisher_name)
        self.lineEdit_31.setText('')
        print('Publisher Added ==> '+publisher_name)
        self.show_publisher()
        self.show_publisher_cb()

    def show_publisher(self):

        self.mysql()

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

        self.mysql()

        self.cur.execute('''SELECT category_name FROM category''')
        data = self.cur.fetchall()
        print(data)
        self.comboBox_8.clear()
        for category in data:
            print(category[0])
            self.comboBox_8.addItem(category[0])
            self.comboBox_3.addItem(category[0])

    def show_author_cb(self):

        self.mysql()

        self.cur.execute('''SELECT Author_name FROM Author''')
        data = self.cur.fetchall()
        print(data)
        self.comboBox_6.clear()
        for author in data:
            print(author[0])
            self.comboBox_6.addItem(author[0])
            self.comboBox_4.addItem(author[0])

    def show_publisher_cb(self):

        self.mysql()

        self.cur.execute('''SELECT Publisher_name FROM Publisher''')
        data = self.cur.fetchall()
        print(data)
        self.comboBox_7.clear()
        for publisher in data:
            print(publisher[0])
            self.comboBox_7.addItem(publisher[0])
            self.comboBox_5.addItem(publisher[0])

    # =========== Export =====================

    def export_books(self):
        self.mysql()
        self.cur.execute('''SELECT  id, book_name, book_desc, book_code, book_category, book_auther,
         book_price FROM book''')
        data = self.cur.fetchall()
        wb = Workbook('book-{}.xlsx'.format(datetime.date.today()))
        sheet1 = wb.add_worksheet()

        sheet1.write(0, 0, 'id')
        sheet1.write(0, 1, 'book_name')
        sheet1.write(0, 2, 'book_desc')
        sheet1.write(0, 3, 'book_code')
        sheet1.write(0, 4, 'book_category')
        sheet1.write(0, 5, 'book_auther')
        sheet1.write(0, 6, 'book_price')
        row_num = 1
        for row in data:
            col_num = 0
            for item in row:
                sheet1.write(row_num, col_num, str(item))
                col_num += 1
            row_num += 1
        wb.close()
        self.statusBar().showMessage("Successfully imported books to Excel ==>" + str(datetime.date.today()) + ".xlsx")
        print(data)

    def export_clients(self):

        self.mysql()
        self.cur.execute('''SELECT  client_name, client_email, client_id  FROM clients''')
        data = self.cur.fetchall()
        wb = Workbook('client-{}.xlsx'.format(datetime.date.today()))
        sheet1 = wb.add_worksheet()

        sheet1.write(0, 0, 'Client Name')
        sheet1.write(0, 1, 'Client Email')
        sheet1.write(0, 2, 'Client Id')
        row_num = 1
        for row in data:
            col_num = 0
            for item in row:
                sheet1.write(row_num, col_num, str(item))
                col_num += 1
            row_num += 1
        wb.close()
        self.statusBar().showMessage("Successfully imported to Excel ==>"+str(datetime.date.today())+".xlsx")
        print(data)

    def export_day_operations(self):
        self.mysql()
        self.cur.execute('''SELECT  id, client_id, book_id, type, day, date, still FROM day_operations''')
        data = self.cur.fetchall()
        wb = Workbook('day-op-{}.xlsx'.format(datetime.date.today()))
        sheet1 = wb.add_worksheet()

        sheet1.write(0, 0, 'id')
        sheet1.write(0, 1, 'client_id')
        sheet1.write(0, 2, 'book_id')
        sheet1.write(0, 3, 'type')
        sheet1.write(0, 4, 'day')
        sheet1.write(0, 5, 'date')
        sheet1.write(0, 6, 'still')
        row_num = 1
        for row in data:
            col_num = 0
            for item in row:
                sheet1.write(row_num, col_num, str(item))
                col_num += 1
            row_num += 1
        wb.close()
        self.statusBar().showMessage("Successfully imported to Excel ==>"+str(datetime.date.today())+".xlsx")
        print(data)
    # ============== Clients ====================
    def add_new_client(self):

        client_name = self.lineEdit_89.text()
        client_email = self.lineEdit_88.text()
        client_id = self.lineEdit_87.text()
        self.mysql()
        self.cur.execute('''INSERT INTO clients (client_name, client_email, client_id) VALUES (%s, %s, %s)
        ''', (client_name, client_email, client_id))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage("New Client Added ==>"+client_name)
        print("New client added "+client_name)
        self.show_all_client()

    def show_all_client(self):
        self.mysql()
        self.cur.execute('''SELECT client_name, client_email, client_id FROM clients''')
        data = self.cur.fetchall()
        print(data)
        if data:
            self.tableWidget_6.setRowCount(0)
            self.tableWidget_6.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_6.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_6.rowCount()
                self.tableWidget_6.insertRow(row_position)

    def search_client(self):

        client_id = self.lineEdit_4.text()
        self.mysql()
        sql = '''SELECT * FROM clients WHERE client_id = %s '''
        self.cur.execute(sql, [client_id])
        data = self.cur.fetchone()
        print(data)
        self.lineEdit_93.setText(data[1])
        self.lineEdit_94.setText(data[2])
        self.lineEdit_95.setText(data[3])

    def edit_client(self):
        client_original_id = self.lineEdit_4.text()
        client_name = self.lineEdit_93.text()
        client_email = self.lineEdit_94.text()
        client_id = self.lineEdit_95.text()
        self.mysql()
        self.cur.execute('''
        UPDATE clients SET client_name = %s, client_email = %s, client_id = %s WHERE client_id = %s
        ''', (client_name, client_email, client_id, client_original_id))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage("Client Info Updated ==>"+client_id)
        print("New client added "+client_name)

    def delete_client(self):
        client_original_id = self.lineEdit_4.text()
        warning = QMessageBox.warning(self, 'Delete Book ', "Are you sure to delete..?",
                                      QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.mysql()
            sql = '''DELETE FROM clients WHERE client_id = %s'''
            self.cur.execute(sql, [client_original_id])
            self.db.commit()
            self.db.close()
            self.statusBar().showMessage("Client Deleted ==>"+client_original_id)
            print("Client Deleted "+client_original_id)
            self.show_all_client()

    # Adding day-to-day operation
    def handle_day_operation(self):
        book_id = self.lineEdit.text()
        client_id = self.lineEdit_5.text()
        types = self.comboBox.currentText()
        days = self.comboBox_2.currentText()
        date = datetime.date.today()
        still = date + datetime.timedelta(days=int(days))
        print(still)
        self.mysql()
        self.cur.execute('''
           INSERT INTO day_operations( client_id,  book_id , type , day, date, still)
            VALUES(%s, %s, %s, %s, %s, %s)''', (client_id, book_id, types, days, date, still))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage("Client Deleted ==> "+client_id)
        print("Operation Added for client ID " + client_id)
        self.show_all_operation()

    def show_all_operation(self):
        self.mysql()
        self.cur.execute('''
        SELECT  client_id, book_id, type, date, still FROM day_operations''')
        data = self.cur.fetchall()
        print(data)
        if data:
            self.tableWidget.setRowCount(0)
            self.tableWidget.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)

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

    # mysql connect
    def mysql(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='', db='lab')
        self.cur = self.db.cursor()


def main():
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
