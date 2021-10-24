from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from models import BaseModel


class LogMessage(BaseModel):
    id = Column(Integer, primary_key=True)
    log_id = Column(Integer, ForeignKey("log.id"), nullable=False, index=True)
    logger = Column(String, nullable=False, default="root")
    levelno = Column(Integer, nullable=False)
    levelname = Column(String, nullable=False)
    content = Column(String, nullable=False)
    trace = Column(String)

    log = relationship("Log", back_populates="messages", foreign_keys=log_id)

    def on_create(self):
        if self.log.is_completed:
            raise Exception("The log has already been completed.")

        if self.log.levelno is None or self.log.levelno < self.levelno:
            self.log.levelno = self.levelno
            self.log.levelname = self.levelname
