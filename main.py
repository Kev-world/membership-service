from fastapi import FastAPI
from databases.sqlDB import engine
from models import bookingModel, membershipModel
from routers import membership

app = FastAPI()

membershipModel.Base.metadata.create_all(bind=engine)
bookingModel.Base.metadata.create_all(bind=engine)

app.include_router(membership.router)