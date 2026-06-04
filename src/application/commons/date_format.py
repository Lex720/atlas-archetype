from datetime import datetime


def datetime_to_isoformat(datetime_data: datetime) -> str:
    """Return a string representing the date and time in ISO 8601 format."""
    return datetime_data.isoformat()
