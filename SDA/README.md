# Smart Device Addiction Manager

A Python desktop application that helps users monitor screen time, configure limits, and review usage behavior.

## Features

- Dark-themed CustomTkinter desktop UI with sidebar navigation.
- Dashboard cards for today's usage, active application, and usage progress.
- Blinking monitoring status indicator updated every second while monitoring is active.
- Usage history table with scroll support.
- Limits and Settings pages with validation for required numeric fields.
- SQLite database for usage logs and persistent settings.
- Background monitoring service using `threading` and `psutil`.
- Desktop alerts via `plyer` when daily screen limit is reached.

## Project Structure

```text
SDA/
├── main.py
├── README.md
├── requirements.txt
└── smart_device_addiction_manager/
    ├── main.py
    ├── assets/
    ├── database/
    │   └── database_manager.py
    ├── gui/
    │   ├── dashboard.py
    │   ├── usage_page.py
    │   ├── limits_page.py
    │   ├── reports_page.py
    │   ├── settings_page.py
    │   └── components.py
    ├── models/
    │   └── data_models.py
    ├── services/
    │   ├── usage_monitor.py
    │   ├── risk_analyzer.py
    │   ├── alert_service.py
    │   ├── prediction_service.py
    │   └── productivity_service.py
    └── utils/
        └── helpers.py
```

## Database Schema

### `usage_logs`
- `app_name`
- `start_time`
- `end_time`
- `duration`
- `date`

### `settings`
- `notifications`
- `screen_limit`
- `break_reminder`
- `focus_duration`
- `quiet_hours`

## Run Instructions

1. Move into the app folder:
   ```bash
   cd SDA
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   python main.py
   ```

## Notes

- The screen time limit logic uses the exact minute value entered by the user.
- Empty required numeric settings are blocked and show: `Please enter a valid value`.
