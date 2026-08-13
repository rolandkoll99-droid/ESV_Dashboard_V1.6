#!/usr/bin/env python3
"""
ds18b20_bridge.py – liest zwei DS18B20-Temperatursonden (Raum + Asphalt/
Bahn) über die 1-Wire-Schnittstelle des Raspberry Pi aus und schreibt das
Ergebnis in sensors.json im lokalen Git-Repo. Committet und pusht die
Datei danach automatisch nach GitHub, damit das über GitHub Pages
ausgelieferte Dashboard sie unter "sensors.json" (selber Ursprung, HTTPS)
einlesen kann.

Voraussetzungen:
- 1-Wire-Interface auf dem Pi aktiviert (siehe RASPBERRY_PI_SENSOREN_SETUP.md)
- Beide DS18B20-Sonden angeschlossen (können sich dieselbe Datenleitung/
  GPIO teilen, jede hat eine eindeutige Werks-ID)
- Keine externe Bibliothek nötig – reine Python-Standardbibliothek, liest
  direkt aus dem Linux-Kernel-Treiber unter /sys/bus/w1/devices/

Läuft auf dem Raspberry Pi, NICHT im Browser.
"""

import json
import re
import subprocess
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ============================================================
# KONFIGURATION – hier anpassen
# ============================================================

# Werks-IDs der beiden Sonden (Ordnername unter /sys/bus/w1/devices/,
# z. B. "28-00000abcdef1"). Ermitteln siehe RASPBERRY_PI_SENSOREN_SETUP.md.
ROOM_SENSOR_ID = "28-XXXXXXXXXXXX"
ASPHALT_SENSOR_ID = "28-YYYYYYYYYYYY"

W1_BASE_PATH = Path("/sys/bus/w1/devices")

# Pfad zum lokalen Git-Repo (dort liegt auch dashboard.html)
REPO_PATH = Path.home() / "stocksport"
SENSORS_FILE = REPO_PATH / "sensors.json"
LOG_FILE = REPO_PATH / "tuya_bridge.log"  # Name beibehalten für Kontinuität mit alten Logs

# Wenn false, wird nur sensors.json geschrieben, aber nicht automatisch
# committet/gepusht (z. B. zum Testen).
GIT_AUTO_PUSH = True

# ============================================================
# SUPABASE (zentrale Historie – siehe SUPABASE_SETUP.md)
# ============================================================
# Leer lassen ("") um die Historie zu deaktivieren und nur sensors.json
# (aktueller Wert) wie bisher zu nutzen.
SUPABASE_URL = ""  # z. B. "https://xxxxxxxxxxxx.supabase.co"
# WICHTIG: hier den SECRET/SERVICE_ROLE-Key eintragen (umgeht Row Level
# Security für den Insert) – NIEMALS diesen Key ins Dashboard/Browser
# einbauen, nur hier auf dem Pi. Für das Dashboard gibt es einen
# separaten, öffentlichen PUBLISHABLE/ANON-Key, siehe SUPABASE_SETUP.md.
SUPABASE_SECRET_KEY = ""

# Wie oft ein fehlgeschlagener CRC-Check (bekanntes, gelegentliches
# 1-Wire-Problem) wiederholt wird, bevor aufgegeben wird.
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 1


# ============================================================
# LOGGING
# ============================================================

def log(msg):
    line = f"[{datetime.now().isoformat(timespec='seconds')}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


# ============================================================
# DS18B20 ÜBER 1-WIRE AUSLESEN
# ============================================================

def read_ds18b20(sensor_id, label):
    device_file = W1_BASE_PATH / sensor_id / "w1_slave"

    if not device_file.exists():
        raise RuntimeError(
            f"{label}: Gerät '{sensor_id}' nicht gefunden unter {device_file}. "
            f"Ist die Sonde angeschlossen und 1-Wire aktiviert? "
            f"Verfügbare Geräte: {[p.name for p in W1_BASE_PATH.glob('28-*')]}"
        )

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        raw = device_file.read_text()
        if "YES" in raw:
            match = re.search(r"t=(-?\d+)", raw)
            if match:
                return round(int(match.group(1)) / 1000, 1)
            last_error = f"Kein 't=' Wert in Ausgabe gefunden: {raw!r}"
        else:
            last_error = f"CRC-Check fehlgeschlagen (Versuch {attempt}/{MAX_RETRIES}): {raw!r}"
        time.sleep(RETRY_DELAY_SECONDS)

    raise RuntimeError(f"{label} ({sensor_id}): {last_error}")


# ============================================================
# SUPABASE – Historie zentral speichern (optional)
# ============================================================

def push_to_supabase(room_temp_c, asphalt_temp_c):
    if not SUPABASE_URL or not SUPABASE_SECRET_KEY:
        return  # Historie deaktiviert, sensors.json/GitHub reicht dann aus

    payload = json.dumps({
        "room_temp_c": room_temp_c,
        "asphalt_temp_c": asphalt_temp_c,
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{SUPABASE_URL}/rest/v1/sensor_readings",
        data=payload,
        method="POST",
        headers={
            "apikey": SUPABASE_SECRET_KEY,
            "Authorization": f"Bearer {SUPABASE_SECRET_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status not in (200, 201):
                log(f"Supabase-Insert unerwarteter Status: {resp.status}")
    except urllib.error.HTTPError as e:
        log(f"Supabase-Insert fehlgeschlagen: HTTP {e.code} – {e.read().decode(errors='replace')}")
    except urllib.error.URLError as e:
        log(f"Supabase-Insert fehlgeschlagen (Netzwerk): {e}")


# ============================================================
# GIT
# ============================================================

def git_commit_and_push():
    def run(cmd):
        return subprocess.run(cmd, cwd=REPO_PATH, capture_output=True, text=True)

    run(["git", "add", "sensors.json"])
    status = run(["git", "status", "--porcelain", "sensors.json"])
    if not status.stdout.strip():
        log("Keine Änderung an sensors.json – kein Commit nötig.")
        return

    commit = run(["git", "commit", "-m", "Sensordaten aktualisiert"])
    if commit.returncode != 0:
        log(f"git commit fehlgeschlagen: {commit.stderr.strip()}")
        return

    push = run(["git", "push"])
    if push.returncode != 0:
        log(f"git push fehlgeschlagen: {push.stderr.strip()}")
    else:
        log("sensors.json erfolgreich nach GitHub gepusht.")


# ============================================================
# HAUPTABLAUF
# ============================================================

def main():
    result = {
        "room_temp_c": None,
        "asphalt_temp_c": None,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    try:
        result["room_temp_c"] = read_ds18b20(ROOM_SENSOR_ID, "Raumsensor")
    except Exception as e:
        log(f"FEHLER Raumsensor: {e}")

    try:
        result["asphalt_temp_c"] = read_ds18b20(ASPHALT_SENSOR_ID, "Asphaltsensor")
    except Exception as e:
        log(f"FEHLER Asphaltsensor: {e}")

    SENSORS_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"sensors.json geschrieben: {result}")

    push_to_supabase(result["room_temp_c"], result["asphalt_temp_c"])

    if GIT_AUTO_PUSH:
        git_commit_and_push()


if __name__ == "__main__":
    main()
