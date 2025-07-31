from typing import List

from pydantic import BaseModel

from coding import Coding


class Code(BaseModel):
    coding: List[Coding]
