from datetime import datetime

import customtkinter as ctk

from smart_device_addiction_manager.gui.components import InfoCard
from smart_device_addiction_manager.utils.helpers import minutes_to_hm


class DashboardPage(ctk.CTkFrame):
    def __init__(self, master, monitor, db):
        super().__init__(master)
        self.monitor = monitor
        self.db = db
        self.blink_on = True

        self.grid_columnconfigure((0, 1), weight=1)

        self.usage_card = InfoCard(self, "Today's Usage", "0h 0m")
        self.usage_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.app_card = InfoCard(self, "Current App", "Unknown")
        self.app_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.progress_frame = ctk.CTkFrame(self)
        self.progress_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(self.progress_frame, text="Daily Usage Progress", font=ctk.CTkFont(size=15, weight="bold")).pack(
            anchor="w", padx=12, pady=(10, 4)
        )
        self.progress = ctk.CTkProgressBar(self.progress_frame)
        self.progress.pack(fill="x", padx=12, pady=8)
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="0% of daily limit")
        self.progress_label.pack(anchor="w", padx=12, pady=(0, 10))

        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.status_text = ctk.CTkLabel(self.status_frame, text="Monitoring Status:", font=ctk.CTkFont(size=16, weight="bold"))
        self.status_text.pack(side="left", padx=(12, 6), pady=12)
        self.indicator = ctk.CTkLabel(self.status_frame, text="●", font=ctk.CTkFont(size=18, weight="bold"), text_color="#22c55e")
        self.indicator.pack(side="left", pady=12)

        self.monitor.set_blink_callback(self._on_blink)
        self.after(1000, self._periodic_refresh)

    def _on_blink(self, is_on: bool):
        self.blink_on = is_on
        color = "#22c55e" if is_on else "#1f2937"
        self.indicator.configure(text_color=color)

    def _periodic_refresh(self):
        self.refresh()
        self.after(1000, self._periodic_refresh)

    def refresh(self):
        today = datetime.now().strftime("%Y-%m-%d")
        total = self.db.get_today_total_minutes(today)
        settings = self.db.get_settings()
        limit = max(1, int(settings.get("screen_limit", 180)))
        ratio = min(1.0, total / limit)

        self.usage_card.set_value(minutes_to_hm(total))
        self.app_card.set_value(self.monitor.current_app_name)
        self.progress.set(ratio)
        self.progress_label.configure(text=f"{int(ratio * 100)}% of daily limit")
