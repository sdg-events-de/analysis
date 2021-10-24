import logging
import sys
import traceback
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from .BaseModel import BaseModel
from .LogMessage import LogMessage


class LogHandler(logging.Handler):
    def __init__(self, log):
        super().__init__()
        self.log = log

    def emit(self, record):
        trace = traceback.format_exc() if record.exc_info else None
        LogMessage.create(
            log=self.log,
            logger=record.name,
            levelno=record.levelno,
            levelname=record.levelname,
            trace=trace,
            content=record.getMessage(),
        )


class Log(BaseModel):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    levelno = Column(Integer)
    levelname = Column(String)
    completed_at = Column(DateTime)

    messages = relationship("LogMessage", back_populates="log")

    def complete(self):
        self.update(completed_at=datetime.now())

    def create_handler(self):
        return LogHandler(log=self)

    @property
    def is_completed(self):
        return self.completed_at is not None