import tkinter as tk
from tkinter import messagebox
import sqlite3

class Login:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("User Login")
        self.window.geometry("400x300")
        self.window.resizable(False, False)

        tk.Label(self.window, text="Login", font=("Arial", 24)).pack(pady=20)

        tk.Label(self.window, text="Username:", font=("Arial", 12)).pack(pady=5)
        self.username_entry = tk.Entry(self.window, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(self.window, text="Password:", font=("Arial", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self.window, width=30, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.window, text="Login", command=self.authenticate_user).pack(pady=20)
        tk.Button(self.window, text="Close", command=self.window.destroy).pack()

    def authenticate_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Validation Error", 
                                   "Please fill in all fields!")
            return

        conn = sqlite3.connect('maintenance.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT 
                    * 
                FROM 
                    users 
                WHERE 
                    username = ? AND password = ?
            ''', (username, password))

            user = cursor.fetchone()

            if user:
                messagebox.showinfo("Success", 
                                    f"Welcome {username}!")
                self.window.destroy()
            else:
                messagebox.showerror("Login Failed", 
                                     "Incorrect username or password!")
        except Exception as e:
            messagebox.showerror("Database Error", 
                                 f"Error: {str(e)}")
        finally:
            conn.close()