import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


class DatabaseManager:
    def __init__(self, db_path: Optional[str] = None):
        default_path = Path(__file__).resolve().parent / "smart_device_manager.db"
        self.db_path = db_path or str(default_path)
        self._init_db()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS usage_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    app_name TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    duration INTEGER NOT NULL,
                    date TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    notifications INTEGER DEFAULT 1,
                    screen_limit INTEGER DEFAULT 180,
                    break_reminder INTEGER DEFAULT 30,
                    focus_duration INTEGER DEFAULT 60,
                    quiet_hours TEXT DEFAULT '22:00-07:00'
                )
                """
            )
            conn.execute(
                """
                INSERT OR IGNORE INTO settings (
                    id, notifications, screen_limit, break_reminder, focus_duration, quiet_hours
                ) VALUES (1, 1, 180, 30, 60, '22:00-07:00')
                """
            )

    def insert_usage_log(self, app_name: str, start_time: str, end_time: str, duration: int, date: str):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO usage_logs (app_name, start_time, end_time, duration, date)
                VALUES (?, ?, ?, ?, ?)
                """,
                (app_name, start_time, end_time, duration, date),
            )

    def get_usage_logs(self, limit: int = 500) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT app_name, start_time, end_time, duration, date FROM usage_logs ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [dict(row) for row in rows]

    def get_today_total_minutes(self, date_value: str) -> int:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COALESCE(SUM(duration), 0) as total FROM usage_logs WHERE date = ?",
                (date_value,),
            ).fetchone()
            return int(row["total"] if row else 0)

    def get_settings(self) -> Dict[str, Any]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM settings WHERE id = 1").fetchone()
            return dict(row) if row else {}

    def update_settings(self, settings: Dict[str, Any]):
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE settings
                SET notifications = ?, screen_limit = ?, break_reminder = ?, focus_duration = ?, quiet_hours = ?
                WHERE id = 1
                """,
                (
                    settings["notifications"],
                    settings["screen_limit"],
                    settings["break_reminder"],
                    settings["focus_duration"],
                    settings["quiet_hours"],
                ),
            )
