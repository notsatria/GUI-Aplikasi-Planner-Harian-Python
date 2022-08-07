import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem, QMessageBox
import sqlite3
from qtconsole.qtconsoleapp import QtCore


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("D:/Python Projects/UAS Daspro GUI/main2.ui", self)
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarDateChanged()
        self.saveButton.clicked.connect(self.saveChanges)
        self.addButton.clicked.connect(self.addNewTask)
        self.hapusButton.clicked.connect(self.clear)
        
    def calendarDateChanged(self):
        print("Tanggal berhasil diubah")
        dateSelected = self.calendarWidget.selectedDate().toPyDate()
        print("Tanggal terpilih:", dateSelected)
        self.updateTaskList(dateSelected)

    def updateTaskList(self, date):
        self.taskListWidget.clear()
        db = sqlite3.connect("D:/Python Projects/UAS Daspro GUI/data.db")
        cursor = db.cursor()
        sql = "SELECT task, completed FROM tasks WHERE date = ?"
        row = (date, )
        results = cursor.execute(sql, row).fetchall()
        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if result[1] == "YES":
                item.setCheckState(QtCore.Qt.Checked)
            elif result[1] == "NO":
                item.setCheckState(QtCore.Qt.Unchecked)  
            self.taskListWidget.addItem(item)

    def saveChanges(self):
        db = sqlite3.connect("D:/Python Projects/UAS Daspro GUI/data.db")
        cursor = db.cursor()
        date = self.calendarWidget.selectedDate().toPyDate()

        for i in range(self.taskListWidget.count()):
            item = self.taskListWidget.item(i)
            task = item.text()
            if item.checkState() == QtCore.Qt.Checked:
                query = "UPDATE tasks SET completed = 'YES' WHERE task = ? AND date = ?"
            else:
                query = "UPDATE tasks SET completed = 'NO' WHERE task = ? AND date = ?"
            row = (task, date,)
            cursor.execute(query, row)
        db.commit()
        messageBox = QMessageBox()
        messageBox.setText("Data Disimpan.")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()

    def addNewTask(self):
        db = sqlite3.connect("D:/Python Projects/UAS Daspro GUI/data.db")
        cursor = db.cursor()

        newTask = str(self.taskLineEdit.text())
        date = self.calendarWidget.selectedDate().toPyDate()

        query = "INSERT INTO tasks(task, completed, date) VALUES (?,?,?)"
        row = (newTask, "NO", date,)

        cursor.execute(query, row)
        db.commit()
        self.updateTaskList(date)
        self.taskLineEdit.clear()

    def clear(self):
        self.taskListWidget.clear()
        db = sqlite3.connect("D:/Python Projects/UAS Daspro GUI/data.db")
        cursor = db.cursor()

        date = self.calendarWidget.selectedDate().toPyDate()
        date = str(date)
        query = "DELETE FROM tasks WHERE date = ?" 
        row = (date,)

        cursor.execute(query, row)
        db.commit()
        
        messageBox = QMessageBox()
        messageBox.setText("Data Dihapus.")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()
        self.updateTaskList(date)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
