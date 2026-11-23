from fastapi import APIRouter,HTTPException
from seatapi.schema import MemberCreate,MemberRead,MemberUpdate
from seatapi.models import Members
from seatapi.database import SessionDep
from sqlalchemy import select

router=APIRouter(prefix="/members",tags=["members"])

@router.post("/create",response_model=MemberRead)
def new_member(session:SessionDep,member_in:MemberCreate):
    member=Members(
        attendee_name=member_in.attendee_name,
        phone_number=member_in.phone_number,
    )
    session.add(member)
    session.commit()
    session.refresh(member)
    return member
@router.patch("/update/{member_id}",response_model=MemberRead)
def update_cred(session:SessionDep,member_id:int,member_data:MemberUpdate):
    member=session.get(Members,member_id)
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
@router.get("/details/{member_id}",response_model=MemberRead)
def get_details(session:SessionDep,member_id:int):
    member=session.get(Members,member_id)
    return member
@router.get("/all",response_model=list[MemberRead])
def get_all_members(session:SessionDep):
    members=session.scalars(select(Members))
    return members
@router.delete("/{member_id}",response_model=MemberRead)
def delete_member(session:SessionDep,member_id:int):
    member=session.get(Members,member_id)
    if not member:
        raise HTTPException(status_code=400,detail="Member not found")
    session.delete(member)
    session.commit()
    return member    


