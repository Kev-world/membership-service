from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from databases.sqlDB import SessionLocal
from models.membershipModel import Members
from annotated_types import Annotated
from dtos.memberDto import RegisterMemberDto

router = APIRouter(
    prefix='/memberships',
    tags=['memberships']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/')
async def get_all(db: db_dependency):
    members = db.query(Members).all()
    return members

@router.get('/{id}')
async def get_one(db: db_dependency, id: str = Path(min_length=36, max_length=36)):
    member = db.query(Members).filter(Members.id == id).first()
    if member is None:
        raise HTTPException(status_code=404, detail='Member Not Found')
    return member

@router.post('/')
async def create(db: db_dependency, dto: RegisterMemberDto):
    member = db.query(Members).filter(Members.email == dto.email).first()
    if member is not None:
        raise HTTPException(status_code=400, detail='Member already exists')
    member = Members(**dto.model_dump())
    db.add(member)
    db.commit()
