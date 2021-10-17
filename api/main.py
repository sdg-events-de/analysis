from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models import Event
from sqlalchemy.orm import joinedload, contains_eager

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sdg-events.de",
        "https://api.sdg-events.de",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EventResponse(BaseModel):
    id: int
    url: str
    host: Optional[str]
    display_title: Optional[str]
    status: str
    needs_review: bool

    class Config:
        orm_mode = True


class DetailedEventResponse(BaseModel):
    id: int
    url: str
    display_title: Optional[str]
    needs_review: bool
    attributes_to_review: Optional[list]

    class Config:
        orm_mode = True


@api.get("/")
def root():
    return {"message": "Hello World! :)"}


@api.get("/events", response_model=list[EventResponse])
def events():
    return Event.with_joined("suggestion").all()


@api.get("/events/{id}", response_model=DetailedEventResponse)
def read_event(id):
    event = (
        Event.with_joined("suggestion", "revision")
        .options(contains_eager("suggestion.event"))
        .filter(Event.id == id)
        .first()
    )

    if event:
        return event

    raise HTTPException(status_code=404, detail="Event not found")