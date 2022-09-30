import db
import sys
import threading
import time

from PyQt6 import uic, QtCore
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QPushButton, QApplication, QMainWindow, QLineEdit, QTableWidget, QTextEdit, QStatusBar, QMessageBox, QMenu, QLabel, \
    QDialog, QDialogButtonBox, QTabWidget, QTableWidgetItem


class QuenstionWindow(QDialog):

    def __init__(self):
        super().__init__()
        uic.loadUi('edit_line.ui', self)
        self.text_line = self.findChild(QLineEdit, 'lineEdit')
        self.buttbox = self.findChild(QDialogButtonBox, 'buttonBox')
        self.buttbox.accepted.connect(self.click_ok)
        self.ok = False
        self.str = ''

    def click_ok(self):
        self.ok = True
        self.str = self.text_line.text()


class MainWindow(QMainWindow):
    table_ok = set([])
    st_update = False
    test_update = False
    t = 0

    def __init__(self):
        super().__init__()
        uic.loadUi('MainWindow.ui', self)

        self.create_db = self.findChild(QPushButton, 'pushButton_4')
        self.del_db = self.findChild(QPushButton, 'pushButton_5')
        self.save_db = self.findChild(QPushButton, 'pushButton')
        self.load_db = self.findChild(QPushButton, 'pushButton_2')
        self.switch_db = self.findChild(QPushButton, 'pushButton_3')
        self.add_st = self.findChild(QPushButton, 'pushButton_6')
        self.del_st = self.findChild(QPushButton, 'pushButton_10')
        self.load_st = self.findChild(QPushButton, 'pushButton_9')
        self.edit_st = self.findChild(QPushButton, 'pushButton_8')
        self.print_st = self.findChild(QPushButton, 'pushButton_7')
        self.add_tst = self.findChild(QPushButton, 'pushButton_11')
        self.del_tst = self.findChild(QPushButton, 'pushButton_15')
        self.load_tst = self.findChild(QPushButton, 'pushButton_14')
        self.edit_tst = self.findChild(QPushButton, 'pushButton_13')
        self.print_tst = self.findChild(QPushButton, 'pushButton_12')
        self.del_students = self.findChild(QPushButton, 'pushButton_16')
        self.del_tsts = self.findChild(QPushButton, 'pushButton_17')
        self.print_bases = self.findChild(QPushButton, 'pushButton_20')
        self.create_testing = self.findChild(QPushButton, 'pushButton_19')
        self.del_testing = self.findChild(QPushButton, 'pushButton_18')
        self.student_table = self.findChild(QTableWidget, 'tableWidget')
        self.test_table = self.findChild(QTableWidget, 'tableWidget_2')
        self.testing_table = self.findChild(QTableWidget, 'tableWidget_3')
        self.output = self.findChild(QTextEdit, 'textEdit')
        self.statusbar = self.findChild(QStatusBar, 'statusbar')
        self.exit = self.findChild(QAction, 'actionExit')
        self.basename = self.findChild(QLineEdit, 'lineEdit')
        self.st_name_id = self.findChild(QLineEdit, 'lineEdit_2')
        self.test_name_id = self.findChild(QLineEdit, 'lineEdit_3')
        self.menu = self.findChild(QMenu, 'menuFile')
        self.tool = self.findChild(QTabWidget, 'tabWidget')

        self.student_table.verticalHeader().setVisible(False)
        self.test_table.verticalHeader().setVisible(False)
        self.info = QLabel()
        self.msg = QLabel()
        self.info.setText('')
        self.msg.setText('')
        self.statusbar.addWidget(self.info)
        self.statusbar.addPermanentWidget(self.msg)

        self.del_testing.clicked.connect(self.delete_testing_table)
        self.del_tsts.clicked.connect(self.delete_tests)
        self.del_students.clicked.connect(self.delete_students)
        self.create_testing.clicked.connect(self.create_testing_table)
        self.print_bases.clicked.connect(self.print_dbs)
        self.print_tst.clicked.connect(self.print_test)
        self.edit_tst.clicked.connect(self.edit_test)
        self.load_tst.clicked.connect(self.fill_tests)
        self.del_tst.clicked.connect(self.delete_test)
        self.add_tst.clicked.connect(self.add_test)
        self.print_st.clicked.connect(self.print_student)
        self.edit_st.clicked.connect(self.edit_student)
        self.load_st.clicked.connect(self.fill_students)
        self.del_st.clicked.connect(self.del_student)
        self.add_st.clicked.connect(self.add_student)
        self.create_db.clicked.connect(self.create_base)
        self.save_db.clicked.connect(self.save_base)
        self.load_db.clicked.connect(self.load_base)
        self.switch_db.clicked.connect(self.switch_base)
        self.del_db.clicked.connect(self.delete_base)
        self.exit.triggered.connect(self.close_app)
        self.status_updater()

    def delete_testing_table(self):
        if db.curr_bd != -1:
            if len(db.bases[db.curr_bd][3]) != 0:
                a = self.get_msg('Confirmation', 'Are you sure?', QMessageBox.Icon.Question,
                                 QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                if a == 1024:
                    db.bases[db.curr_bd][3] = []
                    self.st_update = True
                    if db.bases[db.curr_bd][0] in self.table_ok:
                        self.table_ok.remove(db.bases[db.curr_bd][0])
                    self.testing_table.setRowCount(len(db.bases[db.curr_bd][3]))
                    self.succ_mes('Successfully deleted')
                    self.status_updater()
                else:
                    self.succ_mes('Deletion canceled')
            else:
                self.get_msg('Error', 'The table is empty')
        else:
            self.get_msg('Error', 'The base is not selected')

    def delete_tests(self):
        if db.curr_bd != -1:
            if len(db.bases[db.curr_bd][2]) != 0:
                a = self.get_msg('Confirmation', 'Are you sure?', QMessageBox.Icon.Question,
                                 QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                if a == 1024:
                    db.bases[db.curr_bd][2] = []
                    self.test_update = True
                    if db.bases[db.curr_bd][0] in self.table_ok:
                        self.table_ok.remove(db.bases[db.curr_bd][0])
                    self.succ_mes('Successfully deleted')
                    self.status_updater()
                else:
                    self.succ_mes('Deletion canceled')
            else:
                self.get_msg('Error', 'The table is empty')
        else:
            self.get_msg('Error', 'The base is not selected')

    def delete_students(self):
        if db.curr_bd != -1:
            if len(db.bases[db.curr_bd][1]) != 0:
                a = self.get_msg('Confirmation', 'Are you sure?', QMessageBox.Icon.Question,
                                 QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
                if a == 1024:
                    db.bases[db.curr_bd][1] = []
                    self.st_update = True
                    if db.bases[db.curr_bd][0] in self.table_ok:
                        self.table_ok.remove(db.bases[db.curr_bd][0])
                    self.succ_mes('Successfully deleted')
                    self.status_updater()
                else:
                    self.succ_mes('Deletion canceled')
            else:
                self.get_msg('Error', 'The table is empty')
        else:
            self.get_msg('Error', 'The base is not selected')

    def create_testing_table(self):
        a = db.create_testing_table()
        if a == -1:
            self.get_msg('Error', 'The base is not selected')
        elif a == -3:
            self.get_msg('Error', 'Empty student or test table')
        else:
            self.st_update = False
            self.test_update = False
            self.succ_mes('Successfully created')
            self.status_updater()

    def print_dbs(self):
        if len(db.bases) != 0:
            self.output.clear()
            self.tool.setCurrentIndex(3)
            for x in db.bases:
                self.output.append(x[0])
            self.succ_mes('Successfully printed')
        else:
            self.get_msg('Error', 'No data')

    def add_test(self):
        if len(self.test_name_id.text().strip()) != 0:
            a = db.add_test(self.test_name_id.text().strip())
            if a == -1:
                self.get_msg('Error', 'The base is not selected')
            elif a == 0:
                self.test_update = True
                if db.bases[db.curr_bd][0] in self.table_ok:
                    self.table_ok.remove(db.bases[db.curr_bd][0])
                self.status_updater()
                self.succ_mes('Successfully added')
            else:
                self.get_msg('Error', 'The test already exists')
        else:
            self.get_msg('Error', 'Input test')

    def fill_tests(self):
        if len(self.test_name_id.text().strip()) != 0:
            a = db.fill_tests(self.test_name_id.text().strip())
            if a == -3:
                self.get_msg('Error', 'File not found')
            elif a == -1:
                self.get_msg('Error', 'The base is not selected')
            else:
                self.test_update = True
                if db.bases[db.curr_bd][0] in self.table_ok:
                    self.table_ok.remove(db.bases[db.curr_bd][0])
                self.succ_mes('Successfully uploaded')
                self.status_updater()
        else:
            self.get_msg('Error', 'Input file name')

    def print_test(self):
        if self.test_name_id.text().strip().isdigit():
            a = db.print_test(int(self.test_name_id.text().strip()))
            if a == -3:
                self.get_msg('Error', 'Not found')
            elif a == -1:
                self.get_msg('Error', 'The base is not selected')
            else:
                self.succ_mes('Successfully printed')
                self.output.clear()
                self.output.append(a)
                self.tool.setCurrentIndex(3)
        else:
            self.get_msg('Error', 'Input test id')

    def edit_test(self):
        if self.test_name_id.text().strip().isdigit():
            dialog = QuenstionWindow()
            dialog.exec()
            if dialog.ok:
                if len(dialog.str.strip()) != 0:
                    a = db.edit_test(int(self.test_name_id.text().strip()), dialog.str.strip())
                    if a == -1:
                        self.get_msg('Error', 'The base is not selected')
                    elif a == -3:
                        self.get_msg('Error', 'Not found')
                    elif a == -2:
                        self.get_msg('Error', 'The test already exists')
                    else:
                        self.test_update = True
                        if db.bases[db.curr_bd][0] in self.table_ok:
                            self.table_ok.remove(db.bases[db.curr_bd][0])
                        self.status_updater()
                        self.succ_mes('Successfully updated')
                else:
                    self.get_msg('Error', 'Input test name')
            else:
                self.succ_mes('Editing canceled')
        else:
            self.get_msg('Error', 'Input test id')

    def delete_test(self):
        if self.test_name_id.text().strip().isdigit():
            a = self.get_msg('Confirmation', 'Are you sure?', QMessageBox.Icon.Question,
                             QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            if a == 1024:
                b = db.del_test(int(self.test_name_id.text().strip()))
                if b == -3:
                    self.get_msg('Error', 'Not found')
                elif b == -1:
                    self.get_msg('Error', 'The base is not selected')
                else:
                    self.test_update = True
                    if db.bases[db.curr_bd][0] in self.table_ok:
                        self.table_ok.remove(db.bases[db.curr_bd][0])
                    self.succ_mes('Successfully deleted')
                    self.status_updater()
            else:
                self.succ_mes('Deletion canceled')
        else:
            self.get_msg('Error', 'Input test id')

    def print_student(self):
        if self.st_name_id.text().strip().isdigit():
            a = db.print_student(int(self.st_name_id.text().strip()))
            if a == -1:
                self.get_msg('Error', 'The base is not selected')
            elif a == -3:
                self.get_msg('Error', 'Not found')
            else:
                self.succ_mes('Successfully printed')
                self.output.clear()
                self.output.append(a)
                self.tool.setCurrentIndex(3)
        else:
            self.get_msg('Error', 'Input student id')

    def edit_student(self):
        if self.st_name_id.text().strip().isdigit():
            dialog = QuenstionWindow()
            dialog.exec()
            if dialog.ok:
                if len(dialog.str.strip().split(' ')) == 3:
                    a = db.edit_student(int(self.st_name_id.text().strip()), dialog.str.strip())
                    if a == -1:
                        self.get_msg('Error', 'The base is not selected')
                    elif a == -3:
                        self.get_msg('Error', 'Not found')
                    else:
                        self.st_update = True
                        if db.bases[db.curr_bd][0] in self.table_ok:
                            self.table_ok.remove(db.bases[db.curr_bd][0])
                        self.succ_mes('Successfully updated')
                        self.status_updater()
                else:
                    self.get_msg('Error', 'Input student full name')
            else:
                self.succ_mes('Editing canceled')
        else:
            self.get_msg('Error', 'Input student id')

    def fill_students(self):
        if len(self.st_name_id.text().strip()) != 0:
            a = db.fill_students(self.st_name_id.text().strip())
            if a == -1:
                self.get_msg('Error', 'The base is not selected')
            elif a == -3:
                self.get_msg('Error', 'File not found')
            else:
                self.st_update = True
                if db.bases[db.curr_bd][0] in self.table_ok:
                    self.table_ok.remove(db.bases[db.curr_bd][0])
                self.succ_mes('Successfully uploaded')
                self.status_updater()
        else:
            self.get_msg('Error', 'Input file name')

    def add_student(self):
        if len(self.st_name_id.text().strip().split(' ')) == 3:
            a = db.add_student(self.st_name_id.text().strip())
            if a == -1:
                self.get_msg('Error', 'The base is not selected')
            else:
                self.st_update = True
                if db.bases[db.curr_bd][0] in self.table_ok:
                    self.table_ok.remove(db.bases[db.curr_bd][0])
                self.status_updater()
                self.succ_mes('Successfully added')
        else:
            self.get_msg('Error', 'Input student full name')

    def del_student(self):
        if self.st_name_id.text().strip().isdigit():
            a = self.get_msg('Confirmation', 'Are you sure?', QMessageBox.Icon.Question,
                             QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            if a == 1024:
                b = db.del_student(int(self.st_name_id.text().strip()))
                if b == -1:
                    self.get_msg('Error', 'The base is not selected')
                elif b == -3:
                    self.get_msg('Error', 'Not found')
                else:
                    self.st_update = True
                    if db.bases[db.curr_bd][0] in self.table_ok:
                        self.table_ok.remove(db.bases[db.curr_bd][0])
                    self.succ_mes('Successfully deleted')
                    self.status_updater()
            else:
                self.succ_mes('Deletion canceled')
        else:
            self.get_msg('Error', 'Input student id')

    def mes_edit(self, text, num):
        self.msg.setText(text)
        time.sleep(3)
        if self.t == num:
            self.msg.setText('')
            self.t = 0

    def succ_mes(self, text):
        self.t += 1
        t = threading.Thread(target=self.mes_edit, args=(text, self.t))
        t.start()

    def get_msg(self, name, text, icon=QMessageBox.Icon.Critical, butt=QMessageBox.StandardButton.Ok):
        msg = QMessageBox(parent=self, text=text)
        msg.setIcon(icon)
        msg.setWindowTitle(name)
        msg.setStandardButtons(butt)
        return msg.exec()

    def status_updater(self):
        if db.curr_bd == -1:
            self.info.setText(f'Current db: {None}')
            self.student_table.setRowCount(0)
            self.test_table.setRowCount(0)
            self.testing_table.setRowCount(0)
        else:
            self.student_table.setRowCount(len(db.bases[db.curr_bd][1]))
            for x in db.bases[db.curr_bd][1]:
                item = QTableWidgetItem(str(x[0]))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.student_table.setItem(x[0], 0, item)
                item = QTableWidgetItem(str(x[2]))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.student_table.setItem(x[0], 1, item)
                item = QTableWidgetItem(str(x[1]))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.student_table.setItem(x[0], 2, item)
                item = QTableWidgetItem(str(x[3]))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.student_table.setItem(x[0], 3, item)
            self.student_table.resizeColumnsToContents()
            self.test_table.setRowCount(len(db.bases[db.curr_bd][2]))
            for x in db.bases[db.curr_bd][2]:
                item = QTableWidgetItem(str(x[0]))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.test_table.setItem(x[0], 0, item)
                item = QTableWidgetItem(str(x[1]))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.test_table.setItem(x[0], 1, item)
            self.test_table.resizeColumnsToContents()
            if not (self.st_update or self.test_update):
                self.testing_table.setRowCount(len(db.bases[db.curr_bd][3]))
                for x in db.bases[db.curr_bd][3]:
                    item = QTableWidgetItem(
                        db.bases[db.curr_bd][1][x[0]][1] + ' ' + db.bases[db.curr_bd][1][x[0]][2] + ' ' + db.bases[db.curr_bd][1][x[0]][3])
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                    self.testing_table.setItem(x[0], 0, item)
                    item = QTableWidgetItem(db.bases[db.curr_bd][2][x[1]][1])
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
                    self.testing_table.setItem(x[0], 1, item)
                self.testing_table.resizeColumnsToContents()
            self.info.setText(
                f'Current db: {db.bases[db.curr_bd][0]} | Students: {len(db.bases[db.curr_bd][1])} | Tests: {len(db.bases[db.curr_bd][2])}'
                f' | Testing table ok: {"yes" if not (self.st_update or self.test_update) else "no"}')

    def save_base(self):
        if len(self.basename.text().strip()) != 0:
            if not (self.st_update or self.test_update):
                a = db.save_db(self.basename.text().strip())
                if a == -3:
                    self.get_msg('Error', 'Not found')
                else:
                    self.succ_mes('Successfully saved')
            else:
                self.get_msg('Error', 'Can\'t save a non-final testing table')
        else:
            self.get_msg('Error', 'Input base name')

    def load_base(self):
        if len(self.basename.text().strip()) != 0:
            a = db.load_db(self.basename.text().strip())
            if a == -1:
                self.get_msg('Error', 'Not found')
            else:
                self.st_update = False
                self.test_update = False
                self.table_ok.add(self.basename.text().strip())
                self.succ_mes('Successfully uploaded')
                self.status_updater()
        else:
            self.get_msg('Error', 'Input base name')

    def switch_base(self):
        if len(self.basename.text().strip()) != 0:
            tmp = db.curr_bd
            a = db.switch_bd(self.basename.text().strip())
            if a == -1:
                self.get_msg('Error', 'Not found')
            else:
                if not (self.st_update or self.test_update):
                    self.table_ok.add(db.bases[tmp][0])
                if db.bases[db.curr_bd][0] in self.table_ok:
                    self.st_update = False
                    self.test_update = False
                else:
                    self.st_update = True
                    self.test_update = True
                self.succ_mes('Successfully changed')
                self.status_updater()
        else:
            self.get_msg('Error', 'Input base name')

    def delete_base(self):
        if len(self.basename.text().strip()) != 0:
            a = self.get_msg('Confirmation', 'Are you sure?', QMessageBox.Icon.Question,
                             QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            if a == 1024:
                b = db.del_db(self.basename.text().strip())
                if b == -1:
                    self.get_msg('Error', 'Not found')
                else:
                    if self.basename.text().strip() in self.table_ok:
                        self.table_ok.remove(self.basename.text().strip())
                    self.succ_mes('Successfully deleted')
                    self.status_updater()
            else:
                self.succ_mes('Deletion canceled')
        else:
            self.get_msg('Error', 'Input base name')

    def create_base(self):
        if len(self.basename.text().strip()) != 0:
            a = db.create_db(self.basename.text().strip())
            if a == -1:
                self.get_msg('Error', 'Already exists')
            else:
                self.table_ok.add(db.bases[-1][0])
                self.succ_mes('Successfully created')
                self.status_updater()
        else:
            self.get_msg('Error', 'Input base name')

    def close_app(self):
        raise SystemExit


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
