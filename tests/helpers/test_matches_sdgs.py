from helpers import matches_sdgs


def test_it_ignores_unrelated_text():
    assert not matches_sdgs("die Ziele für eine bessere Welt")
    assert not matches_sdgs("Biodiversität und Nachhaltigkeit im Fokus")


def test_it_matches_sdgs():
    assert matches_sdgs("die SDGs sind eine globale Agenda")
    assert matches_sdgs("SDG 13 on Climate Action")
    assert matches_sdgs("SDG13 on Climate Action")


def test_it_matches_agenda_2030():
    assert matches_sdgs("die Agenda 2030 ist")
    assert matches_sdgs("die 2030 Agenda ist")
    assert matches_sdgs("die UN Agenda2030 ist")


def test_it_matches_ziele_fuer_nachhaltige_entwicklung():
    assert matches_sdgs("ein Ziele für Nachhaltige Entwicklung")
    assert matches_sdgs("die ziele für nachhaltige entwicklung")
    assert matches_sdgs("mit den Zielen für Nachhaltige Entwicklung")