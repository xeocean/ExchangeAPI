from pydantic import BaseModel, Field


class Currency(BaseModel):
    value_1: str = Field(min_length=3, max_length=3)
    value_2: str = Field(min_length=3, max_length=3)
    quantity: float = 1
