from pydantic import BaseModel, Field, ConfigDict


class UserRegRequest(BaseModel):
    username:str=Field(...,min_length=1, max_length=8)
    password:str=Field(...,min_length=3, max_length=32)

class UserLoginRequest(BaseModel):
    username:str=Field(...,min_length=1, max_length=8)
    password:str=Field(...,min_length=3, max_length=32)

class UserProfileResponse(BaseModel):
    id:int
    username:str

    model_config = ConfigDict(
        from_attributes=True,
    )
