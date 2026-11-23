from sqlalchemy import create_engine
from sqlalchemy.orm import Session,DeclarativeBase,sessionmaker
from typing import Annotated
from fastapi import Depends


URL="sqlite:///database.db"
engine=create_engine(URL,connect_args={"check_same_thread":False},echo=True)

SessionLocal=sessionmaker(bind=engine,autoflush=False)
class Base(DeclarativeBase):

    pass

def get_db_and_tables():
    import seatapi.models
    Base.metadata.create_all(bind=engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep=Annotated[Session,Depends(get_session)]

        