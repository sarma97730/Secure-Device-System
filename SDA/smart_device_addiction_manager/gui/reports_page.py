from collections import defaultdict

import customtkinter as ctk


class ReportsPage(ctk.CTkFrame):
    def __init__(self, master, db):
        super().__init__(master)
        self.db = db

        self.daily = ctk.CTkLabel(self, text="Daily usage chart: No data")
        self.daily.pack(anchor="w", padx=14, pady=(16, 8))

        self.weekly = ctk.CTkLabel(self, text="Weekly usage chart: No data")
        self.weekly.pack(anchor="w", padx=14, pady=8)

        self.monthly = ctk.CTkLabel(self, text="Monthly usage chart: No data")
        self.monthly.pack(anchor="w", padx=14, pady=8)

    def refresh(self):
        logs = self.db.get_usage_logs(limit=2000)
        daily_totals = defaultdict(int)
        for row in logs:
            daily_totals[row["date"]] += int(row["duration"])

        if daily_totals:
            ordered = sorted(daily_totals.items())
            last_day = ordered[-1]
            week = ordered[-7:]
            month = ordered[-30:]
            self.daily.configure(text=f"Daily usage chart: {last_day[0]} = {last_day[1]} min")
            self.weekly.configure(text=f"Weekly usage chart: {sum(v for _, v in week)} min total")
            self.monthly.configure(text=f"Monthly usage chart: {sum(v for _, v in month)} min total")
        else:
            self.daily.configure(text="Daily usage chart: No data")
            self.weekly.configure(text="Weekly usage chart: No data")
            self.monthly.configure(text="Monthly usage chart: No data")
