import customtkinter as ctk

from smart_device_addiction_manager.utils.helpers import validate_required_numeric_fields


class SettingsPage(ctk.CTkFrame):
    def __init__(self, master, db, monitor):
        super().__init__(master)
        self.db = db
        self.monitor = monitor
        self.base_font = ctk.CTkFont(size=16)

        self.notifications = ctk.BooleanVar(value=True)
        self.auto_start = ctk.BooleanVar(value=True)

        self._build_ui()
        self._load()

    def _build_ui(self):
        ctk.CTkLabel(self, text="SETTINGS", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=14, pady=(14, 10))

        ctk.CTkLabel(self, text="GENERAL SETTINGS", font=ctk.CTkFont(size=17, weight="bold")).pack(anchor="w", padx=14, pady=(8, 4))
        ctk.CTkCheckBox(self, text="Enable Notifications", variable=self.notifications, font=self.base_font).pack(anchor="w", padx=20, pady=3)
        ctk.CTkCheckBox(self, text="Start Monitoring Automatically", variable=self.auto_start, font=self.base_font).pack(anchor="w", padx=20, pady=3)

        ctk.CTkLabel(self, text="SCREEN TIME CONTROL", font=ctk.CTkFont(size=17, weight="bold")).pack(anchor="w", padx=14, pady=(12, 4))
        self.screen_limit = self._entry_row("Daily Screen Limit (minutes)")
        self.break_reminder = self._entry_row("Break Reminder (minutes)")

        ctk.CTkLabel(self, text="FOCUS MODE", font=ctk.CTkFont(size=17, weight="bold")).pack(anchor="w", padx=14, pady=(12, 4))
        self.focus_duration = self._entry_row("Focus Duration (minutes)")

        ctk.CTkLabel(self, text="QUIET HOURS", font=ctk.CTkFont(size=17, weight="bold")).pack(anchor="w", padx=14, pady=(12, 4))
        self.quiet_start = self._entry_row("Start (HH:MM)", numeric=False)
        self.quiet_end = self._entry_row("End (HH:MM)", numeric=False)

        ctk.CTkLabel(self, text="HEALTH REMINDERS", font=ctk.CTkFont(size=17, weight="bold")).pack(anchor="w", padx=14, pady=(12, 4))
        self.eye_break = self._entry_row("Eye Break (minutes)")

        ctk.CTkLabel(self, text="MONTH / DATE FILTER", font=ctk.CTkFont(size=17, weight="bold")).pack(anchor="w", padx=14, pady=(12, 4))
        self.month_vars = []
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December",
        ]
        for month in months:
            var = ctk.BooleanVar(value=True)
            self.month_vars.append(var)
            ctk.CTkCheckBox(self, text=month, variable=var, font=self.base_font).pack(anchor="w", padx=20, pady=2)

        self.include_specific_dates = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(self, text="Enable custom date selection", variable=self.include_specific_dates, font=self.base_font).pack(
            anchor="w", padx=20, pady=6
        )

        self.msg = ctk.CTkLabel(self, text="", font=self.base_font)
        self.msg.pack(anchor="w", padx=14, pady=6)

        ctk.CTkButton(self, text="SAVE SETTINGS", command=self.save, font=ctk.CTkFont(size=16, weight="bold")).pack(
            anchor="w", padx=14, pady=(6, 14)
        )

    def _entry_row(self, label, numeric=True):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=3)
        ctk.CTkLabel(frame, text=label, font=self.base_font).pack(side="left")
        entry = ctk.CTkEntry(frame, width=180, font=self.base_font)
        entry.pack(side="right")
        entry.numeric = numeric
        return entry

    def _load(self):
        settings = self.db.get_settings()
        self.notifications.set(bool(settings.get("notifications", 1)))
        self.screen_limit.insert(0, str(settings.get("screen_limit", 180)))
        self.break_reminder.insert(0, str(settings.get("break_reminder", 30)))
        self.focus_duration.insert(0, str(settings.get("focus_duration", 60)))
        quiet = str(settings.get("quiet_hours", "22:00-07:00")).split("-")
        self.quiet_start.insert(0, quiet[0])
        self.quiet_end.insert(0, quiet[1] if len(quiet) > 1 else "07:00")
        self.eye_break.insert(0, "20")

    def save(self):
        numeric_values = {
            "Daily Screen Limit": self.screen_limit.get(),
            "Break Reminder": self.break_reminder.get(),
            "Focus Duration": self.focus_duration.get(),
        }
        errors = validate_required_numeric_fields(numeric_values)
        if errors:
            self.msg.configure(text="Please enter a valid value", text_color="#ef4444")
            return

        new_settings = self.db.get_settings()
        new_settings["notifications"] = 1 if self.notifications.get() else 0
        new_settings["screen_limit"] = int(self.screen_limit.get())
        new_settings["break_reminder"] = int(self.break_reminder.get())
        new_settings["focus_duration"] = int(self.focus_duration.get())
        new_settings["quiet_hours"] = f"{self.quiet_start.get()}-{self.quiet_end.get()}"

        self.db.update_settings(new_settings)
        self.msg.configure(text="Settings saved successfully", text_color="#22c55e")
