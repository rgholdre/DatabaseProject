import tkinter as tk
import database as db

# set-up main window
root = tk.Tk()
root.title("CS Class Search")
root.geometry("400x300")

def createTable():
    db.runQuery(db.create_test_table)
def dropTable():
    db.runQuery(db.drop_test_table)

# Button definitions
CreateButton = tk.Button(root, text="Create Test Table", command=createTable)
DropButton = tk.Button(root, text="Drop Test Table", command=dropTable)

# Button placement on window
CreateButton.pack(padx=10, pady=10)
DropButton.pack(padx=20, pady=20)

root.mainloop()