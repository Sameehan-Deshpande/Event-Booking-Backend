from seatapi.database import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import ForeignKey
from datetime import datetime,timezone

class Events(Base):
    __tablename__="events"

    id:Mapped[int]=mapped_column(primary_key=True)
    title:Mapped[str]
    venue:Mapped[str]
    category:Mapped[str]
    total_seats:Mapped[int]
    available_seats:Mapped[int]
    tickets:Mapped[list["Tickets"]]=relationship(back_populates="event")

class Tickets(Base):
    __tablename__="tickets"
    
    id:Mapped[int]=mapped_column(primary_key=True)
    attendee_name:Mapped[str]
    event_id:Mapped[int]=mapped_column(ForeignKey("events.id"))
    customer_id:Mapped[int]=mapped_column(ForeignKey("members.id"))
    booked_at:Mapped[datetime]=mapped_column(default=lambda:datetime.now(timezone.utc))
    cancelled:Mapped[bool]=mapped_column(default=False)
    event:Mapped["Events"]=relationship(back_populates="tickets")
    

class Members(Base):
    __tablename__="members"
    id:Mapped[int]=mapped_column(primary_key=True)
    attendee_name:Mapped[str]
    phone_number:Mapped[int]=mapped_column(unique=True)





