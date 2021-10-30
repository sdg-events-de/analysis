from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import contains_eager
from models import Event, EventSuggestion, Log
from api.models import EventResponse, DetailedEventResponse

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sdg-events.de",
        "https://admin.sdg-events.de",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/")
def root():
    return {"message": "Hello World! :)"}


@api.get("/events", response_model=list[EventResponse])
def events():
    return Event.with_joined("suggestion").order_by("id").all()


@api.get("/events/review", response_model=list[EventResponse])
def events_to_review():
    print(
        Event.query.join(Event.suggestion)
        .options(contains_eager(Event.suggestion))
        .filter(Event.needs_review)
        .filter(
            (Event.status == "published")
            | ((Event.status == "draft") & (EventSuggestion.status == "published"))
        )
        .order_by("id")
    )

    return (
        Event.query.join(Event.suggestion)
        .options(contains_eager(Event.suggestion))
        .filter(Event.needs_review)
        .filter(
            (Event.status == "published")
            | ((Event.status == "draft") & (EventSuggestion.status == "published"))
        )
        .order_by("id")
        .all()
    )


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