
class PredictionService:
    def predict_end_of_day_usage(self, current_minutes: int, hours_elapsed: float) -> int:
        if hours_elapsed <= 0:
            return current_minutes
        rate = current_minutes / hours_elapsed
        return int(rate * 24)
