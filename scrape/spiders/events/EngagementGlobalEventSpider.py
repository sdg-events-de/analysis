import re
from .EventSpiderBase import EventSpiderBase, EventBase
from helpers import matches_sdgs


class EngagementGlobalEvent(EventBase):
    ATTRIBUTES = [
        "url",
        "title",
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
        return self.response.css("div.event")

    @property
    def title(self):
        return self.extract_text("h1::text")

    @property
    def description(self):
        elements = [
            el
            for el in self.response.css("div.event > *")
            if "table-event" not in el.attrib["class"]
        ]
        texts = [self.element_to_text(element) for element in elements]
        return self.join_texts(texts, "\n\n")

    @property
    def starts_at(self):
        if not self.start_date:
            return None

        return self.combine_date_and_time(self.start_date, self.start_time)

    @property
    def ends_at(self):
        if not self.end_date:
            return None

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
                'div.table-event tr:contains("Datum:") td',
            )
        )

    @property
    def start_date(self):
        date = re.split(r" (bis|und) ", self.date)[0].strip()

        # Add year, if missing
        if not re.search(r" \d{4}$", date) and self.end_date:
            date += f" {self.end_date.year}"

        return self.parse_date(
            date,
            languages=["de"],
            settings={"STRICT_PARSING": True},
        )

    @property
    def end_date(self):
        return self.parse_date(
            re.split(r" (bis|und) ", self.date)[-1],
            languages=["de"],
            settings={"STRICT_PARSING": True},
        )

    @property
    def time(self):
        time = self.extract_text(
            'div.table-event tr:contains("Uhrzeit:") td',
        )

        return time if re.match(r"^[\d:]+( Uhr)? bis [\d:]+ Uhr$", time) else None

    @property
    def start_time(self):
        if not self.time:
            return self.time_midnight()

        return self.parse_time(
            self.time.split(" bis ")[0], date_formats=["%H", "%H Uhr", "%H:%M Uhr"]
        ).time()

    @property
    def end_time(self):
        if not self.time:
            return self.time_midnight()

        return self.parse_time(
            self.time.split(" bis ")[-1], date_formats=["%H Uhr", "%H:%M Uhr"]
        ).time()

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
        return self.extract_text('div.table-event tr:contains("Ort:") td')


class EngagementGlobalEventSpider(EventSpiderBase):
    name = "EngagementGlobalEvent"
    allowed_domains = [
        "global-engagement.de",
        "www.engagement-global.de",
        "skew.engagement-global.de",
        "feb.engagement-global.de",
    ]
    EventClass = EngagementGlobalEvent