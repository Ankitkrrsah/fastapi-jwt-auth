from pydantic import BaseModel

class UserResponse(BaseModel):
    name: str
    email: str

class UserInput(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str
