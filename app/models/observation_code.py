from typing import List

from pydantic import BaseModel

from .coding import Coding


class ObservationCode(BaseModel):
    """
    A model class representing an observation code field in an Observation resource.
    """

    coding: List[Coding]
