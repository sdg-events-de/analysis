from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from models import Event

api = FastAPI()


class EventResponse(BaseModel):
    url: str
    display_title: Optional[str]
    status: str
    needs_review: bool

    class Config:
        orm_mode = True


@api.get("/")
def root():
    return {"message": "Hello World! :)"}


@api.get("/events", response_model=list[EventResponse])
def events():
    return Event.with_joined("suggestion").all()
