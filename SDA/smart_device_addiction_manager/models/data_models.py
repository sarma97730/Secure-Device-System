from dataclasses import dataclass


@dataclass
class UsageLog:
    app_name: str
    start_time: str
    end_time: str
    duration: int
    date: str


@dataclass
class Settings:
    notifications: bool
    screen_limit: int
    break_reminder: int
    focus_duration: int
    quiet_hours: str
