import sys
import mysql.connector as mcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QComboBox, QTextEdit, QMessageBox
import random 

class HouseShufflerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up the main window
        self.setWindowTitle('House Shuffler')
        self.setGeometry(100, 100, 600, 400)
        
        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Define widgets
        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText('Enter Host')
        
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText('Enter User')
        
        self.passwd_input = QLineEdit()
        self.passwd_input.setPlaceholderText('Enter Password')
        self.passwd_input.setEchoMode(QLineEdit.Password)
        
        self.database_input = QLineEdit()
        self.database_input.setPlaceholderText('Enter Database')

        self.admno_input = QLineEdit()
        self.admno_input.setPlaceholderText('Enter Admission Number')

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Enter Name of student to be added')

        self.grade_input = QLineEdit()
        self.grade_input.setPlaceholderText('Enter Grade of student to be added')
        
        self.record_text = QTextEdit()
        self.record_text.setReadOnly(True)
        
        self.house_combo = QComboBox()
        self.house_combo.addItems(["Fathima", "Montfort", "Joseph", "Gabriel"])
        
        self.delete_record_button = QPushButton('Delete Record')
        self.show_record_button = QPushButton('Show Record and House')
        self.show_house_button = QPushButton('Show Students in House')
        self.add_record_button = QPushButton('Add Record')
        
        # Add widgets to layout
        self.layout.addWidget(self.host_input)
        self.layout.addWidget(self.user_input)
        self.layout.addWidget(self.passwd_input)
        self.layout.addWidget(self.database_input)
        self.layout.addWidget(self.admno_input)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.grade_input)
        self.layout.addWidget(self.delete_record_button)
        self.layout.addWidget(self.show_record_button)
        self.layout.addWidget(self.show_house_button)
        self.layout.addWidget(self.add_record_button)
        self.layout.addWidget(self.house_combo)
        self.layout.addWidget(self.record_text)
        
        # Connect buttons to methods
        self.delete_record_button.clicked.connect(self.delete_record)
        self.show_record_button.clicked.connect(self.show_record)
        self.show_house_button.clicked.connect(self.show_house)
        self.add_record_button.clicked.connect(self.add_record)
    
    def get_db_connection(self):
        host = self.host_input.text()
        user = self.user_input.text()
        passwd = self.passwd_input.text()
        database = self.database_input.text()
        
        return mcon.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
        )
    
    def delete_record(self):
        admno = self.admno_input.text()
        if not admno:
            QMessageBox.warning(self, 'Input Error', 'Please enter an admission number')
            return

        conn = self.get_db_connection()
        cur = conn.cursor()
        try:
            # Delete from achievements table
            cur.execute("DELETE FROM Achievements WHERE admno = %s", (admno,))
            # Delete from students table
            cur.execute("DELETE FROM students WHERE admno = %s", (admno,))
            conn.commit()
            QMessageBox.information(self, 'Success', 'Record deleted successfully')
        except mcon.Error as err:
            QMessageBox.critical(self, 'Database Error', f'Error: {err}')
        finally:
            cur.close()
            conn.close()

    def show_record(self):
        admno = self.admno_input.text()
        if not admno:
            QMessageBox.warning(self, 'Input Error', 'Please enter an admission number')
            return

        conn = self.get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT s.admno, s.name, s.house FROM students s
                WHERE s.admno = %s
            """, (admno,))
            result = cur.fetchone()
            if result:
                self.record_text.setText(f"Admission Number: {result[0]}\nName: {result[1]}\nHouse: {result[2]}")
            else:
                self.record_text.setText('No record found')
        except mcon.Error as err:
            QMessageBox.critical(self, 'Database Error', f'Error: {err}')
        finally:
            cur.close()
            conn.close()

    def show_house(self):
        house = self.house_combo.currentText()
        conn = self.get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT admno, name FROM students
                WHERE house = %s
            """, (house,))
            results = cur.fetchall()
            student_list = "\n".join([f"{admno[0]} - {admno[1]}" for admno in results])
            self.record_text.setText(f"Students in {house}:\n{student_list}")
        except mcon.Error as err:
            QMessageBox.critical(self, 'Database Error', f'Error: {err}')
        finally:
            cur.close()
            conn.close()

    def add_record(self):
        admno = self.admno_input.text()
        name = self.name_input.text()
        grade = self.grade_input.text()
        if not admno or not name or not grade:
            QMessageBox.warning(self, 'Input Error', 'Please enter an admission number, name, and grade')
            return

        # List of available houses
        houses = ["Fathima", "Montfort", "Joseph", "Gabriel"]

        # Randomly select a house
        house = random.choice(houses)

        conn = self.get_db_connection()
        cur = conn.cursor()
        try:
            # Insert the new record into the `students` table with the randomly assigned house and grade
            cur.execute(f"INSERT INTO students (admno, name, grade, house) VALUES (%s, %s, %s, %s)", 
                        (admno, name, grade, house))
            conn.commit()
            QMessageBox.information(self, 'Success', f'Record added successfully with house assignment: {house}')
        except mcon.Error as err:
            QMessageBox.critical(self, 'Database Error', f'Error: {err}')
        finally:
            cur.close()
            conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HouseShufflerApp()
    window.show()
    sys.exit(app.exec_())
