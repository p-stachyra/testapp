from pydantic import BaseModel


# Pydantic model for user registration
class UserRegistration(BaseModel):
    username: str
    password: str