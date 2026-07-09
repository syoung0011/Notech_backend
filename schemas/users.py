from pydantic import BaseModel, Field


class UserRegRequest(BaseModel):
    username:str=Field(...,min_length=1, max_length=8)
    password:str=Field(...,min_length=3, max_length=32)