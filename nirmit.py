import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
# Connect to the MySQL server
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nirmit",
    database="assignment_manager"
)

# Create a cursor object to interact with the database
cursor = db.cursor()

# Create the tables if they don't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        roll_no INT UNIQUE,
        name VARCHAR(255)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id INT,
        subject VARCHAR(255),
        chapter VARCHAR(255),
        assignment_no INT,
        assignment_type VARCHAR(255),
        marks_total INT,
        marks_gained INT,
        FOREIGN KEY (student_id) REFERENCES students(id)
    )
""")

class AssignmentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Assignment Manager")

        self.create_widgets()
        self.load_students()
        self.load_assignments()

    def create_widgets(self):
        # Create and configure tabs
        tab_control = ttk.Notebook(self.root)
        tab_control.pack(fill="both", expand="yes")

        students_tab = ttk.Frame(tab_control)
        assignments_tab = ttk.Frame(tab_control)

        tab_control.add(students_tab, text="Students")
        tab_control.add(assignments_tab, text="Assignments")

        # Create widgets for Students tab
        students_label = ttk.Label(students_tab, text="Students")
        students_label.pack(pady=10)

        self.students_listbox = tk.Listbox(students_tab, width=40, height=15)
        self.students_listbox.pack()

        students_scrollbar = tk.Scrollbar(students_tab)
        students_scrollbar.pack(side="right", fill="y")

        self.students_listbox.config(yscrollcommand=students_scrollbar.set)
        students_scrollbar.config(command=self.students_listbox.yview)

        add_student_button = ttk.Button(students_tab, text="Add Student", command=self.add_student_window)
        add_student_button.pack()

        edit_student_button = ttk.Button(students_tab, text="Edit Student", command=self.edit_student)
        edit_student_button.pack()

        delete_student_button = ttk.Button(students_tab, text="Delete Student", command=self.delete_student)
        delete_student_button.pack()

        self.search_mode_students = tk.StringVar()
        search_mode_students_label = ttk.Label(students_tab, text="Search Mode:")
        search_mode_students_label.pack()
        search_mode_students_exact = ttk.Radiobutton(students_tab, text="Exact Match", variable=self.search_mode_students, value="exact")
        search_mode_students_exact.pack()
        search_mode_students_partial = ttk.Radiobutton(students_tab, text="Partial Match", variable=self.search_mode_students, value="partial")
        search_mode_students_partial.pack()
        self.search_mode_students.set("exact")

        search_student_label = ttk.Label(students_tab, text="Search Student:")
        search_student_label.pack()
        self.search_student_entry = ttk.Entry(students_tab)
        self.search_student_entry.pack()
        search_student_button = ttk.Button(students_tab, text="Search", command=self.search_students)
        search_student_button.pack()

        self.students_listbox.bind("<Double-Button-1>", self.show_student_assignments)

        # Create widgets for Assignments tab
        assignments_label = ttk.Label(assignments_tab, text="Assignments")
        assignments_label.pack(pady=10)

        self.assignments_listbox = tk.Listbox(assignments_tab, width=60, height=15)
        self.assignments_listbox.pack()

        assignments_scrollbar = tk.Scrollbar(assignments_tab)
        assignments_scrollbar.pack(side="right", fill="y")

        self.assignments_listbox.config(yscrollcommand=assignments_scrollbar.set)
        assignments_scrollbar.config(command=self.assignments_listbox.yview)

        add_assignment_button = ttk.Button(assignments_tab, text="Add Assignment", command=self.add_assignment_window)
        add_assignment_button.pack()

        edit_assignment_button = ttk.Button(assignments_tab, text="Edit Assignment", command=self.edit_assignment)
        edit_assignment_button.pack()

        delete_assignment_button = ttk.Button(assignments_tab, text="Delete Assignment", command=self.delete_assignment)
        delete_assignment_button.pack()

        self.search_mode_assignments = tk.StringVar()
        search_mode_assignments_label = ttk.Label(assignments_tab, text="Search Mode:")
        search_mode_assignments_label.pack()
        search_mode_assignments_exact = ttk.Radiobutton(assignments_tab, text="Exact Match", variable=self.search_mode_assignments, value="exact")
        search_mode_assignments_exact.pack()
        search_mode_assignments_partial = ttk.Radiobutton(assignments_tab, text="Partial Match", variable=self.search_mode_assignments, value="partial")
        search_mode_assignments_partial.pack()
        self.search_mode_assignments.set("exact")

        search_assignment_label = ttk.Label(assignments_tab, text="Search Assignment:")
        search_assignment_label.pack()
        self.search_assignment_entry = ttk.Entry(assignments_tab)
        self.search_assignment_entry.pack()
        search_assignment_button = ttk.Button(assignments_tab, text="Search", command=self.search_assignments)
        search_assignment_button.pack()

        self.assignments_listbox.bind("<Double-Button-1>", self.show_students_assignment)

        self.students_assignment_label = ttk.Label(assignments_tab, text="Students who completed this assignment:")
        self.students_assignment_label.pack()
        self.students_assignment_listbox = tk.Listbox(assignments_tab, width=60, height=10)
        self.students_assignment_listbox.pack()

        self.student_assignments_label = ttk.Label(students_tab, text="Assignments done by this student with grades:")
        self.student_assignments_label.pack()
        self.student_assignments_listbox = tk.Listbox(students_tab, width=60, height=10)
        self.student_assignments_listbox.pack()

    def load_students(self):
        self.students_listbox.delete(0, tk.END)
        try:
            cursor.execute("SELECT * FROM students")
            students = cursor.fetchall()

            for student in students:
                self.students_listbox.insert(tk.END, f"ID: {student[0]}, Roll No: {student[1]}, Name: {student[2]}")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to load students: {error}")

    def load_assignments(self):
        self.assignments_listbox.delete(0, tk.END)
        try:
            cursor.execute("SELECT * FROM assignments")
            assignments = cursor.fetchall()

            for assignment in assignments:
                self.assignments_listbox.insert(tk.END, f"ID: {assignment[0]}, Subject: {assignment[2]}, Chapter: {assignment[3]}, Assignment No: {assignment[4]}, Type: {assignment[5]}, Marks Total: {assignment[6]}, Marks Gained: {assignment[7]}")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to load assignments: {error}")

    def add_student_window(self):
        add_student_window = tk.Toplevel(self.root)
        add_student_window.title("Add Student")

        label = ttk.Label(add_student_window, text="Add Student Details:")
        label.pack(pady=10)

        roll_no_label = ttk.Label(add_student_window, text="Roll No:")
        roll_no_label.pack()
        self.roll_no_entry = ttk.Entry(add_student_window)
        self.roll_no_entry.pack()

        name_label = ttk.Label(add_student_window, text="Name:")
        name_label.pack()
        self.name_entry = ttk.Entry(add_student_window)
        self.name_entry.pack()

        save_button = ttk.Button(add_student_window, text="Save", command=self.save_student)
        save_button.pack()

    def save_student(self):
        roll_no = self.roll_no_entry.get()
        name = self.name_entry.get()

        if not roll_no or not name:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            query = "INSERT INTO students (roll_no, name) VALUES (%s, %s)"
            values = (roll_no, name)
            cursor.execute(query, values)
            db.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            self.roll_no_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.load_students()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to add student: {error}")

    def edit_student(self):
        selected_student = self.students_listbox.curselection()
        if not selected_student:
            messagebox.showinfo("Info", "Please select a student to edit.")
            return

        selected_student = selected_student[0]
        student_info = self.students_listbox.get(selected_student)
        student_id = int(student_info.split(",")[0].split(":")[1].strip())

        try:
            cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
            student_data = cursor.fetchone()
            roll_no = student_data[1]
            name = student_data[2]
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to fetch student data: {error}")
            return

        edit_student_window = tk.Toplevel(self.root)
        edit_student_window.title("Edit Student")

        label = ttk.Label(edit_student_window, text="Edit Student Details:")
        label.pack(pady=10)

        roll_no_label = ttk.Label(edit_student_window, text="Roll No:")
        roll_no_label.pack()
        self.roll_no_entry_edit = ttk.Entry(edit_student_window)
        self.roll_no_entry_edit.pack()
        self.roll_no_entry_edit.insert(0, roll_no)

        name_label = ttk.Label(edit_student_window, text="Name:")
        name_label.pack()
        self.name_entry_edit = ttk.Entry(edit_student_window)
        self.name_entry_edit.pack()
        self.name_entry_edit.insert(0, name)

        save_button = ttk.Button(edit_student_window, text="Save", command=lambda: self.save_student_edit(student_id))
        save_button.pack()

    def save_student_edit(self, student_id):
        roll_no = self.roll_no_entry_edit.get()
        name = self.name_entry_edit.get()

        if not roll_no or not name:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            query = "UPDATE students SET roll_no = %s, name = %s WHERE id = %s"
            values = (roll_no, name, student_id)
            cursor.execute(query, values)
            db.commit()
            messagebox.showinfo("Success", "Student details updated successfully!")
            self.roll_no_entry_edit.delete(0, tk.END)
            self.name_entry_edit.delete(0, tk.END)
            self.load_students()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to update student details: {error}")

    def delete_student(self):
        selected_student = self.students_listbox.curselection()
        if not selected_student:
            messagebox.showinfo("Info", "Please select a student to delete.")
            return

        selected_student = selected_student[0]
        student_info = self.students_listbox.get(selected_student)
        student_id = int(student_info.split(",")[0].split(":")[1].strip())

        try:
            query = "DELETE FROM students WHERE id = %s"
            values = (student_id,)
            cursor.execute(query, values)
            db.commit()
            messagebox.showinfo("Success", "Student deleted successfully!")
            self.load_students()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to delete student: {error}")

    def add_assignment_window(self):
        add_assignment_window = tk.Toplevel(self.root)
        add_assignment_window.title("Add Assignment")

        label = ttk.Label(add_assignment_window, text="Add Assignment Details:")
        label.pack(pady=10)

        student_id_label = ttk.Label(add_assignment_window, text="Student ID:")
        student_id_label.pack()
        self.student_id_entry = ttk.Entry(add_assignment_window)
        self.student_id_entry.pack()

        subject_label = ttk.Label(add_assignment_window, text="Subject:")
        subject_label.pack()
        self.subject_entry = ttk.Entry(add_assignment_window)
        self.subject_entry.pack()

        chapter_label = ttk.Label(add_assignment_window, text="Chapter:")
        chapter_label.pack()
        self.chapter_entry = ttk.Entry(add_assignment_window)
        self.chapter_entry.pack()

        assignment_no_label = ttk.Label(add_assignment_window, text="Assignment No:")
        assignment_no_label.pack()
        self.assignment_no_entry = ttk.Entry(add_assignment_window)
        self.assignment_no_entry.pack()

        assignment_type_label = ttk.Label(add_assignment_window, text="Assignment Type:")
        assignment_type_label.pack()
        self.assignment_type_entry = ttk.Entry(add_assignment_window)
        self.assignment_type_entry.pack()

        marks_total_label = ttk.Label(add_assignment_window, text="Total Marks:")
        marks_total_label.pack()
        self.marks_total_entry = ttk.Entry(add_assignment_window)
        self.marks_total_entry.pack()

        marks_gained_label = ttk.Label(add_assignment_window, text="Marks Gained:")
        marks_gained_label.pack()
        self.marks_gained_entry = ttk.Entry(add_assignment_window)
        self.marks_gained_entry.pack()

        save_button = ttk.Button(add_assignment_window, text="Save", command=self.save_assignment)
        save_button.pack()

    def save_assignment(self):
        student_id = self.student_id_entry.get()
        subject = self.subject_entry.get()
        chapter = self.chapter_entry.get()
        assignment_no = self.assignment_no_entry.get()
        assignment_type = self.assignment_type_entry.get()
        marks_total = self.marks_total_entry.get()
        marks_gained = self.marks_gained_entry.get()

        if not student_id or not subject or not chapter or not assignment_no or not assignment_type or not marks_total or not marks_gained:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            query = "INSERT INTO assignments (student_id, subject, chapter, assignment_no, assignment_type, marks_total, marks_gained) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (student_id, subject, chapter, assignment_no, assignment_type, marks_total, marks_gained)
            cursor.execute(query, values)
            db.commit()
            messagebox.showinfo("Success", "Assignment added successfully!")
            self.clear_assignment_entries()
            self.load_assignments()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to add assignment: {error}")

    def clear_assignment_entries(self):
        self.student_id_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.chapter_entry.delete(0, tk.END)
        self.assignment_no_entry.delete(0, tk.END)
        self.assignment_type_entry.delete(0, tk.END)
        self.marks_total_entry.delete(0, tk.END)
        self.marks_gained_entry.delete(0, tk.END)

    def edit_assignment(self):
        selected_assignment = self.assignments_listbox.curselection()
        if not selected_assignment:
            messagebox.showinfo("Info", "Please select an assignment to edit.")
            return

        selected_assignment = selected_assignment[0]
        assignment_info = self.assignments_listbox.get(selected_assignment)
        assignment_id = int(assignment_info.split(",")[0].split(":")[1].strip())

        try:
            cursor.execute("SELECT * FROM assignments WHERE id = %s", (assignment_id,))
            assignment_data = cursor.fetchone()
            student_id = assignment_data[1]
            subject = assignment_data[2]
            chapter = assignment_data[3]
            assignment_no = assignment_data[4]
            assignment_type = assignment_data[5]
            marks_total = assignment_data[6]
            marks_gained = assignment_data[7]
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to fetch assignment data: {error}")
            return

        edit_assignment_window = tk.Toplevel(self.root)
        edit_assignment_window.title("Edit Assignment")

        label = ttk.Label(edit_assignment_window, text="Edit Assignment Details:")
        label.pack(pady=10)

        student_id_label = ttk.Label(edit_assignment_window, text="Student ID:")
        student_id_label.pack()
        self.student_id_entry_edit = ttk.Entry(edit_assignment_window)
        self.student_id_entry_edit.pack()
        self.student_id_entry_edit.insert(0, student_id)

        subject_label = ttk.Label(edit_assignment_window, text="Subject:")
        subject_label.pack()
        self.subject_entry_edit = ttk.Entry(edit_assignment_window)
        self.subject_entry_edit.pack()
        self.subject_entry_edit.insert(0, subject)

        chapter_label = ttk.Label(edit_assignment_window, text="Chapter:")
        chapter_label.pack()
        self.chapter_entry_edit = ttk.Entry(edit_assignment_window)
        self.chapter_entry_edit.pack()
        self.chapter_entry_edit.insert(0, chapter)

        assignment_no_label = ttk.Label(edit_assignment_window, text="Assignment No:")
        assignment_no_label.pack()
        self.assignment_no_entry_edit = ttk.Entry(edit_assignment_window)
        self.assignment_no_entry_edit.pack()
        self.assignment_no_entry_edit.insert(0, assignment_no)

        assignment_type_label = ttk.Label(edit_assignment_window, text="Assignment Type:")
        assignment_type_label.pack()
        self.assignment_type_entry_edit = ttk.Entry(edit_assignment_window)
        self.assignment_type_entry_edit.pack()
        self.assignment_type_entry_edit.insert(0, assignment_type)

        marks_total_label = ttk.Label(edit_assignment_window, text="Total Marks:")
        marks_total_label.pack()
        self.marks_total_entry_edit = ttk.Entry(edit_assignment_window)
        self.marks_total_entry_edit.pack()
        self.marks_total_entry_edit.insert(0, marks_total)

        marks_gained_label = ttk.Label(edit_assignment_window, text="Marks Gained:")
        marks_gained_label.pack()
        self.marks_gained_entry_edit = ttk.Entry(edit_assignment_window)
        self.marks_gained_entry_edit.pack()
        self.marks_gained_entry_edit.insert(0, marks_gained)

        save_button = ttk.Button(edit_assignment_window, text="Save", command=lambda: self.save_assignment_edit(assignment_id))
        save_button.pack()

    def save_assignment_edit(self, assignment_id):
        student_id = self.student_id_entry_edit.get()
        subject = self.subject_entry_edit.get()
        chapter = self.chapter_entry_edit.get()
        assignment_no = self.assignment_no_entry_edit.get()
        assignment_type = self.assignment_type_entry_edit.get()
        marks_total = self.marks_total_entry_edit.get()
        marks_gained = self.marks_gained_entry_edit.get()

        if not student_id or not subject or not chapter or not assignment_no or not assignment_type or not marks_total or not marks_gained:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            query = "UPDATE assignments SET student_id = %s, subject = %s, chapter = %s, assignment_no = %s, assignment_type = %s, marks_total = %s, marks_gained = %s WHERE id = %s"
            values = (student_id, subject, chapter, assignment_no, assignment_type, marks_total, marks_gained, assignment_id)
            cursor.execute(query, values)
            db.commit()
            messagebox.showinfo("Success", "Assignment details updated successfully!")
            self.load_assignments()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to update assignment details: {error}")

    def delete_assignment(self):
        selected_assignment = self.assignments_listbox.curselection()
        if not selected_assignment:
            messagebox.showinfo("Info", "Please select an assignment to delete.")
            return

        selected_assignment = selected_assignment[0]
        assignment_info = self.assignments_listbox.get(selected_assignment)
        assignment_id = int(assignment_info.split(",")[0].split(":")[1].strip())

        try:
            query = "DELETE FROM assignments WHERE id = %s"
            values = (assignment_id,)
            cursor.execute(query, values)
            db.commit()
            messagebox.showinfo("Success", "Assignment deleted successfully!")
            self.load_assignments()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to delete assignment: {error}")

    def search_students(self):
        search_query = self.search_student_entry.get()
        search_mode = self.search_mode_students.get()

        self.students_listbox.delete(0, tk.END)

        try:
            if search_mode == "exact":
                query = "SELECT * FROM students WHERE name = %s"
            elif search_mode == "partial":
                query = "SELECT * FROM students WHERE name LIKE %s"
                search_query = f"%{search_query}%"
            else:
                return

            values = (search_query,)
            cursor.execute(query, values)
            students = cursor.fetchall()

            for student in students:
                self.students_listbox.insert(tk.END, f"ID: {student[0]}, Roll No: {student[1]}, Name: {student[2]}")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to search students: {error}")

    def search_assignments(self):
        search_query = self.search_assignment_entry.get()
        search_mode = self.search_mode_assignments.get()

        self.assignments_listbox.delete(0, tk.END)

        try:
            if search_mode == "exact":
                query = "SELECT * FROM assignments WHERE subject = %s"
            elif search_mode == "partial":
                query = "SELECT * FROM assignments WHERE subject LIKE %s"
                search_query = f"%{search_query}%"
            else:
                return

            values = (search_query,)
            cursor.execute(query, values)
            assignments = cursor.fetchall()

            for assignment in assignments:
                self.assignments_listbox.insert(tk.END, f"ID: {assignment[0]}, Subject: {assignment[2]}, Chapter: {assignment[3]}, Assignment No: {assignment[4]}, Type: {assignment[5]}, Marks Total: {assignment[6]}, Marks Gained: {assignment[7]}")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to search assignments: {error}")

    def show_student_assignments(self, event):
        selected_student = self.students_listbox.curselection()
        if not selected_student:
            return

        selected_student = selected_student[0]
        student_info = self.students_listbox.get(selected_student)
        student_id = int(student_info.split(",")[0].split(":")[1].strip())

        try:
            query = "SELECT subject, assignment_no, assignment_type, marks_total, marks_gained FROM assignments WHERE student_id = %s"
            values = (student_id,)
            cursor.execute(query, values)
            assignments = cursor.fetchall()

            self.student_assignments_listbox.delete(0, tk.END)

            for assignment in assignments:
                subject = assignment[0]
                assignment_no = assignment[1]
                assignment_type = assignment[2]
                marks_total = assignment[3]
                marks_gained = assignment[4]

                self.student_assignments_listbox.insert(tk.END, f"Subject: {subject}, Assignment No: {assignment_no}, Type: {assignment_type}, Marks Total: {marks_total}, Marks Gained: {marks_gained}")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to fetch student assignments: {error}")

    def show_students_assignment(self, event):
        selected_assignment = self.assignments_listbox.curselection()
        if not selected_assignment:
            return

        selected_assignment = selected_assignment[0]
        assignment_info = self.assignments_listbox.get(selected_assignment)
        assignment_id = int(assignment_info.split(",")[0].split(":")[1].strip())

        try:
            query = "SELECT students.name, assignments.marks_gained FROM students INNER JOIN assignments ON students.id = assignments.student_id WHERE assignments.id = %s"
            values = (assignment_id,)
            cursor.execute(query, values)
            students = cursor.fetchall()

            self.students_assignment_listbox.delete(0, tk.END)

            for student in students:
                student_name = student[0]
                marks_gained = student[1]

                self.students_assignment_listbox.insert(tk.END, f"Student Name: {student_name}, Marks Gained: {marks_gained}")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to fetch students for assignment: {error}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AssignmentManagerApp(root)
    root.mainloop()

    # Close the database connection
    db.close()
    print('''Thank you for using Assignment Manager!          
            Hope you liked it!
            THIS TOOK DAYS OF EFFORT TO MAKE!
            ALSO IT'S EXACTLY 600 LINES OF CODE!
          ''')
