from pydantic import BaseModel


class Subject(BaseModel):
    """
    A model class representing a subject field in an Observation resource.
    """

    reference: str
