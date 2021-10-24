import logging
import pytest
from models import Log, LogMessage


def test_it_can_create_logs():
    log = Log.create(name="Scraping Listings and Events")
    LogMessage.create(
        log=log, levelname="warn", levelno=logging.WARN, content="My log message"
    )
    log.complete()

    assert log.is_completed
    assert len(log.messages) == 1
    assert log.messages[0].content == "My log message"


def test_it_cannot_add_messages_to_completed_logs():
    log = Log.create(name="Scraping Listings and Events")
    log.complete()

    with pytest.raises(Exception, match="The log has already been completed."):
        LogMessage.create(
            log=log, levelname="warn", levelno=logging.WARN, content="My log message"
        )


def test_it_raises_level_on_log_if_new_messages_has_higher_level():
    log = Log.create(name="Scraping Listings and Events")

    LogMessage.create(log=log, levelname="info", levelno=logging.INFO, content="...")

    log.reload()
    assert log.levelno == logging.INFO
    assert log.levelname == "info"

    LogMessage.create(log=log, levelname="warn", levelno=logging.WARN, content="...")

    log.reload()
    assert log.levelno == logging.WARN
    assert log.levelname == "warn"


def test_it_keeps_level_on_log_if_new_messages_has_lower_level():
    log = Log.create(name="Scraping Listings and Events")

    LogMessage.create(log=log, levelname="warn", levelno=logging.WARN, content="...")
    LogMessage.create(log=log, levelname="debug", levelno=logging.INFO, content="...")

    log.reload()
    assert log.levelno == logging.WARN
    assert log.levelname == "warn"


def example_exception(logger):
    try:
        raise Exception("this will raise")
    except Exception as e:
        logger.exception("an error occurred")


def test_it_can_attach_to_logger():
    log = Log.create(name="Scraping Listings and Events")
    logger = logging.getLogger("testLogger")
    logger.setLevel(logging.INFO)
    logger.addHandler(log.create_handler())

    logger.info("an info message")
    example_exception(logger)

    assert len(log.messages) == 2
    assert log.messages[0].content == "an info message"
    assert log.messages[0].levelno == logging.INFO
    assert log.messages[0].logger == "testLogger"

    assert log.messages[1].content == "an error occurred"
    assert log.messages[1].trace != None
    assert log.messages[1].levelno == logging.ERROR
    assert log.messages[1].logger == "testLogger"
