from fastapi import APIRouter,HTTPException
from seatapi.schema import MemberRead,MemberUpdate
from seatapi.models import Members,Tickets
from seatapi.database import SessionDep
from sqlalchemy import select
from seatapi.dependencies import CurrentMember,AdminMember

router=APIRouter(prefix="/members",tags=["members"])


@router.patch("/update",response_model=MemberRead)
def update_cred(session:SessionDep,member_in:CurrentMember,member_data:MemberUpdate):
    member=session.get(Members,member_in.id)
    if not member:
        raise HTTPException(status_code=400,detail="Member not found")
    update_dict=member_data.model_dump(exclude_unset=True)
    if member_data.phone_number:
        if member_data.phone_number<1000000000 or member_data.phone_number>9999999999:
            raise HTTPException(status_code=404,detail="Enter a valid Phone number")
        
    for key,value in update_dict.items():
        setattr(member,key,value)
    session.commit()
    session.refresh(member)
    return member
@router.get("/details",response_model=MemberRead)
def get_details(session:SessionDep,members:CurrentMember):
    member=session.get(Members,members.id)
    return member
@router.get("/all",response_model=list[MemberRead])
def get_all_members(session:SessionDep,member:AdminMember):
    members=session.scalars(select(Members)).all()
    return members
@router.delete("/",response_model=MemberRead)
def delete_member(session:SessionDep,member:CurrentMember):

    membert=session.get(Members,member.id)
    any_events=session.scalar(select(Tickets).where(Tickets.customer_id==member.id,Tickets.cancelled==False))

    if any_events:
        raise HTTPException(status_code=400,detail="Member in active event")
    if not membert:
        raise HTTPException(status_code=400,detail="Member not found")
    session.delete(membert)
    session.commit()
    return membert    


