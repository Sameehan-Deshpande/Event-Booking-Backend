from fastapi import HTTPException,APIRouter
from sqlalchemy.engine import CursorResult
from seatapi.database import SessionDep
from sqlalchemy import select,update
from sqlalchemy.orm import selectinload
from seatapi.models import Tickets,Members,Events
from seatapi.schema import BookingCreate,BookingRead
from seatapi.dependencies import CurrentMember,AdminMember

router=APIRouter(prefix="/bookings",tags=["bookings"])

@router.post("/",response_model=BookingRead)
def make_booking(session:SessionDep,ticket_in:BookingCreate,current_member:CurrentMember):
    if ticket_in.customer_id!=current_member.id:
        raise HTTPException(status_code=401,detail="Unauthorized access")

    member=current_member
    if not member:
        raise HTTPException(status_code=400,detail="Member not found")
    event=session.get(Events,ticket_in.event_id)
    if not event:
        raise HTTPException(status_code=400,detail="Event not found")
    stmt=update(Events).where(Events.id==ticket_in.event_id,Events.available_seats>0).values(available_seats=Events.available_seats-1).returning(Events.id)
    result=session.scalar(stmt)
    if not result:
        raise HTTPException(status_code=409,detail="Event already sold out")
    
    new_ticket=Tickets(
        attendee_name=member.attendee_name,
        event_id=event.id,
        customer_id=member.id,
    )
    
    session.add(new_ticket)
    session.commit()
    session.refresh(new_ticket)
    return new_ticket

@router.get("/",response_model=list[BookingRead])
def get_booking(member:CurrentMember,session:SessionDep):
    
    ticket=session.scalars(select(Tickets).where(Tickets.customer_id==member.id)).all()
    if not ticket:
        raise HTTPException(status_code=400,detail="No ticket found")
    return ticket

@router.delete("/",response_model=BookingRead)
def cancel_booking(session:SessionDep,member:CurrentMember):
    ticket=session.scalar(select(Tickets).where(Tickets.customer_id==member.id,Tickets.cancelled==False))
    if not ticket:
        raise HTTPException(status_code=404,detail="Ticket not found")
    stmt1=update(Tickets).where(Tickets.id==ticket.id,Tickets.cancelled==False).values(cancelled=True).returning(Tickets.event_id)
    result1=session.scalar(stmt1)
    if not result1:
        raise HTTPException(status_code=409,detail="Cancellation unsuccesfull")
    stmt=update(Events).where(Events.id==result1).values(available_seats=Events.available_seats+1).returning(Events.id)
    result=session.scalar(stmt)
    if not result:
        session.rollback()
        raise HTTPException(status_code=409,detail="Cancellation unsuccesfull")
    session.commit()
    return ticket

