from datetime import datetime,timedelta,timezone
import jwt
from pwdlib import PasswordHash

SECRET_KEY = "change-this-to-a-long-random-secret-key-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

password_hash=PasswordHash.recommended()

def hash_password(plain_password:str) -> str:
    return password_hash.hash(plain_password)

def verify_password(plain_password:str,hash_password:str) -> bool:
    return password_hash.verify(plain_password,hash_password)

def create_access_token(member_id:int,role:str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload={
        "sub":str(member_id),
        "role":role,
        "exp":expire,
    }
    
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

def decode_access_tokens(token:str) -> dict:
    return jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
