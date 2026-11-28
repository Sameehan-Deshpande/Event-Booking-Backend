from fastapi import APIRouter,HTTPException
from sqlalchemy import select

from seatapi.security import decode_access_tokens,create_access_token,hash_password,verify_password
from seatapi.schema import MemberRegister,MemberAuthRead,MemberLogin,Token
from seatapi.database import SessionDep
from seatapi.models import Members
router=APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register",response_model=MemberAuthRead)
def register_member(payload:MemberRegister,session:SessionDep):
    statement=session.scalar(select(Members).where(Members.phone_number==payload.phone_number))
    if statement:
        raise HTTPException(status_code=409,detail="member already exists")
    newmember=Members(
        attendee_name=payload.attendee_name,
        phone_number=payload.phone_number,
        hashed_password=hash_password(payload.password),
        role="member"
    )
    session.add(newmember)
    session.commit()
    session.refresh(newmember)
    return newmember

@router.post("/login",response_model=Token)
def login(session:SessionDep,payload:MemberLogin):
    user=session.scalar(select(Members).where(Members.phone_number==payload.phone_number))
    if not user:
        raise HTTPException(status_code=404,detail="No user found with this phone number")
    login=verify_password(payload.password,user.hashed_password)
    if not login:
        raise HTTPException(status_code=401,detail="Please check the password or phone number and try again",headers={"WWW-Authenticate": "Bearer"},)
    token=create_access_token(member_id=user.id,role="member")
    return Token(access_token=token,token_type="bearer")
