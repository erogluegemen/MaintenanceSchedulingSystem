import csv
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class ReportGeneration:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Generate Maintenance Reports")
        self.window.geometry("800x500")
        self.window.resizable(False, False)

        ttk.Label(self.window, text="Generate Maintenance Reports", font=("Arial", 18)).pack(pady=10)

        filter_frame = ttk.Frame(self.window)
        filter_frame.pack(pady=10)

        self.status_translation = {
            "All": "Hepsi",
            "Scheduled": "Planlandı",
            "Pending": "Bekliyor",
            "Completed": "Tamamlandı"
        }

        ttk.Label(filter_frame, text="Filter by Status:").grid(row=0, column=0, padx=5, pady=5)
        self.status_combo = ttk.Combobox(filter_frame, values=list(self.status_translation.keys()), state="readonly")
        self.status_combo.grid(row=0, column=1, padx=5, pady=5)
        self.status_combo.current(0)

        ttk.Button(filter_frame, text="Generate Report", command=self.generate_report).grid(row=0, column=2, padx=10)
        ttk.Button(filter_frame, text="Export to CSV", command=self.export_to_csv).grid(row=0, column=3, padx=10)

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

        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)
        self.current_records = []

    def generate_report(self):
        selected_status = self.status_combo.get()
        for record in self.tree.get_children():
            self.tree.delete(record)

        conn = sqlite3.connect('maintenance.db')
        cursor = conn.cursor()

        try:
            if selected_status == "All":
                query = '''
                    SELECT 
                        mt.id, m.name, mt.maintenance_type, mt.date_scheduled, mt.technician_name, mt.status
                    FROM 
                        maintenance_tasks mt
                    JOIN 
                        machines m ON mt.machine_id = m.id
                '''
                cursor.execute(query)
            else:
                translated_status = self.status_translation[selected_status]
                query = '''
                    SELECT 
                        mt.id, m.name, mt.maintenance_type, mt.date_scheduled, mt.technician_name, mt.status
                    FROM 
                        maintenance_tasks mt
                    JOIN 
                        machines m ON mt.machine_id = m.id
                    WHERE 
                        mt.status = ?
                '''
                cursor.execute(query, (translated_status,))

            self.current_records = cursor.fetchall()
            for row in self.current_records:
                self.tree.insert("", tk.END, values=row)

            if not self.current_records:
                messagebox.showinfo("No Data", 
                                    "No records found for the selected filter.")

        except Exception as e:
            messagebox.showerror("Database Error", 
                                 f"Error: {str(e)}")
        finally:
            conn.close()

    def export_to_csv(self):
        if not self.current_records:
            messagebox.showwarning("No Data",
                                   "Please generate a report before exporting.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save Report As"
        )

        if not file_path:
            return  
        try:
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Task ID", "Machine", "Maintenance Type", "Date Scheduled", "Technician", "Status"])
                writer.writerows(self.current_records)
            messagebox.showinfo("Success", f"Report exported successfully!")

        except Exception as e:
            messagebox.showerror("File Error", f"Error: {str(e)}")
