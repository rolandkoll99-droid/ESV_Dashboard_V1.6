# Raum- & Asphalttemperatur im Dashboard (DS18B20-Tauchsonden)

Diese Anleitung richtet zwei wasserdichte DS18B20-Temperatursonden ein
(„Temperatursensor-Modul-Kit mit wasserdichter Edelstahlsonde für Arduino
und Raspberry Pi“) – eine für die Raumtemperatur, eine für die
Asphalt-/Bahntemperatur. Die Werte erscheinen automatisch im Dashboard.

**Das ist die einfachste und zuverlässigste der bisher besprochenen
Varianten:** Die Sonden werden direkt per Kabel an den Raspberry Pi
angeschlossen (1-Wire-Protokoll) – kein WLAN am Sensor, keine App, keine
Cloud, kein API-Key, keine externe Python-Bibliothek nötig. Gerade für
die Asphaltsonde (oft im Freien, wo WLAN-Empfang schwach ist) ein klarer
Vorteil gegenüber den WLAN-Varianten von vorhin.

## 1. Sonden anschließen

Beide Sonden können sich **dieselbe Datenleitung (GPIO 4)** teilen – das
ist die Besonderheit von 1-Wire: jede Sonde hat eine eindeutige,
werkseitig eingebrannte ID, sodass beliebig viele Sonden an einer Leitung
hängen können.

| Sondenkabel | Pi-Anschluss (BCM-Nummerierung) | Pi-Pin (physisch) |
|---|---|---|
| Rot (VDD)   | 3.3V                              | Pin 1              |
| Schwarz (GND) | GND                             | Pin 6 (oder 9, 14, 20, 25, 30, 34, 39) |
| Gelb (Data) | GPIO 4                            | Pin 7               |

Zusätzlich einen **4,7-kΩ-Pull-up-Widerstand** zwischen Datenleitung
(GPIO 4) und 3.3V einbauen (liegt vielen DS18B20-Kits bereits bei). Beide
Sonden werden parallel an dieselben drei Punkte angeschlossen (VDD an
VDD, GND an GND, Data an Data) – nur ein Widerstand für beide zusammen
nötig.

*Alternative ohne externen Widerstand:* Der interne Pull-up des Pi lässt
sich per Software aktivieren (`dtoverlay=w1-gpio-pullup` statt
`w1-gpio`, siehe Schritt 2) – in der Praxis ist ein echter Widerstand
aber zuverlässiger, besonders bei längeren Kabeln zur Außenbahn.

**Vor dem Anschließen den Pi ausschalten** (`sudo shutdown -h now`),
danach erst verkabeln.

## 2. 1-Wire-Interface aktivieren

```bash
sudo raspi-config
```

→ **Interface Options → 1-Wire → Yes** → Finish → Neustart.

(Alternativ manuell: in `/boot/config.txt` bzw. `/boot/firmware/config.txt`
die Zeile `dtoverlay=w1-gpio` ergänzen und neu starten.)

## 3. Sonden erkennen und Werks-IDs ablesen

Nach dem Neustart:

```bash
ls /sys/bus/w1/devices/
```

Es sollten zwei Einträge erscheinen, die mit `28-` beginnen, z. B.:

```
28-00000a1b2c3d  28-00000e4f5a6b  w1_bus_master1
```

Das sind die eindeutigen IDs der beiden Sonden – diese kommen später in
`ds18b20_bridge.py`.

**Testweise auslesen:**

```bash
cat /sys/bus/w1/devices/28-00000a1b2c3d/w1_slave
```

Ausgabe z. B.:

```
b4 01 4b 46 7f ff 0e 10 74 : crc=74 YES
b4 01 4b 46 7f ff 0e 10 74 t=23500
```

`YES` bedeutet: Prüfsumme korrekt, Messung gültig. `t=23500` bedeutet
23,5 °C (Wert steht in 1/1000 °C).

## 4. Herausfinden, welche ID zu welcher Sonde gehört

Da beide Sonden dieselbe Leitung teilen, muss man einmalig zuordnen,
welche ID die Raum- und welche die Asphaltsonde ist:

1. Eine der beiden Sonden kurz in der Hand warm werden lassen (oder in
   warmes Wasser halten).
2. Beide IDs kurz hintereinander auslesen:
   ```bash
   cat /sys/bus/w1/devices/28-00000a1b2c3d/w1_slave
   cat /sys/bus/w1/devices/28-00000e4f5a6b/w1_slave
   ```
3. Die ID mit dem spürbar höheren `t=`-Wert ist die gerade erwärmte
   Sonde – so lässt sich zuordnen, welche ID physisch welches Kabel ist.
4. IDs beschriften (z. B. mit Klebeband am Kabel notieren), bevor die
   Sonden endgültig verlegt werden (eine an die Bahn/Asphalt, eine im
   Innenraum).

## 5. `ds18b20_bridge.py` einrichten

1. Datei `ds18b20_bridge.py` in denselben Ordner wie `dashboard.html`
   legen (lokaler Klon des GitHub-Repos auf dem Pi, standardmäßig
   `~/stocksport`, siehe `RASPBERRY_PI_SETUP.md`).
2. `ROOM_SENSOR_ID` und `ASPHALT_SENSOR_ID` mit den in Schritt 3–4
   ermittelten IDs (inkl. `28-` Präfix) eintragen.
3. Git-Push-Zugriff einrichten, falls noch nicht vorhanden:
   ```bash
   cd ~/stocksport
   git remote set-url origin https://<TOKEN>@github.com/DEIN-NUTZERNAME/trainingsportal.git
   ```
   ([Personal Access Token](https://github.com/settings/tokens) erstellen,
   falls noch keins vorhanden.)
4. Testlauf von Hand:
   ```bash
   cd ~/stocksport
   python3 ds18b20_bridge.py
   cat sensors.json
   ```
   Bei Erfolg zeigt `sensors.json` beide Temperaturwerte und einen
   Zeitstempel. Fehler landen zusätzlich in `tuya_bridge.log` im selben
   Ordner (Dateiname historisch, gilt jetzt für dieses Skript).

## 6. Automatisch alle paar Minuten laufen lassen (Cron)

```bash
crontab -e
```

Zeile ergänzen (Beispiel: alle 5 Minuten):

```
*/5 * * * * /usr/bin/python3 /home/pi/stocksport/ds18b20_bridge.py >> /home/pi/stocksport/tuya_bridge.log 2>&1
```

Danach aktualisiert sich `sensors.json` automatisch, wird ins Repo
gepusht, und GitHub Pages liefert die neue Version innerhalb von ein bis
zwei Minuten aus. Der Dashboard-Header zeigt einen ⚠️-Hinweis neben dem
Temperaturwert, wenn der letzte Messwert älter als 20 Minuten ist
(einstellbar über `SENSORS_MAX_AGE_MINUTES` in `dashboard.html`) – so
fällt eine unterbrochene Kabelverbindung oder ein gestoppter Cronjob
sofort auf.

## 7. Kabellänge zur Außenbahn

DS18B20 funktioniert laut Datenblatt zuverlässig bis ca. 20–30 m
Kabellänge (bei gutem Pull-up-Widerstand, ggf. etwas geringer dimensioniert
bei sehr langen Strecken – z. B. 3,3 kΩ statt 4,7 kΩ). Bei deutlich
größeren Entfernungen zwischen Pi und Asphaltbahn ggf. ein
Verlängerungskabel mit Schirmung verwenden oder die Sonde stattdessen
per aktivem Signalverstärker/Repeater anschließen.

## 8. Fehlersuche

- **Kein `28-...`-Eintrag unter `/sys/bus/w1/devices/`**: Verkabelung
  prüfen (Data/VDD/GND vertauscht?), Pull-up-Widerstand vorhanden?
  1-Wire wirklich aktiviert und neu gestartet?
- **`crc=... NO` statt `YES`**: instabile Verbindung – Kabel/Lötstellen
  prüfen, ggf. Pull-up-Widerstand tauschen oder Kabel kürzen. Das Skript
  wiederholt fehlgeschlagene Messungen automatisch dreimal.
- **`t=85000` (also 85 °C) direkt nach dem Einschalten**: normal – das
  ist der Power-on-Reset-Wert des Sensors, bevor die erste echte Messung
  abgeschlossen ist. Verschwindet nach wenigen Sekunden von selbst.
- **`git push` schlägt fehl**: Zugriffsrechte/Token prüfen (Schritt 5.3).
- **Dashboard zeigt dauerhaft „n. v.“**: prüfen, ob `sensors.json` im
  Repo-Root liegt und ob GitHub Pages die neue Version schon ausgeliefert
  hat (`https://DEIN-NUTZERNAME.github.io/trainingsportal/sensors.json`
  direkt im Browser aufrufen).
