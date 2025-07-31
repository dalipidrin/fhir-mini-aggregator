from datetime import datetime

from pydantic import BaseModel

from .observation_code import ObservationCode
from .subject import Subject
from .value_quantity import ValueQuantity


class Observation(BaseModel):
    """
    A model class representing an Observation resource.
    """

    resourceType: str
    id: str
    status: str
    code: ObservationCode
    subject: Subject
    effectiveDateTime: datetime
    valueQuantity: ValueQuantity
