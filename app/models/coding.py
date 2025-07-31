from pydantic import BaseModel


class Coding(BaseModel):
    """
    A model class representing a coding field in an Observation resource.
    """

    system: str
    code: str
    display: str
