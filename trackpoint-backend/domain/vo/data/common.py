from pydantic import BaseModel


class DescriptionNumber(BaseModel):
    max: int | float
    min: int | float
    avg: int | float
