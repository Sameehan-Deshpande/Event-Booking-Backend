from seatapi.database import SessionDep,Session
from fastapi import APIRouter,HTTPException
from sqlalchemy import select
from seatapi.schema import EventCreate,EventRead,EventUpdate
from seatapi.models import Events

router=APIRouter(prefix="/events",tags=["events"])

@router.get("/",response_model=list[EventRead])
def get_events(session:SessionDep,event_name:str|None=None):
    events=select(Events)
    if event_name:
        events=events.where(Events.title==event_name)
    session.scalars(events).all()
    return session.scalars(events).all()

@router.post("/create",response_model=EventRead)
def create_event(session:SessionDep,event_in:EventCreate):
    new_event=Events(
        title=event_in.title,
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
def event_update(session:SessionDep,event_data:EventUpdate,event_id:int):
    event=session.get(Events,event_id)
    if not event:
        raise HTTPException(status_code=404,detail="Event not found")
    update_dict=event_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(event, key, value)
    session.commit()
    session.refresh(event)
    return event
@router.delete("/{event_id}",response_model=EventRead)
def delete_event(session:SessionDep,event_id:int):
    event=session.get(Events,event_id)
    if not event:
        raise HTTPException(status_code=404,detail="Event not found")
    if len(event.tickets)!=0:
        raise HTTPException(status_code=404,detail="Can not delete from live event")
    session.delete(event)
    session.commit()
    return event

    
