from plyer import notification


class AlertService:
    @staticmethod
    def send(title: str, message: str):
        try:
            notification.notify(title=title, message=message, timeout=5)
        except Exception:
            # Keep app stable in environments where desktop notifications are not available.
            pass
