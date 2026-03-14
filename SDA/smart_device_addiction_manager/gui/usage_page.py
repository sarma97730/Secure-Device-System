import customtkinter as ctk
from tkinter import ttk


class UsagePage(ctk.CTkFrame):
    def __init__(self, master, db):
        super().__init__(master)
        self.db = db

        columns = ("app_name", "duration", "start_time", "end_time", "date")
        self.table = ttk.Treeview(self, columns=columns, show="headings", height=20)
        self.table.heading("app_name", text="Application Name")
        self.table.heading("duration", text="Usage Duration (min)")
        self.table.heading("start_time", text="Start Time")
        self.table.heading("end_time", text="End Time")
        self.table.heading("date", text="Date")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 10), pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def refresh(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for item in self.db.get_usage_logs():
            self.table.insert(
                "",
                "end",
                values=(
                    item["app_name"],
                    item["duration"],
                    item["start_time"],
                    item["end_time"],
                    item["date"],
                ),
            )
