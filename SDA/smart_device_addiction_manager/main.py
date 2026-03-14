import customtkinter as ctk

from smart_device_addiction_manager.database.database_manager import DatabaseManager
from smart_device_addiction_manager.gui.dashboard import DashboardPage
from smart_device_addiction_manager.gui.limits_page import LimitsPage
from smart_device_addiction_manager.gui.reports_page import ReportsPage
from smart_device_addiction_manager.gui.settings_page import SettingsPage
from smart_device_addiction_manager.gui.usage_page import UsagePage
from smart_device_addiction_manager.services.usage_monitor import UsageMonitor


class SmartDeviceAddictionManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Smart Device Addiction Manager")
        self.geometry("1200x760")
        self.minsize(1000, 680)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.db = DatabaseManager()
        self.monitor = UsageMonitor(self.db)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_header()
        self._create_sidebar()
        self._create_content()

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.show_page("Dashboard")
        self.monitor.start_monitoring()

    def _create_header(self):
        self.header = ctk.CTkFrame(self, corner_radius=0)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.header.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header,
            text="Smart Device Addiction Manager",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        self.title_label.grid(row=0, column=0, padx=16, pady=12, sticky="w")

        self.status_label = ctk.CTkLabel(
            self.header,
            text="Monitoring: ●",
            text_color="#22c55e",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.status_label.grid(row=0, column=1, padx=16, pady=12, sticky="e")

    def _create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220)
        self.sidebar.grid(row=1, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)

        pages = ["Dashboard", "Usage", "Limits", "Reports", "Settings"]
        self.nav_buttons = {}
        for idx, page in enumerate(pages):
            btn = ctk.CTkButton(
                self.sidebar,
                text=page,
                anchor="w",
                command=lambda p=page: self.show_page(p),
            )
            btn.grid(row=idx, column=0, padx=14, pady=(14 if idx == 0 else 8, 0), sticky="ew")
            self.nav_buttons[page] = btn

        self.sidebar.grid_columnconfigure(0, weight=1)

    def _create_content(self):
        self.content = ctk.CTkFrame(self)
        self.content.grid(row=1, column=1, sticky="nsew", padx=12, pady=12)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.pages = {
            "Dashboard": DashboardPage(self.content, self.monitor, self.db),
            "Usage": UsagePage(self.content, self.db),
            "Limits": LimitsPage(self.content, self.db, self.monitor),
            "Reports": ReportsPage(self.content, self.db),
            "Settings": SettingsPage(self.content, self.db, self.monitor),
        }

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_name: str):
        page = self.pages[page_name]
        page.tkraise()

        if page_name == "Dashboard":
            page.refresh()
            self._blink_header_indicator()
        elif page_name == "Usage":
            page.refresh()
        elif page_name == "Reports":
            page.refresh()

    def _blink_header_indicator(self):
        active = self.monitor.monitoring_active
        color = "#22c55e" if active else "#ef4444"
        text = "Monitoring: ●" if active else "Monitoring: ○"
        self.status_label.configure(text=text, text_color=color)

    def on_close(self):
        self.monitor.stop_monitoring()
        self.destroy()


def run():
    app = SmartDeviceAddictionManagerApp()
    app.mainloop()
