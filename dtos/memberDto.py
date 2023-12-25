from pydantic import BaseModel, Field
from datetime import datetime

class RegisterMemberDto(BaseModel):
    firstName: str = Field(min_length=3)
    lastName: str = Field(min_length=3)
    email: str = Field(min_length=10)
    address: str
    dob: datetime = None
    date_created: datetime = None
