from pydantic import BaseModel


class RecordDTO(BaseModel):
    name: str
    date: str
