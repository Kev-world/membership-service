from fastapi import FastAPI
from databases.sqlDB import engine
from models import classModel, membershipModel
from routers import membership, classEvent

app = FastAPI()

membershipModel.Base.metadata.create_all(bind=engine)
classModel.Base.metadata.create_all(bind=engine)

app.include_router(membership.router)
app.include_router(classEvent.router)