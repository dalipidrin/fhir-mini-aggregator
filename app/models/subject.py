from pydantic import BaseModel


class Subject(BaseModel):
    reference: str
