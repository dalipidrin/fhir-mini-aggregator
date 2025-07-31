from pydantic import BaseModel


class ValueQuantity(BaseModel):
    value: float
    unit: str
