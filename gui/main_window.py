import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from gui.dashboard import Dashboard
from gui.task_management import TaskManagement
from gui.report_generation import ReportGeneration
from gui.machine_management import MachineManagement
from gui.maintenance_history import MaintenanceHistory


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.languages = {"English": "en", 
                          "Türkçe": "tr"}
        self.current_language = "en"  

        self.translations = {
            "en": {
                "title": "Maintenance Scheduling System",
                "btn_manage_machines": "Manage Machines",
                "btn_manage_tasks": "Manage Tasks",
                "btn_view_history": "View Maintenance History",
                "btn_generate_reports": "Generate Reports",
                "btn_dashboard": "Dashboard",
                "language_label": "Select Language:"
            },
            "tr": {
                "title": "Bakım Planlama Sistemi",
                "btn_manage_machines": "Makineleri Yönet",
                "btn_manage_tasks": "Bakım Görevlerini Yönet",
                "btn_view_history": "Bakım Geçmişini Görüntüle",
                "btn_generate_reports": "Rapor Oluştur",
                "btn_dashboard": "Dashboard",
                "language_label": "Dil Seçiniz:"
            }
        }

        self.title_label = tk.Label(root, text=self.translations["en"]["title"], font=("Arial", 24))
        self.title_label.pack(pady=10)

        image = Image.open("assets/icon.png")
        self.image = ImageTk.PhotoImage(image)
        img_label = tk.Label(self.root, image=self.image)
        img_label.pack(pady=10)
        
        self.nav_frame = ttk.Frame(root)
        self.nav_frame.pack(pady=20)

        self.btn_machine = ttk.Button(self.nav_frame, text=self.translations["en"]["btn_manage_machines"],
                                      command=self.open_machine_management)
        self.btn_machine.grid(row=0, column=0, padx=10)

        self.btn_tasks = ttk.Button(self.nav_frame, text=self.translations["en"]["btn_manage_tasks"],
                                    command=self.open_task_management)
        self.btn_tasks.grid(row=0, column=1, padx=10)

        self.btn_history = ttk.Button(self.nav_frame, text=self.translations["en"]["btn_view_history"],
                                      command=self.open_maintenance_history)
        self.btn_history.grid(row=0, column=2, padx=10)

        self.btn_reports = ttk.Button(self.nav_frame, text=self.translations["en"]["btn_generate_reports"],
                                      command=self.open_report_generation)
        self.btn_reports.grid(row=1, column=0, padx=10)

        btn_dashboard = ttk.Button(self.nav_frame, text=self.translations["en"]["btn_dashboard"], command=self.open_dashboard)
        btn_dashboard.grid(row=1, column=1, padx=10)

        lang_frame = ttk.Frame(root)
        lang_frame.place(relx=0.95, rely=0.95, anchor="se")  

        self.lang_label = ttk.Label(lang_frame, text=self.translations["en"]["language_label"])
        self.lang_label.grid(row=0, column=0, padx=5)

        self.lang_combo = ttk.Combobox(lang_frame, values=list(self.languages.keys()), state="readonly")
        self.lang_combo.grid(row=0, column=1, padx=5)
        self.lang_combo.current(0) 
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)

    def change_language(self, event):
        selected_lang = self.lang_combo.get()
        self.current_language = self.languages[selected_lang]
        translations = self.translations[self.current_language]
        self.title_label.config(text=translations["title"])
        self.btn_machine.config(text=translations["btn_manage_machines"])
        self.btn_tasks.config(text=translations["btn_manage_tasks"])
        self.btn_history.config(text=translations["btn_view_history"])
        self.btn_reports.config(text=translations["btn_generate_reports"])
        self.lang_label.config(text=translations["language_label"])

    def open_machine_management(self):
        MachineManagement(self.root)

    def open_task_management(self):
        TaskManagement(self.root)

    def open_maintenance_history(self):
        MaintenanceHistory(self.root)

    def open_report_generation(self):
        ReportGeneration(self.root)
    
    def open_dashboard(self):
        Dashboard(self.root)