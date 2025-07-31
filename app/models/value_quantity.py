from pydantic import BaseModel


class ValueQuantity(BaseModel):
    """
    A model class representing a value quantity field in an Observation resource.
    """

    value: float
    unit: str
