import sqlite3
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Dashboard:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Dashboard")
        self.window.geometry("800x600")
        self.window.resizable(False, False)

        ttk.Label(self.window, text="Dashboard Overview", font=("Arial", 24)).pack(pady=10)

        cards_frame = tk.Frame(self.window, bg="#333")
        cards_frame.pack(pady=10)

        self.card_values = []  
        self.card_values.append(self.create_card(cards_frame, "Total Machines", "0", 0, 0))
        self.card_values.append(self.create_card(cards_frame, "Pending Tasks", "0", 0, 1))
        self.card_values.append(self.create_card(cards_frame, "Completed Tasks", "0", 1, 0))
        self.card_values.append(self.create_card(cards_frame, "Upcoming Maintenance", "0", 1, 1))

        self.chart_data = {}  
        self.load_dashboard_data()

        self.chart_frame = tk.Frame(self.window)
        self.chart_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        self.draw_chart()

    def create_card(self, parent, title, value, row, column):
        card_frame = tk.Frame(parent, bg="#444", relief="ridge", bd=3)
        card_frame.grid(row=row, column=column, padx=20, pady=20, sticky="nsew")

        title_label = tk.Label(card_frame, text=title, font=("Arial", 14), bg="#444", fg="white")
        title_label.pack(pady=10, padx=10)

        value_label = tk.Label(card_frame, text=value, font=("Arial", 20, "bold"), bg="#444", fg="#4CAF50")
        value_label.pack(pady=10, padx=10)

        card_frame.config(width=200, height=100)
        return value_label 

    def load_dashboard_data(self):
        conn = sqlite3.connect('maintenance.db')
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT COUNT(*) FROM machines")
            machines_count = cursor.fetchone()[0]
            self.update_card_value(0, machines_count)

            cursor.execute("SELECT COUNT(*) FROM maintenance_tasks WHERE status = 'Pending' or status = 'Bekliyor'")
            pending_tasks_count = cursor.fetchone()[0]
            self.update_card_value(1, pending_tasks_count)

            cursor.execute("SELECT COUNT(*) FROM maintenance_tasks WHERE status = 'Completed' or status = 'Tamamlandı'")
            completed_tasks_count = cursor.fetchone()[0]
            self.update_card_value(2, completed_tasks_count)

            cursor.execute("SELECT COUNT(*) FROM maintenance_tasks WHERE status = 'Scheduled' or status = 'Planlandı'")
            upcoming_tasks_count = cursor.fetchone()[0]
            self.update_card_value(3, upcoming_tasks_count)

            self.chart_data = {
                "Total Machines": machines_count,
                "Pending Tasks": pending_tasks_count,
                "Completed Tasks": completed_tasks_count,
                "Upcoming Maintenance": upcoming_tasks_count
            }

        except Exception as e:
            print(f"Database Error: {str(e)}")
        finally:
            conn.close()

    def update_card_value(self, index, value):
        self.card_values[index].config(text=value)

    def draw_chart(self):
        if not self.chart_data:
            self.chart_data = {"Total Machines": 0, 
                               "Pending Tasks": 0, 
                               "Completed Tasks": 0, 
                               "Upcoming Maintenance": 0}

        figure = Figure(figsize=(6, 4), dpi=100)
        ax = figure.add_subplot(1, 1, 1)

        categories = list(self.chart_data.keys())
        values = list(self.chart_data.values())

        ax.bar(categories, values, color=['#4CAF50', '#FFC107', '#2196F3', '#FF5722'])
        ax.set_title("Maintenance Overview")

        chart_canvas = FigureCanvasTkAgg(figure, master=self.chart_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)