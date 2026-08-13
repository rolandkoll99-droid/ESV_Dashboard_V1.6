# Zentrale Temperatur-Historie (Supabase)

Diese Anleitung ergänzt `RASPBERRY_PI_SENSOREN_SETUP.md` um einen
**Temperaturverlauf** im Dashboard, statt nur den aktuellen Wert
anzuzeigen (Roadmap-Punkt 1.1/1.2, siehe `ROADMAP.md`).

**Optional:** Ohne diese Einrichtung funktioniert das Dashboard genauso
wie bisher – aktuelle Werte über `sensors.json`. Die Verlaufskarte
erscheint einfach nicht, wenn `SUPABASE_URL` leer bleibt.

## Warum Supabase

Anders als bei Tuya braucht Supabase **zwei unterschiedliche Schlüssel**
mit unterschiedlicher Berechtigung – dadurch lässt sich der Lesezugriff
fürs Dashboard sicher direkt im Browser einbauen, ohne dass jemand damit
Daten verändern könnte:

- **Secret-Key** (früher „service_role key“ genannt) – umgeht jede
  Zugriffsbeschränkung, darf **nur auf dem Pi** stehen (in
  `ds18b20_bridge.py`), niemals im Dashboard.
- **Publishable-Key** (früher „anon key“ genannt) – für den Browser
  gedacht, öffentlich sichtbar im Quelltext ist damit unproblematisch,
  weil die Datenbank selbst (über „Row Level Security“) festlegt, dass
  dieser Key **nur lesen**, nicht schreiben darf.

*Hinweis:* Supabase benennt diese Schlüssel gerade neu (Legacy-Namen
„anon“/„service_role“ laufen bis Ende 2026 aus, neue Namen
„publishable“/„secret“). Je nachdem, wann du dein Projekt anlegst, siehst
du eventuell noch die alten Bezeichnungen – gemeint ist dasselbe.

## 1. Supabase-Projekt anlegen

1. Kostenlosen Account auf **supabase.com** anlegen, neues Projekt
   erstellen (Region möglichst nah an Europa wählen).
2. Im Projekt unter **SQL Editor** folgendes SQL ausführen, um die
   Tabelle für die Sensor-Historie anzulegen:

   ```sql
   create table if not exists sensor_readings (
     id bigint generated always as identity primary key,
     created_at timestamptz not null default now(),
     room_temp_c numeric,
     asphalt_temp_c numeric
   );

   alter table sensor_readings enable row level security;

   create policy "Public read access"
     on sensor_readings
     for select
     to anon
     using (true);
   ```

   Das erlaubt **nur Lesen** für den öffentlichen Key – es gibt bewusst
   **keine** Insert/Update/Delete-Policy für `anon`. Schreiben kann daher
   ausschließlich der Secret-Key (der die Policies komplett umgeht).

3. Unter **Project Settings → API** findest du:
   - die **Projekt-URL** (z. B. `https://xxxxxxxxxxxx.supabase.co`)
   - den **Publishable-/Anon-Key** (öffentlich, für den Browser)
   - den **Secret-/Service-Role-Key** (geheim, nur für den Pi)

## 2. Pi einrichten (`ds18b20_bridge.py`)

In `ds18b20_bridge.py` eintragen:

```python
SUPABASE_URL = "https://xxxxxxxxxxxx.supabase.co"
SUPABASE_SECRET_KEY = "dein-secret-key"
```

Ab dem nächsten Durchlauf (manuell testen mit `python3 ds18b20_bridge.py`)
schreibt das Skript jede Messung zusätzlich zu `sensors.json` auch als
neue Zeile in die Supabase-Tabelle. Fehler beim Insert landen wie gehabt
in `tuya_bridge.log`.

## 3. Dashboard einrichten (`dashboard.html`)

Im Skriptbereich von `dashboard.html` eintragen:

```js
const SUPABASE_URL = 'https://xxxxxxxxxxxx.supabase.co';
const SUPABASE_PUBLISHABLE_KEY = 'dein-publishable-key';
```

**Wichtig:** Hier nur den Publishable-/Anon-Key eintragen, niemals den
Secret-Key – dieser Wert landet im öffentlich sichtbaren Quelltext der
Webseite.

Nach dem nächsten `git push` und der GitHub-Pages-Aktualisierung zeigt
das Dashboard automatisch eine Verlaufskarte mit den letzten 48 Stunden,
sobald mindestens zwei Messpunkte in der Datenbank stehen.

## 4. Aufbewahrungsdauer / Aufräumen (optional)

Ohne weiteres Zutun wächst die Tabelle unbegrenzt (bei einer Messung alle
5 Minuten sind das ca. 105.000 Zeilen/Jahr – für den kostenlosen
Supabase-Tarif kein Problem, aber überschaubar zu halten schadet nicht).
Optional lässt sich im SQL Editor ein Aufräum-Zeitplan einrichten, der
z. B. Daten älter als 1 Jahr löscht:

```sql
create extension if not exists pg_cron;

select cron.schedule(
  'cleanup-old-sensor-readings',
  '0 3 * * *',  -- täglich um 03:00 Uhr
  $$ delete from sensor_readings where created_at < now() - interval '1 year' $$
);
```

## 5. Fehlersuche

- **Verlaufskarte erscheint nicht**: `SUPABASE_URL`/`SUPABASE_PUBLISHABLE_KEY`
  in `dashboard.html` korrekt gesetzt? Mindestens 2 Messwerte in der
  Datenbank? Browser-Konsole (F12) prüfen, ob der Fetch-Aufruf einen
  Fehler zeigt.
- **„new row violates row-level security policy“** im `tuya_bridge.log`
  des Pi: Der Pi verwendet versehentlich den Publishable- statt den
  Secret-Key, oder die Policy aus Schritt 1 fehlt.
- **Dashboard zeigt Daten, aber falsche/keine Werte für einen Sensor**:
  in der Supabase-Tabelle direkt nachschauen (Table Editor), ob
  `room_temp_c`/`asphalt_temp_c` für die jeweilige Zeile wirklich befüllt
  sind – leere Werte werden im Chart automatisch übersprungen.
