from databases.sqlDB import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship
import uuid

class Instructors(Base):
    __tablename__ = 'instructors'
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    firstName = Column(String(20))
    lastName = Column(String(20))
    email = Column(String(50), unique=True, nullable=False)
    

class Rooms(Base):
    __tablename__ = 'rooms'
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(50))
    description = Column(String(20))
    instructor_id = Column(String(36), ForeignKey('instructors.id'))
    max_capacity = Column(Integer)
    participants = Column(JSON)

class Events(Base):
    __tablename__ = 'events'
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(50))
    description = Column(String(100))
    host_date = Column(Date)
    class_id = Column(String(36), ForeignKey('rooms.id'))