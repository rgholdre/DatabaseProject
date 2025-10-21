import tkinter as tk
import database as db

# set-up main window
root = tk.Tk()
root.title("CS Class Search")
root.geometry("400x600")

def createStudentTable():
    db.runQuery(db.create_student_table)
def createInstructorTable():
    db.runQuery(db.create_instructor_table)
def createSectionTable():
    db.runQuery(db.create_section_table)    

def dropStudentTable():
    db.runQuery(db.drop_student_table)
def dropInstructorTable():
    db.runQuery(db.drop_instructor_table)
def dropSectionTable():
    db.runQuery(db.drop_section_table)

# Button definitions
CreateStudentButton = tk.Button(root, text="Create student Table", command=createStudentTable)
CreateInstructorButton = tk.Button(root, text="Create instructor Table", command=createInstructorTable)
CreateSectionButton = tk.Button(root, text="Create Section Table", command=createSectionTable)

DropStudentButton = tk.Button(root, text="Drop student Table", command=dropStudentTable)
DropInstructorButton = tk.Button(root, text="Drop Instructor Table", command=dropInstructorTable)
DropSectionButton = tk.Button(root, text="Drop section Table", command=dropSectionTable)


# Button placement on window
CreateStudentButton.pack(padx=10, pady=10)
CreateInstructorButton.pack(padx=20, pady=20)
CreateSectionButton.pack(padx=30, pady=30)

DropStudentButton.pack(padx=35, pady=35)
DropInstructorButton.pack(padx=40, pady=40)
DropSectionButton.pack(padx=45, pady=45)

root.mainloop()