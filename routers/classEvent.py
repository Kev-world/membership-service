from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from annotated_types import Annotated
from databases.sqlDB import SessionLocal
from models.classModel import Rooms, Instructors, Events
from dtos.classEventDto import CreateClass, RegisterInstructor, CreateEvent

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
    # Query all rooms and their corresponding events
    results = db.query(Rooms, Events).outerjoin(Events, Rooms.id == Events.class_id).all()

    # Create a dictionary to hold the room data and associated events
    rooms_with_events = {}

    # Process the results and organize them into the rooms_with_events dictionary
    for room_event_pair in results:
        room, event = room_event_pair

        # Ensure that room is an instance of the Rooms model
        if not isinstance(room, Rooms):
            continue  # or handle error appropriately

        # Initialize the room entry in the dictionary if it doesn't exist
        if room.id not in rooms_with_events:
            rooms_with_events[room.id] = {
                'id': room.id,
                'title': room.title,
                'description': room.description,
                'max_capacity': room.max_capacity,
                'instructor_id': room.instructor_id,
                'events': []
            }

        # If there is an event and it's an instance of the Events model, append it to the room's list of events
        if event and isinstance(event, Events):
            rooms_with_events[room.id]['events'].append({
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'host_date': event.host_date.isoformat()  # Convert date to string
            })

    # Convert the rooms_with_events dictionary to a list of values
    rooms_events_list = list(rooms_with_events.values())

    return rooms_events_list

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

@router.post('/class/{id}/event')
async def create_event(db: db_dependency, dto: CreateEvent, id: str = Path(min_length=36, max_length=36)):
    classModel = db.query(Rooms).filter(Rooms.id == id).first()
    if classModel is None:
        raise HTTPException(status_code=404, detail='Class does not exist')
    eventModel = Events(**dto.model_dump(), class_id = id)
    db.add(eventModel)
    db.commit()
