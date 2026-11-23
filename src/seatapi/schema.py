from pydantic import BaseModel,Field,ConfigDict
from enum import Enum
from datetime import datetime


class Category(str,Enum):

    COMEDY="comedy"
    MUSIC="music"
    WORKSHOP="workshop"
    SPORTS="sports"

class MemberCreate(BaseModel):
    attendee_name:str=Field(min_length=2)
    phone_number:int=Field(ge=1_000_000_000, le=9_999_999_999)
    
class MemberRead(MemberCreate):
    id:int
    model_config=ConfigDict(from_attributes=True)
class EventCreate(BaseModel):
    title:str=Field(min_length=2)
    venue:str=Field(min_length=2)
    category:Category
    total_seats:int=Field(ge=0)


class EventUpdate(BaseModel):
    title:str|None=None
    venue:str|None=None
    total_seats:int|None=None

class BookingCreate(BaseModel):
    event_id:int
    customer_id:int
class BookingRead(BookingCreate):
    attendee_name:str
    booked_at:datetime
    cancelled:bool|None=None
    model_config=ConfigDict(from_attributes=True)

class MemberUpdate(BaseModel):
    attendee_name:str|None=None
    phone_number:int|None=None
    
    
class EventRead(EventCreate):
    id:int
    available_seats:int
    tickets:list[BookingRead]
    model_config=ConfigDict(from_attributes=True)
