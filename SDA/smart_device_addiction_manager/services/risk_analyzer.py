
class RiskAnalyzer:
    def analyze(self, total_minutes: int, limit_minutes: int) -> str:
        if limit_minutes <= 0:
            return "unknown"
        ratio = total_minutes / limit_minutes
        if ratio < 0.5:
            return "low"
        if ratio < 0.9:
            return "moderate"
        if ratio <= 1.0:
            return "high"
        return "critical"
