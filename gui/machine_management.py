import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


class MachineManagement:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Manage Machines")
        self.window.geometry("600x400")
        self.window.resizable(False, False)

        ttk.Label(self.window, text="Manage Machines", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(self.window, text="Machine Name:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.machine_name = ttk.Entry(self.window)
        self.machine_name.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.window, text="Location:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.location = ttk.Entry(self.window)
        self.location.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(self.window, text="Type:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.machine_type = ttk.Entry(self.window)
        self.machine_type.grid(row=3, column=1, padx=10, pady=10)

        ttk.Label(self.window, text="Status:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.status = ttk.Combobox(self.window, values=["Operational", "Maintenance Required", "Offline"])
        self.status.grid(row=4, column=1, padx=10, pady=10)

        ttk.Button(self.window, text="Add Machine", command=self.add_machine).grid(row=5, column=0, padx=10, pady=20)
        ttk.Button(self.window, text="Close", command=self.window.destroy).grid(row=5, column=1, padx=10, pady=20)

    def add_machine(self):
        if not all([self.machine_name.get(), self.location.get(), self.machine_type.get(), self.status.get()]):
            messagebox.showwarning("Validation Error", 
                                   "All fields must be filled out!")
            return

        conn = sqlite3.connect('maintenance.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO 
                    machines (name, location, type, status)
                VALUES 
                    (?, ?, ?, ?)
            ''', (self.machine_name.get(), self.location.get(), self.machine_type.get(), self.status.get()))

            conn.commit()
            messagebox.showinfo("Success", 
                                "Machine added successfully!")
        except Exception as e:
            messagebox.showerror("Database Error", 
                                 f"Error: {str(e)}")
        finally:
            conn.close()