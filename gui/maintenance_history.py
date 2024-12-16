import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


class MaintenanceHistory:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Maintenance History")
        self.window.geometry("800x400")
        self.window.resizable(False, False)

        ttk.Label(self.window, text="Maintenance History", font=("Arial", 18)).pack(pady=10)

        self.tree = ttk.Treeview(
            self.window, 
            columns=("ID", "Machine", "Maintenance Type", "Completion Date", "Remarks"), 
            show='headings'
        )
        self.tree.heading("ID", text="Task ID")
        self.tree.heading("Machine", text="Machine")
        self.tree.heading("Maintenance Type", text="Maintenance Type")
        self.tree.heading("Completion Date", text="Completion Date")
        self.tree.heading("Remarks", text="Remarks")

        self.tree.column("ID", width=50)
        self.tree.column("Machine", width=150)
        self.tree.column("Maintenance Type", width=150)
        self.tree.column("Completion Date", width=150)
        self.tree.column("Remarks", width=250)

        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        action_frame = ttk.Frame(self.window)
        action_frame.pack(pady=10)

        ttk.Button(action_frame, text="Refresh", command=self.load_data).grid(row=0, column=0, padx=10)
        ttk.Button(action_frame, text="Close", command=self.window.destroy).grid(row=0, column=1, padx=10)

        self.load_data()

    def load_data(self):
        for record in self.tree.get_children():
            self.tree.delete(record)

        conn = sqlite3.connect('maintenance.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT 
                    mh.id, 
                    m.name, 
                    mt.maintenance_type, 
                    mh.completion_date, 
                    mh.remarks
                FROM 
                    maintenance_history mh
                JOIN 
                    maintenance_tasks mt ON mh.task_id = mt.id
                JOIN
                    machines m ON mt.machine_id = m.id
                ORDER BY
                    mh.id ASC
            ''')
            records = cursor.fetchall()

            if not records:
                messagebox.showinfo("No Records Found", 
                                    "No maintenance history records found.")

            for row in records:
                self.tree.insert("", tk.END, values=row)

        except Exception as e:
            messagebox.showerror("Database Error", 
                                 f"Error: {str(e)}")

        finally:
            conn.close()

    def mark_completed(self):
        """ Mark a task as completed and add it to the maintenance history """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", 
                                   "Please select a task to mark as completed.")
            return

        task_id = self.tree.item(selected_item[0])["values"][0]  
        conn = sqlite3.connect('maintenance.db')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE 
                    maintenance_tasks
                SET 
                    status = 'Completed'
                WHERE
                    id = ?
            ''', (task_id,))

            cursor.execute('''
                INSERT INTO 
                    maintenance_history (task_id, completion_date, remarks)
                SELECT 
                    id, date_scheduled, maintenance_type || ' completed by ' || technician_name
                FROM 
                    maintenance_tasks
                WHERE 
                    id = ?
            ''', (task_id,))

            conn.commit()
            messagebox.showinfo("Success", 
                                "Task marked as completed and added to maintenance history.")
            self.load_data()

        except Exception as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}")

        finally:
            conn.close()