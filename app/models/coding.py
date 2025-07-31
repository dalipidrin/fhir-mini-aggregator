from pydantic import BaseModel


class Coding(BaseModel):
    system: str
    code: str
    display: str
