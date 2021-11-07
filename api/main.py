from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import contains_eager
from models import Event, EventSuggestion, Log
from api.models import (
    EventResponse,
    EventReviewResponse,
    EventReviewRequest,
    DetailedEventResponse,
    LogResponse,
    LogWithMessagesResponse,
)

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


@api.get("/events/review/{id}", response_model=EventReviewResponse)
def read_event_to_review(id):
    event = (
        Event.with_joined("suggestion", "revision")
        .options(contains_eager("suggestion.event"))
        .filter(Event.id == id)
        .first()
    )

    if event:
        return event

    raise HTTPException(status_code=404, detail="Event not found")


@api.post("/events/review/{id}")
def submit_event_review(id: int, review: EventReviewRequest):
    event = (
        Event.with_joined("suggestion", "revision")
        .options(contains_eager("suggestion.event"))
        .filter(Event.id == id)
        .first()
    )

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event.review(**review.dict(exclude_unset=True))

    return {"success": True}


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


@api.get("/logs", response_model=list[LogResponse])
def logs():
    return Log.query.order_by(Log.id.desc()).all()


@api.get("/logs/{id}", response_model=LogWithMessagesResponse)
def logs(id):
    log = Log.with_joined("messages").filter(Log.id == id).first()

    if log:
        return log

    raise HTTPException(status_code=404, detail="Log not found")
