import threading
import time
from datetime import datetime
from typing import Callable, Optional

import psutil

from smart_device_addiction_manager.services.alert_service import AlertService


class UsageMonitor:
    def __init__(self, db_manager):
        self.db = db_manager
        self.monitoring_active = False
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self.current_app_name = "Unknown"
        self._blink_callback: Optional[Callable[[bool], None]] = None
        self._indicator_state = True
        self._session_start = datetime.now()
        self._last_alert_at_limit = None

    def set_blink_callback(self, callback: Callable[[bool], None]):
        self._blink_callback = callback

    def start_monitoring(self):
        if self.monitoring_active:
            return
        self.monitoring_active = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()

    def stop_monitoring(self):
        self.monitoring_active = False
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1)

    def _monitor_loop(self):
        while not self._stop_event.is_set():
            self.current_app_name = self._detect_active_app()
            self._update_indicator()
            self._check_screen_time_limit()
            time.sleep(1)

    def _update_indicator(self):
        if not self.monitoring_active:
            return
        self._indicator_state = not self._indicator_state
        if self._blink_callback:
            self._blink_callback(self._indicator_state)

    def _detect_active_app(self) -> str:
        candidates = []
        for proc in psutil.process_iter(attrs=["name", "cpu_percent"]):
            try:
                name = proc.info.get("name") or ""
                cpu = proc.info.get("cpu_percent") or 0
                if name:
                    candidates.append((cpu, name))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        if not candidates:
            return "Unknown"
        candidates.sort(reverse=True)
        return candidates[0][1]

    def _check_screen_time_limit(self):
        settings = self.db.get_settings()
        # Bug fix: strictly use exact value entered by user (minutes, no multipliers).
        screen_limit_minutes = int(settings.get("screen_limit", 180))
        today = datetime.now().strftime("%Y-%m-%d")
        elapsed_minutes = self.db.get_today_total_minutes(today)
        if elapsed_minutes >= screen_limit_minutes and self._last_alert_at_limit != today:
            if int(settings.get("notifications", 1)) == 1:
                AlertService.send(
                    "Screen Limit Reached",
                    f"Daily screen limit of {screen_limit_minutes} minute(s) reached.",
                )
            self._last_alert_at_limit = today

    def log_manual_session(self, minutes: int):
        now = datetime.now()
        start = now.strftime("%H:%M:%S")
        end = now.strftime("%H:%M:%S")
        date = now.strftime("%Y-%m-%d")
        self.db.insert_usage_log(self.current_app_name, start, end, minutes, date)
