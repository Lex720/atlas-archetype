from src.application.commons.date_format import datetime_to_isoformat


def clean_data_types(data: dict) -> dict:
    """Method used to clean data into more native types.

    Args:
        data (:obj:`dict`): Information from the instance model.

    Returns:
        Cleaned data in dict form.
    """
    if data.get("uuid"):
        data["uuid"] = str(data["uuid"])
    if data.get("created_at"):
        data["created_at"] = datetime_to_isoformat(data["created_at"])
    if data.get("updated_at"):
        data["updated_at"] = datetime_to_isoformat(data["updated_at"])
    return data
