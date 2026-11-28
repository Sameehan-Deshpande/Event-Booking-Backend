from typing import Annotated

from seatapi.database import SessionDep
from seatapi.security import decode_access_tokens
from seatapi.models import Members

import jwt
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import Depends,HTTPException,status
from sqlalchemy import select

bearer_scheme=HTTPBearer()

def get_current_member(credentials:Annotated[HTTPAuthorizationCredentials,Depends(bearer_scheme)],session:SessionDep):
    credentials_exception = HTTPException(status_code=401,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"},)
    try:
        payload=decode_access_tokens(credentials.credentials)
        subject=payload.get("sub")
        if not subject:
            raise credentials_exception
        member_id=int(subject)
    except(jwt.InvalidTokenError, ValueError, TypeError):
        raise credentials_exception
    member=session.scalar(select(Members).where(Members.id==member_id))
    if not member:
        raise HTTPException(status_code=404,detail="Member not found")
    return member
CurrentMember=Annotated[Members,Depends(get_current_member)]

def get_admin_member(member:CurrentMember):
    if member.role!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Admin status required")
    return member
AdminMember=Annotated[Members,Depends(get_admin_member)]