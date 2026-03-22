from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str
    remember_me: bool = False