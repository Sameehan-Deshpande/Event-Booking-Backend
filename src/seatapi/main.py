from fastapi import FastAPI
from pathlib import Path
from contextlib import asynccontextmanager
from seatapi.database import get_db_and_tables
from seatapi.routers import events,members,bookings,auth
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(app:FastAPI):
    get_db_and_tables()
    yield
app=FastAPI(title="bullshit", lifespan=lifespan)

app.include_router(events.router)
app.include_router(members.router)
app.include_router(bookings.router)
app.include_router(auth.router)

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")





