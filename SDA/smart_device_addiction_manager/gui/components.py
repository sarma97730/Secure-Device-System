import customtkinter as ctk


class InfoCard(ctk.CTkFrame):
    def __init__(self, master, title: str, value: str):
        super().__init__(master)
        self.title_label = ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=14, weight="bold"))
        self.title_label.pack(anchor="w", padx=12, pady=(10, 6))
        self.value_label = ctk.CTkLabel(self, text=value, font=ctk.CTkFont(size=24, weight="bold"))
        self.value_label.pack(anchor="w", padx=12, pady=(0, 12))

    def set_value(self, value: str):
        self.value_label.configure(text=value)
