from fastapi import HTTPException,APIRouter
from seatapi.database import SessionDep
from seatapi.models import Tickets,Members,Events
from seatapi.schema import BookingCreate,BookingRead

router=APIRouter(prefix="/bookings",tags=["bookings"])

@router.post("/",response_model=BookingRead)
def make_booking(session:SessionDep,event_id:int,member_id:int,ticket_in:BookingCreate):
    member=session.get(Members,member_id)
    if not member:
        raise HTTPException(status_code=400,detail="Member not found")
    event=session.get(Events,event_id)
    if not event:
        raise HTTPException(status_code=400,detail="Event not found")
    if not event.available_seats>0:
        raise HTTPException(status_code=404,detail="No more tickets available")
    new_ticket=Tickets(
        attendee_name=member.attendee_name,
        event_id=event.id,
        customer_id=member.id,
    )
    event.available_seats-=1
    session.add(new_ticket)
    session.commit()
    session.refresh(new_ticket)
    return new_ticket

@router.get("/{booking_id}",response_model=BookingRead)
def get_booking(booking_id:int,session:SessionDep):
    ticket=session.get(Tickets,booking_id)
    if not ticket:
        raise HTTPException(status_code=400,detail="No ticket found")
    return ticket
@router.delete("/{booking_id}",response_model=BookingRead)
def cancel_booking(session:SessionDep,booking_id:int):
    ticket=session.get(Tickets,booking_id)
    if not ticket:
        raise HTTPException(status_code=400,detail="No ticket found")
    ticket.cancelled=True
    session.delete(ticket)
    session.commit()
    return ticket

