# Roadmap Trainingsportal ESV Grein – Weg zum „Gesamtpaket mit allen Daten"

Stand: August 2026. Dieses Dokument bündelt die in den letzten Gesprächen
identifizierten Verbesserungspunkte, priorisiert nach Wirkung fürs
Gesamtziel „alle Trainings- und Umgebungsdaten an einem Ort, zuverlässig,
über die Saison hinweg auswertbar".

## Warum diese Reihenfolge

Die größte Lücke ist nicht ein einzelnes Feature, sondern die
**Datenarchitektur**: Trainings- und Sensordaten liegen aktuell verteilt
und größtenteils flüchtig (Browser-Speicher pro Gerät, Sensor-Momentaufnahme
ohne Historie). Bevor weitere Features draufgesetzt werden, lohnt es sich,
zuerst ein zentrales, verlässliches Datenfundament zu schaffen – alles
andere baut darauf auf.

---

## Phase 1 – Fundament: zentrale Datenhaltung (höchste Priorität)

**Ziel:** Ein zentraler Speicher, auf den alle Geräte (Pi, Tablet,
Spieler-Handys) zugreifen können, statt isolierter Browser-Speicher pro
Gerät.

**Empfohlener Ansatz:** Ein kleiner, kostenloser Cloud-Datenbankdienst
(z. B. **Supabase** – Postgres-Datenbank mit fertiger REST-API, kostenloser
Tarif für den Vereinsbedarf ausreichend, funktioniert nahtlos mit der
bestehenden GitHub-Pages-Architektur, da die API über HTTPS mit einem
für den Client gedachten „anon key" sicher erreichbar ist – anders als
der Tuya-Key vorhin).

**Einstiegspunkt (risikoarm):** Nicht sofort die bestehende, gewachsene
Spielerverwaltung/Trainingsanalyse migrieren (hohes Risiko, sehr große
Dateien), sondern mit etwas komplett Neuem anfangen:

1.1 **Sensor-Historie zentral speichern** *(→ wird jetzt umgesetzt, siehe unten)*
1.2 Kleine „Verlaufsanzeige" im Dashboard (Temperaturverlauf statt nur
    Momentaufnahme)
1.3 Erst danach, als eigener späterer Schritt: Spielerliste und
    Trainingsergebnisse schrittweise auf dieselbe zentrale Datenbank
    umstellen (größerer Umbau, eigene Planung nötig)

---

## Phase 2 – Ausfallsicherheit Pi (bevor Monate an Daten daran hängen)

2.1 Hochwertige „High Endurance"-SD-Karte oder Boot von USB-SSD
    (SD-Karten-Verschleiß durch häufige Schreibzugriffe)
2.2 Unterbrechungsfreie Stromversorgung / sauberes Herunterfahren
    (Datenkorruption bei Stromausfall vermeiden)
2.3 LAN statt WLAN für den Pi, wo möglich (Stabilität)

## Phase 3 – Software-Politur

3.1 Temperatur-Historie place (siehe Phase 1.1) mit Trainingsergebnissen
    verknüpfen (Auswertung „Leistung vs. Temperatur")
3.2 Offline-Fallback (Service Worker) gegen kurze Internetausfälle
3.3 Automatischer Kiosk-Neustart/Reload-Konzept
3.4 Echter Zugriffsschutz statt Klartext-Passwort (`auth.js`)
3.5 Wetter-/API-Keys individuell pro Verein statt geteilt (relevant vor
    Weitergabe an andere Vereine)

## Phase 4 – Hardware-Feinschliff

4.1 Kabeldurchführung/Wetterschutz der Asphaltsonde
4.2 Sonnenschutz/Blende für den Touch-Monitor bei Außeneinsatz

## Phase 5 – Erweiterte Sensorik (optional, nach Bedarf)

5.1 BME280 statt/zusätzlich DS18B20 (Luftfeuchtigkeit, Luftdruck)
5.2 Mehrere Asphaltmesspunkte statt einem
5.3 Windmessung (nur falls wirklich benötigt – aufwendiger/teurer)

---

## Status

| Punkt | Status |
|---|---|
| 1.1 Sensor-Historie zentral | 🔵 wird jetzt begonnen |
| 1.2 Verlaufsanzeige Dashboard | 🔵 wird jetzt begonnen |
| 1.3 Spieler-/Trainingsdaten migrieren | ⚪ geplant, eigener Schritt |
| 2.x Pi-Ausfallsicherheit | ⚪ offen |
| 3.x Software-Politur | ⚪ offen |
| 4.x Hardware-Feinschliff | ⚪ offen |
| 5.x Erweiterte Sensorik | ⚪ offen, optional |
