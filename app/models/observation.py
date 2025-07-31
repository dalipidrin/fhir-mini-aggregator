from datetime import datetime

from pydantic import BaseModel

from code import Code
from subject import Subject
from value_quantity import ValueQuantity


class Observation(BaseModel):
    resourceType: str
    id: str
    status: str
    code: Code
    subject: Subject
    effectiveDateTime: datetime
    valueQuantity: ValueQuantity
