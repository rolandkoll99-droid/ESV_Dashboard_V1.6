# Trainingsportal auf dem Raspberry Pi (Touch-Monitor / Monitor)

Diese Anleitung geht davon aus, dass das Gesamtpaket **auf GitHub liegt**
und über **GitHub Pages** veröffentlicht ist (siehe README.md, Abschnitt
„So legst du das Projekt auf GitHub an“). Der Pi lädt die Seite dann direkt
von dort – es ist **kein eigener lokaler Webserver auf dem Pi mehr nötig**.

Getestet/empfohlen für **Raspberry Pi OS (64-bit, mit Desktop)** auf
Raspberry Pi 4 oder 5. Ein Pi Zero/1/2 ist für die aufwendigeren Module
(Trainingsanalyse mit Charts) zu schwach.

## 1. GitHub Pages einmalig einrichten

Falls noch nicht geschehen: Repository anlegen, Dateien hochladen, unter
**Settings → Pages** die Veröffentlichung aktivieren (Branch `main`,
Ordner `/ (root)`). Details dazu stehen in der `README.md`. Danach ist die
Seite erreichbar unter:

```
https://DEIN-NUTZERNAME.github.io/trainingsportal/
```

Diese URL verwendest du im Folgenden überall dort, wo `<PAGES-URL>` steht,
und trägst sie außerdem als `GITHUB_PAGES_BASE_URL` in `dashboard.html`
ein (siehe README.md, Abschnitt „QR-Codes im Dashboard“) – nur dann zeigen
die dort platzierten QR-Codes für Trainingsanalyse und Einzeltraining
korrekt auf eine vom Smartphone aus erreichbare Adresse.

## 2. Chromium im Kiosk-Modus automatisch starten

```bash
sudo apt update
sudo apt install -y chromium-browser unclutter
mkdir -p ~/.config/lxsession/LXDE-pi
nano ~/.config/lxsession/LXDE-pi/autostart
```

Datei mit folgendem Inhalt anlegen/ersetzen (URL anpassen!):

```
@xset s off
@xset -dpms
@xset s noblank
@unclutter -idle 0.5 -root
@chromium-browser --noerrdialogs --disable-infobars --kiosk \
  --overscroll-history-navigation=0 --disable-pinch \
  https://DEIN-NUTZERNAME.github.io/trainingsportal/
```

Erklärung der wichtigsten Punkte:
- `xset s off` / `-dpms` / `s noblank` – Bildschirmschoner und
  Energiesparmodus deaktivieren, damit der Monitor nicht abschaltet.
- `unclutter` – blendet den Mauszeiger nach kurzer Inaktivität aus
  (nützlich, auch wenn der Monitor Touch-fähig ist).
- `--kiosk` – echtes Vollbild ohne Adressleiste, ohne Möglichkeit für
  Besucher, die Seite zu verlassen.
- `--disable-pinch` – verhindert versehentliches Auseinanderziehen/
  Verzerren der Ansicht per Touch.

**Kein `--incognito` mehr nötig/empfohlen:** Da die Daten (Spielerliste,
Trainingsergebnisse) ohnehin lokal im `localStorage` des Pi-Browsers
liegen, willst du diese normalerweise über Neustarts hinweg behalten.
Nur wenn der Pi jedes Mal „sauber“ starten soll (z. B. öffentlicher
Verleih-Kiosk), `--incognito` ergänzen.

Danach neu starten: `sudo reboot`

## 3. Wichtig: Internetverbindung ist jetzt Voraussetzung

Da die Seite direkt von GitHub Pages geladen wird, **braucht der Pi eine
funktionierende Internetverbindung** (WLAN oder LAN), um die Seite
überhaupt anzuzeigen. Es gibt aktuell keine Offline-Speicherung
(Service Worker/Cache) im Projekt – bei Verbindungsabbruch zeigt Chromium
eine Fehlerseite, bis die Verbindung zurück ist.

Praxistipps:
- Pi wenn möglich per **LAN-Kabel** statt WLAN anbinden (stabiler in
  Hallen mit vielen Geräten/Störungen).
- WLAN-Verbindung vorab testen: `ping github.io` im Terminal.
- Nach jedem `git push` auf GitHub dauert es (durch GitHub Pages'
  Build-Prozess) üblicherweise ein bis zwei Minuten, bis Änderungen live
  sind – Chromium zeigt bis dahin noch die alte Version.

## 4. Aktualisierungen einspielen

Wenn du am Code etwas änderst und es auf GitHub pushst, holt sich der Pi
die neue Version beim nächsten normalen Neuladen. Da der Kiosk-Modus die
Seite aber nicht automatisch neu lädt, entweder:
- Pi regelmäßig neu starten (z. B. nachts per Cronjob `sudo reboot`), oder
- einen kleinen Auto-Reload-Mechanismus einbauen (z. B. `<meta
  http-equiv="refresh" content="3600">` in `dashboard.html`, falls
  gewünscht – bei Bedarf einfach nachfragen, das lässt sich ergänzen).

## 5. Touch-Monitor kalibrieren (falls nötig)

Die meisten HDMI-Touch-Monitore funktionieren unter Raspberry Pi OS „out of
the box“ (Plug & Play über USB für den Touch-Teil). Falls die Touch-Punkte
nicht exakt sitzen:

```bash
sudo apt install -y xinput-calibrator
xinput_calibrator
```

Die ausgegebenen Werte in `/etc/X11/xorg.conf.d/99-calibration.conf`
eintragen (Anleitung erscheint direkt im Terminal nach dem Kalibrieren).

## 6. Bildschirmauflösung / Ausrichtung

Über `sudo raspi-config` → **Display Options** lässt sich die Auflösung
fix einstellen, falls der Monitor per HDMI nicht automatisch erkannt wird.
Für Hochkant-Montage kann in `/boot/config.txt` `display_rotate=1` (90°)
gesetzt werden – Touch-Eingabe muss dann ggf. per `xinput` mit
transformiert werden (`xinput set-prop … 'Coordinate Transformation Matrix'`).

## 7. Zugriffsschutz & lokale Daten

- Da die Seite jetzt über eine öffentlich erreichbare GitHub-Pages-URL
  läuft (sofern das Repo nicht privat ist), ist der Passwortschutz
  (`index.html`/`login.html`) nicht mehr nur „kosmetisch“ – siehe
  Abschnitt „Wichtiger Hinweis zur Sicherheit“ in der `README.md`. Prüfe,
  ob `PROTECTION_ENABLED` in `auth.js` auf `true` stehen soll, wenn
  Unbefugte die Adresse nicht einfach aufrufen können sollen.
- Spielerliste und Trainingsergebnisse werden weiterhin im `localStorage`
  des jeweiligen Geräts gespeichert, **nicht zentral auf GitHub**. Pi und
  Tablet haben also jeweils ihren eigenen Datenstand, auch wenn beide
  dieselbe GitHub-Pages-Adresse aufrufen. Für einen Abgleich die
  Export-/Import-Funktion (CSV/Excel) in der Spielerverwaltung nutzen.
