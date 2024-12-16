import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


class TaskManagement:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Manage Maintenance Tasks")
        self.window.geometry("800x500")
        self.window.resizable(False, False)

        ttk.Label(self.window, text="Manage Maintenance Tasks", font=("Arial", 18)).pack(pady=10)

        form_frame = ttk.Frame(self.window)
        form_frame.pack(pady=10, padx=20, fill=tk.X)

        ttk.Label(form_frame, text="Machine:").grid(row=0, column=0, padx=10, pady=5, sticky="W")
        self.machine_combo = ttk.Combobox(form_frame, state="readonly")
        self.machine_combo.grid(row=0, column=1, padx=10, pady=5, sticky="W")

        ttk.Label(form_frame, text="Maintenance Type:").grid(row=1, column=0, padx=10, pady=5, sticky="W")
        self.maintenance_type_combo = ttk.Combobox(form_frame, values=["Inspection", "Repair", "Calibration"], state="readonly")
        self.maintenance_type_combo.grid(row=1, column=1, padx=10, pady=5, sticky="W")

        ttk.Label(form_frame, text="Date Scheduled:").grid(row=2, column=0, padx=10, pady=5, sticky="W")
        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.grid(row=2, column=1, padx=10, pady=5, sticky="W")

        ttk.Label(form_frame, text="Technician Name:").grid(row=3, column=0, padx=10, pady=5, sticky="W")
        self.technician_entry = ttk.Entry(form_frame)
        self.technician_entry.grid(row=3, column=1, padx=10, pady=5, sticky="W")

        ttk.Label(form_frame, text="Status:").grid(row=4, column=0, padx=10, pady=5, sticky="W")
        self.status_combo = ttk.Combobox(form_frame, values=["Scheduled", "Completed", "Pending"], state="readonly")
        self.status_combo.grid(row=4, column=1, padx=10, pady=5, sticky="W")

        action_frame = ttk.Frame(self.window)
        action_frame.pack(pady=10)

        ttk.Button(action_frame, text="Add Task", command=self.add_task).grid(row=0, column=0, padx=10)
        ttk.Button(action_frame, text="Clear Form", command=self.clear_form).grid(row=0, column=1, padx=10)
        ttk.Button(action_frame, text="Close", command=self.window.destroy).grid(row=0, column=2, padx=10)

        self.tree = ttk.Treeview(self.window, columns=("ID", "Machine", "Type", "Date", "Technician", "Status"), show="headings")
        self.tree.heading("ID", text="Task ID")
        self.tree.heading("Machine", text="Machine")
        self.tree.heading("Type", text="Maintenance Type")
        self.tree.heading("Date", text="Date Scheduled")
        self.tree.heading("Technician", text="Technician")
        self.tree.heading("Status", text="Status")

        self.tree.column("ID", width=50)
        self.tree.column("Machine", width=150)
        self.tree.column("Type", width=150)
        self.tree.column("Date", width=150)
        self.tree.column("Technician", width=150)
        self.tree.column("Status", width=100)

        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        self.load_machines()
        self.load_tasks()

    def clear_form(self):
        self.machine_combo.set("")
        self.maintenance_type_combo.set("")
        self.date_entry.delete(0, tk.END)
        self.technician_entry.delete(0, tk.END)
        self.status_combo.set("")

    def load_machines(self):
        conn = sqlite3.connect('maintenance.db')
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT id, name FROM machines")
            machines = cursor.fetchall()
            machine_list = [f"{mid}: {mname}" for mid, mname in machines]
            self.machine_combo["values"] = machine_list
        except Exception as e:
            messagebox.showerror("Database Error", 
                                 f"Error: {str(e)}")
        finally:
            conn.close()

    def load_tasks(self):
        for record in self.tree.get_children():
            self.tree.delete(record)

        conn = sqlite3.connect('maintenance.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT 
                    mt.id, m.name, mt.maintenance_type, mt.date_scheduled, mt.technician_name, mt.status
                FROM 
                    maintenance_tasks mt
                JOIN 
                    machines m ON mt.machine_id = m.id
                ORDER BY
                    mt.id ASC
            ''')
            tasks = cursor.fetchall()

            for task in tasks:
                self.tree.insert("", tk.END, values=task)

        except Exception as e:
            messagebox.showerror("Database Error", 
                                 f"Error: {str(e)}")

        finally:
            conn.close()

    def add_task(self):
        machine_id = self.machine_combo.get().split(":")[0].strip()
        maintenance_type = self.maintenance_type_combo.get()
        date_scheduled = self.date_entry.get().strip()
        technician_name = self.technician_entry.get().strip()
        status = self.status_combo.get()

        if not all([machine_id, maintenance_type, date_scheduled, technician_name, status]):
            messagebox.showwarning("Validation Error", 
                                   "All fields must be filled out!")
            return

        conn = sqlite3.connect('maintenance.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO 
                    maintenance_tasks (machine_id, maintenance_type, date_scheduled, technician_name, status)
                VALUES 
                    (?, ?, ?, ?, ?)
            ''', (machine_id, maintenance_type, date_scheduled, technician_name, status))

            task_id = cursor.lastrowid

            if status == "Completed":
                cursor.execute('''
                    INSERT INTO
                        maintenance_history (task_id, completion_date, remarks)
                    VALUES 
                        (?, ?, ?)
                ''', (task_id, date_scheduled, f"{maintenance_type} completed by {technician_name}"))

            conn.commit()
            messagebox.showinfo("Success", "Maintenance task added successfully!")
            self.load_tasks()
            self.clear_form()

        except Exception as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")

        finally:
            conn.close()