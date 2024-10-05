from pydantic import BaseModel, constr


class User(BaseModel):
    username: str = constr(min_length=3, max_length=30)
    password: str = constr(min_length=8, max_length=30)

