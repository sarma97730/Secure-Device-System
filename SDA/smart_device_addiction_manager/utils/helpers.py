from typing import Dict, List


def validate_required_numeric_fields(values: Dict[str, str]) -> List[str]:
    errors = []
    for field_name, value in values.items():
        if str(value).strip() == "":
            errors.append(f"{field_name}: Please enter a valid value")
            continue
        try:
            int(value)
        except ValueError:
            errors.append(f"{field_name}: Please enter a valid value")
    return errors


def minutes_to_hm(total_minutes: int) -> str:
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours}h {minutes}m"
