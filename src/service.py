from datetime import datetime

from src.db import BaseCRUD
from src.models import Record


def validate_obj(obj):
    try:
        if len(obj['name']) >= 50:
            return False
        datetime.strptime(obj['date'], "%Y-%m-%d_%H:%M")
        return True
    except Exception as e:
        print(e)
        return False


class RecordCRUD(BaseCRUD):
    model = Record
