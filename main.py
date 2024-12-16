import tkinter as tk
from database.db_setup import initialize_db
from gui.main_window import MainWindow
from gui.login import Login

''' Note
This function is for trial. For real usage we should comment this function
to not reset the db every time we restart the app.
'''

initialize_db()

root = tk.Tk()
root.title("Maintenance Scheduling System")
root.geometry("800x600")
root.resizable(False, False)

Login(root)

app = MainWindow(root)
root.mainloop()