from .EventSpiderBase import EventSpiderBase, EventBase
from helpers import matches_sdgs


class DgvnEvent(EventBase):
    ATTRIBUTES = [
        "url",
        "title",
        "summary",
        "description",
        "address",
        "is_online",
        "starts_at",
        "ends_at",
        "status",
        "status_note",
    ]

    @property
    def base_css(self):
        return self.response.css("div.tx-event")

    @property
    def title(self):
        return self.extract_text("h1.headline::text")

    @property
    def summary(self):
        return self.extract_text("div.detail__teaser")

    @property
    def description(self):
        return self.extract_text("div.detail__content-body")

    @property
    def starts_at(self):
        return self.combine_date_and_time(self.start_date, self.start_time)

    @property
    def ends_at(self):
        return self.combine_date_and_time(self.end_date, self.end_time)

    @property
    def is_online(self):
        return self.location == "Online"

    @property
    def address(self):
        if self.is_online:
            return None
        return self.location

    @property
    def status(self):
        if self.mentions_sdgs and not self.has_ended:
            return "published"

        return "deleted"

    @property
    def status_note(self):
        if not self.mentions_sdgs:
            return "Event does not mention SDGs"

        if self.has_ended:
            return "Event has ended"

        return None

    @property
    def date(self):
        return self.squish_whitespace(
            self.extract_text(
                'div.event-data__item:contains("Datum: ") span.event-data__value',
            )
        )

    @property
    def start_date(self):
        date = self.date.split(" – ")[0]

        # Add month
        if date.count(".") == 1 and date.endswith("."):
            date += f"{self.end_date.month}."

        # Add year
        if date.count(".") == 2 and date.endswith("."):
            date += f"{self.end_date.year}"

        return self.strptime(date, "%d.%m.%Y")

    @property
    def end_date(self):
        return self.strptime(self.date.split(" – ")[-1], "%d.%m.%Y")

    @property
    def time(self):
        return self.extract_text(
            'div.event-data__item:contains("Uhrzeit: ") span.event-data__value'
        )

    @property
    def start_time(self):
        if not self.time:
            return self.time_midnight()

        return self.strptime(self.time.split(" - ")[0], "%H:%Mh").time()

    @property
    def end_time(self):
        if not self.time:
            return self.time_midnight()

        return self.strptime(self.time.split(" - ")[-1], "%H:%Mh").time()

    @property
    def has_ended(self):
        return self.end_date < self.time_now()

    @property
    def mentions_sdgs(self):
        if matches_sdgs(self.description):
            return True

        return False

    @property
    def location(self):
        return self.extract_text(
            'div.event-data__item:contains("Ort: ") span.event-data__value'
        )


class DgvnEventSpider(EventSpiderBase):
    name = "DgvnEvent"
    allowed_domains = ["dgvn.de"]
    EventClass = DgvnEvent