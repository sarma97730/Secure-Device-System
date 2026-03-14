import customtkinter as ctk


class LimitsPage(ctk.CTkFrame):
    def __init__(self, master, db, monitor):
        super().__init__(master)
        self.db = db
        self.monitor = monitor

        ctk.CTkLabel(self, text="Daily Screen Limit (minutes)", font=ctk.CTkFont(size=15)).pack(anchor="w", padx=14, pady=(20, 6))
        self.limit_slider = ctk.CTkSlider(self, from_=1, to=720, number_of_steps=719, command=self._on_limit_change)
        self.limit_slider.pack(fill="x", padx=14)
        self.limit_value = ctk.CTkLabel(self, text="180")
        self.limit_value.pack(anchor="w", padx=14, pady=(6, 14))

        ctk.CTkLabel(self, text="Break Reminder (minutes)", font=ctk.CTkFont(size=15)).pack(anchor="w", padx=14, pady=(8, 6))
        self.break_slider = ctk.CTkSlider(self, from_=5, to=180, number_of_steps=175, command=self._on_break_change)
        self.break_slider.pack(fill="x", padx=14)
        self.break_value = ctk.CTkLabel(self, text="30")
        self.break_value.pack(anchor="w", padx=14, pady=(6, 14))

        self.save_btn = ctk.CTkButton(self, text="Save Limits", command=self.save)
        self.save_btn.pack(anchor="w", padx=14, pady=8)
        self.status = ctk.CTkLabel(self, text="")
        self.status.pack(anchor="w", padx=14)

        self._load()

    def _load(self):
        settings = self.db.get_settings()
        limit = int(settings.get("screen_limit", 180))
        reminder = int(settings.get("break_reminder", 30))
        self.limit_slider.set(limit)
        self.break_slider.set(reminder)
        self.limit_value.configure(text=str(limit))
        self.break_value.configure(text=str(reminder))

    def _on_limit_change(self, value):
        self.limit_value.configure(text=str(int(value)))

    def _on_break_change(self, value):
        self.break_value.configure(text=str(int(value)))

    def save(self):
        settings = self.db.get_settings()
        settings["screen_limit"] = int(float(self.limit_slider.get()))
        settings["break_reminder"] = int(float(self.break_slider.get()))
        self.db.update_settings(settings)
        self.status.configure(text="Limits saved.", text_color="#22c55e")
