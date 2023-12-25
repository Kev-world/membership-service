from typing import List
from pydantic import BaseModel, Field
from datetime import datetime

class CreateClass(BaseModel):
    title: str = Field(min_length=5, max_length=50)
    description: str = Field(min_length=5, max_length=20)
    instructor_id: str = Field(min_length=36, max_length=36)
    max_capacity: int = Field(min=1, max=6)
    participants: List[str]

class RegisterInstructor(BaseModel):
    firstName: str = Field(min_length=3, max_length=20)
    lastName: str = Field(min_length=3, max_length=20)
    email: str = Field(min_length=10, max_length=50)

class CreateEvent(BaseModel):
    title: str = Field(min_length=5, max_length=50)
    description: str = Field(min_length=5, max_length=20)
    host_date: datetime = None