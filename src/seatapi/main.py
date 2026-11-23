from fastapi import FastAPI
from contextlib import asynccontextmanager
from seatapi.database import get_db_and_tables
from seatapi.routers import events,members,bookings

@asynccontextmanager
async def lifespan(app:FastAPI):
    get_db_and_tables()
    yield
app=FastAPI(title="bullshit", lifespan=lifespan)

app.include_router(events.router)
app.include_router(members.router)
app.include_router(bookings.router)






