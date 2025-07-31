from typing import List

from pydantic import BaseModel

from .coding import Coding


class ObservationCode(BaseModel):
    coding: List[Coding]
