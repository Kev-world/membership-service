from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from annotated_types import Annotated
from databases.sqlDB import SessionLocal
from models.classModel import Rooms, Instructors, Events
from dtos.classEventDto import CreateClass, RegisterInstructor

router = APIRouter(
    prefix='/classEvent',
    tags=['classEvent']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/')
async def get_all_rooms(db: db_dependency):
    return db.query(Rooms).all()

@router.get('/events')
async def get_all_rooms_events(db: db_dependency):
    return db.query(Rooms, Events).join(Events, Rooms.id == Events.class_id).all()

@router.get('/instructors')
async def get_all_instructors(db: db_dependency):
    return db.query(Instructors).all()

@router.post('/instructor')
async def register_instructor(db: db_dependency, dto: RegisterInstructor):
    instructor = db.query(Instructors).filter(Instructors.email == dto.email).first()
    if instructor is not None:
        raise HTTPException(status_code=400, detail='Email Already Taken')
    instructor = Instructors(**dto.model_dump())
    db.add(instructor)
    db.commit()

@router.post('/class')
async def create_class(db: db_dependency, dto: CreateClass):
    instructorExist = db.query(Instructors).filter(Instructors.id == dto.instructor_id).first()
    if instructorExist is None:
        raise HTTPException(status_code=404, detail='Instructor does not exist')
    classModel = Rooms(**dto.model_dump())
    db.add(classModel)
    db.commit()

