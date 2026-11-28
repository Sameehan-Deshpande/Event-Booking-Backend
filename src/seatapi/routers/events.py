from seatapi.database import SessionDep,Session
from fastapi import APIRouter,HTTPException
from sqlalchemy import select,func
from sqlalchemy.orm import selectinload
from seatapi.schema import EventCreate,EventRead,EventUpdate
from seatapi.models import Events,Tickets
from seatapi.dependencies import CurrentMember,AdminMember

router=APIRouter(prefix="/events",tags=["events"])

@router.get("/",response_model=list[EventRead])
def get_events(session:SessionDep,member:CurrentMember,event_name:str|None=None):
    event=select(Events)
    if event_name:
        event=select(Events).where(Events.title==event_name)
    return session.scalars(event).all()
@router.get("/{event_id}",response_model=EventRead)
def get_spec_event(session:SessionDep,event_id:int):
    event=session.scalar(select(Events).where(Events.id==event_id))
    if not event:
        raise HTTPException(status_code=404,detail="Event not found")
    return event    

@router.post("/",response_model=EventRead)
def create_event(session:SessionDep,event_in:EventCreate,member:AdminMember):

    new_event=Events(
        title=event_in.title,
        creator_id=member.id,
        venue=event_in.venue,
        total_seats=event_in.total_seats,
        category=event_in.category.value,
        available_seats=event_in.total_seats,
    )
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return new_event
@router.patch("/{event_id}",response_model=EventRead)
def event_update(session:SessionDep,event_data:EventUpdate,event_id:int,member:AdminMember):
    
    event=session.scalar(select(Events).where(Events.creator_id==member.id,Events.id==event_id))
    if not event:
        raise HTTPException(status_code=404,detail="Event not found")
    update_dict=event_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(event, key, value)

    session.commit()
    session.refresh(event)
    return event
@router.delete("/{event_id}",response_model=EventRead)
def delete_event(session:SessionDep,event_id:int,member:AdminMember):
    
    event=session.scalar(select(Events).where(Events.creator_id==member.id,Events.id==event_id))
    if not event:
        raise HTTPException(status_code=404,detail="Event not found")
    count=(
    session.scalar(
        select(func.count(Tickets.id)).where(
            Tickets.event_id == event_id,
            Tickets.cancelled==False,
        )
    ) or 0)
    if count!=0:
        raise HTTPException(status_code=409,detail="Can not delete live event")
    session.delete(event)
    session.commit()
    return event



    
