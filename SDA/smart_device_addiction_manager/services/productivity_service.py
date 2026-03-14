
class ProductivityService:
    def focus_score(self, total_minutes: int, focus_duration: int) -> float:
        if focus_duration <= 0:
            return 0.0
        return max(0.0, 100 - (total_minutes / focus_duration) * 10)
