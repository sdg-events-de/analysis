from datetime import datetime
import requests
import pytest
from freezegun import freeze_time
from scrapy.http import HtmlResponse
from scrape.spiders.events.EngagementGlobalEventSpider import (
    EngagementGlobalEventSpider,
)
from helpers import matches_dict


@pytest.mark.vcr()
def test_it_scrapes_event():
    url = "https://skew.engagement-global.de/veranstaltung-detail/online-seminar-einstieg-in-den-kompass-nachhaltigkeit-3799.html"

    # forge a scrapy response to test
    scrapy_response = HtmlResponse(body=requests.get(url).content, url=url)

    results = EngagementGlobalEventSpider().parse(scrapy_response)
    event = next(results)

    assert (
        {
            "url": url,
            "title": "Online-Seminar Einstieg in den Kompass Nachhaltigkeit",
            "description": """Wie kann ich den Kompass Nachhaltigkeit nutzen, um Ausschreibungen mit sozialen und ökologischen Kriterien erfolgreich durchzuführen?
Unser Online-Seminar zeigt, welche Möglichkeiten die Webplattform bietet. Anhand von Übungsaufgaben können Fragestellungen direkt ausprobiert werden.

Bitte beachten Sie, dass die Teilnehmendenzahl für dieses Online-Seminar leider begrenzt ist.
Nach erfolgter Anmeldung erhalten Sie wenige Tage vor der Veranstaltung den Link zur Teilnahme über WebEx und weitere Informationen. Sie müssen hierfür keine weiteren Installationen an Ihrem Computer vornehmen.

Veranstaltungsort

Online

Kontakt


Sabrina Limburger
+49 228 20717 2159
Sabrina.Limburger@engagement-global.de

Anmeldung

Die Frist für die Online-Anmeldung ist bereits abgelaufen.""",
            "starts_at": datetime.fromisoformat("2021-11-02T10:30:00"),
            "ends_at": datetime.fromisoformat("2021-11-02T12:00:00"),
            "is_online": True,
            "address": None,
            "status": "deleted",
            "status_note": "Event does not mention SDGs",
        }
        == matches_dict(event)
    )


@pytest.mark.vcr()
@freeze_time("2021-09-11")
def test_it_scrapes_sdg_event():
    url = "https://skew.engagement-global.de/veranstaltung-detail/sustainable-partnerships-for-sustainable-development.html"

    # forge a scrapy response to test
    scrapy_response = HtmlResponse(body=requests.get(url).content, url=url)

    results = EngagementGlobalEventSpider().parse(scrapy_response)
    event = next(results)

    assert (
        {
            "url": url,
            "title": "Sustainable Partnerships for Sustainable Development",
            "description": """Virtuelle internationale Partnerschaftskonferenz der Initiative „Kommunales Know-How für Nahost“

Mit einem zweiteiligen Konferenzkonzept lässt die Initiative „Kommunales Know-how für Nahost“ (IKKN) der SKEW von Engagement Global ihre laufende zweite Projektphase ausklingen und die dritte und letzte Projektphase anlaufen.
Als Abschlussveranstaltung für die zweite Projektphase findet am 9. und 10. November 2021, jeweils halbtägig, eine virtuelle Konferenz statt. Etwa 100 Teilnehmende aus jordanischen, libanesischen, türkischen und deutschen Partnerkommunen werden zusammenkommen und gemeinsam auf die gesammelten Erfahrungen blicken. Welche Synergien finden wir dabei gemeinsam? Welche Strategien und Konzepte haben sich bewährt und können übertragen werden?
In der dritten Phase der IKKN, beginnend im Januar 2022, soll es vor allem darum gehen, die Partnerschaften und das Netzwerk nachhaltig zu festigen und zu stärken. Aber wie können wir den gemeinsamen andauernden regionalen Herausforderungen - wie politischer Instabilität, Wirtschaftskrisen und Jugendarbeitslosigkeit -, aber auch den übergreifenden globalen Problemen - wie sozialer Ungleichheit, Flucht und Vertreibung sowie der Corona-Pandemie - begegnen? Wie können wir die lokale Regierungsführung stärken und die Resilienz unserer Kommunen im Krisenmanagement ausbauen? Die Teilnehmenden diskutieren diese Fragen in verschiedenen Arbeitsgruppen während der beiden Konferenztage. Eine Podiumsdiskussion zu den Herausforderungen und Chancen der Kommunen bei der Umsetzung der Agenda 2030 am zweiten Vormittag rundet die Veranstaltung ab.
Ein zweiter Teil dieser Veranstaltungsreihe, geplant für September 2022, baut auf der virtuellen Veranstaltung im November auf. Bei dieser Konferenz werden die Teilnehmenden die Fragestellungen weiter vertiefen. Diese Veranstaltung wird voraussichtlich in Jordanien in Präsenz stattfinden. Schon jetzt freuen sich die Teilnehmenden darauf, sich endlich (wieder) auch „in echt“ treffen zu können.

Kontakt


Faraz Dahar
+49 228 20717 2637
Faraz.Dahar@engagement-global.de

Weitere Informationen


Zur Internetseite der Initiative Kommunales Know-how für Nahost

Anmeldung

zur Online-Anmeldung""",
            "starts_at": datetime.fromisoformat("2021-11-09T00:00:00"),
            "ends_at": datetime.fromisoformat("2021-11-10T00:00:00"),
            "status": "published",
        }
        == matches_dict(event)
    )


@pytest.mark.vcr
def test_it_scrapes_multi_day_event():
    url = "https://skew.engagement-global.de/veranstaltung-detail/6-vernetzungstreffen-club-der-agenda-2030-kommunen.html"

    # forge a scrapy response to test
    scrapy_response = HtmlResponse(body=requests.get(url).content, url=url)

    results = EngagementGlobalEventSpider().parse(scrapy_response)
    event = next(results)

    assert {
        "url": url,
        "title": "6. Vernetzungstreffen Club der Agenda 2030 Kommunen",
        "starts_at": datetime.fromisoformat("2021-11-04T00:00:00"),
        "ends_at": datetime.fromisoformat("2021-11-05T00:00:00"),
        "address": "Berlin",
        "is_online": False,
    } == matches_dict(event)


@pytest.mark.vcr
def test_it_sets_no_date_on_certain_events():
    url = "https://www.engagement-global.de/veranstaltung-detail/ewnt-weiterbildung-globales-lernen-3718.html"

    # forge a scrapy response to test
    scrapy_response = HtmlResponse(body=requests.get(url).content, url=url)

    results = EngagementGlobalEventSpider().parse(scrapy_response)
    event = next(results)

    assert {
        "url": url,
        "title": "EWNT Weiterbildung Globales Lernen",
        "starts_at": None,
        "ends_at": None,
        "address": None,
        "is_online": True,
    } == matches_dict(event)


@pytest.mark.vcr
def test_it_scrapes_time_correctly():
    url = "https://www.engagement-global.de/veranstaltung-detail/ringvorlesung-2021-ambivalenzen-der-digitalisierung-f%C3%BCr-nachhaltigen-frieden.html"

    # forge a scrapy response to test
    scrapy_response = HtmlResponse(body=requests.get(url).content, url=url)

    results = EngagementGlobalEventSpider().parse(scrapy_response)
    event = next(results)

    assert {
        "url": url,
        "title": "Ringvorlesung 2021 - Ambivalenzen der Digitalisierung für nachhaltigen Frieden",
        "starts_at": datetime.fromisoformat("2021-12-06T18:00:00"),
        "ends_at": datetime.fromisoformat("2021-12-06T19:30:00"),
    } == matches_dict(event)


@pytest.mark.vcr(record_mode="once")
def test_it_scrapes_time_correctly_2():
    url = "https://www.engagement-global.de/veranstaltung-detail/bne-stiftungsforum-5-ps-for-future.html"

    # forge a scrapy response to test
    scrapy_response = HtmlResponse(body=requests.get(url).content, url=url)

    results = EngagementGlobalEventSpider().parse(scrapy_response)
    event = next(results)

    assert {
        "url": url,
        "title": "BNE-StiftungsForum: 5 P‘s For Future!",
        "starts_at": datetime.fromisoformat("2021-12-16T10:00:00"),
        "ends_at": datetime.fromisoformat("2021-12-16T17:00:00"),
    } == matches_dict(event)