from typing import Any, List

from pydantic import BaseModel, conlist


class Iris(BaseModel):
    data: List[conlist(float, min_items=4, max_items=4)]


class IrisPredictionResponse(BaseModel):
    prediction: List[int]
    probability: List[Any]
    log_probability: List[Any]
