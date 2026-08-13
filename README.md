# Trainingsportal

Statische Website mit Passwortsperre, Login, Dashboard und 5 Trainingsmodulen.

## Design

Einheitliches Grün/Gold-Theme über alle Seiten, angelehnt an das
Dashboard-Design (`chrome.css`): dunkelgrüner Verlauf im Hintergrund,
grüne Kopfleiste mit ESV-Grein-Logo auf jeder Seite, Gold (`#ffdf8c`) als
Akzentfarbe, „Space Grotesk" für Überschriften und „Inter" als
Fließtext-Schrift. Jede Modulseite hat eine grüne Kopfleiste mit Link
zurück zum Dashboard und einem Abmelden-Button.

Die weißen Inhaltskarten (Tabellen, Ranking, Analyse-Ansicht, Kehren-Grid)
in den Modulen wurden bewusst beibehalten, da sie für die Lesbarkeit von
Daten wichtig sind – nur der äußere Rahmen (Kopfzeile, Hintergrundfarbe)
wurde an das neue Theme angepasst. Team- bzw. bahnspezifische Farben
(Grün/Rot für Mannschaften, Blau für „Bahn 1") sind funktional und wurden
nicht verändert.

**Hinweis zu Dark Mode:** Der Dark-Mode-Umschalter (🌓) im Dashboard
wirkt aktuell auf Header, Hintergrund und die Dashboard-eigenen Karten.
Die internen weißen Karten/Tabellen der einzelnen Module (01, 02, 04, 05,
06) reagieren derzeit nicht auf den Dark-Mode-Schalter – das wäre ein
größerer separater Umbau jeder einzelnen Moduldatei.

## Smartphone-Nutzung (Querformat)

Alle Seiten (Dashboard + die 5 Module) sind für die Bedienung am
Smartphone **im Querformat** optimiert:

- Bei kurzen Bildschirmhöhen (typisch für ein liegendes Handy, z. B.
  360–430 px hoch) greift eine eigene Kompakt-Ansicht: kleinerer Header,
  kleinere Kacheln, ausgeblendete Beschreibungstexte – damit möglichst
  viel ohne Scrollen sichtbar ist. Passt dennoch nicht alles auf den
  Bildschirm, kann innerhalb der weißen Karte gescrollt werden (vorher
  war das durch `overflow: hidden` blockiert – behoben).
- Wird das Handy **hochkant** gehalten (schmal und hoch), erscheint ein
  Hinweis „Bitte das Gerät ins Querformat drehen“, da die App für die
  Bedienung im Querformat ausgelegt ist.

Getestet wurde dies bislang nur mit den Browser-Entwicklertools
(Chrome-Gerätesimulation); ein Test auf echten Geräten unterschiedlicher
Displaygrößen wird empfohlen, bevor es im Vereinsbetrieb eingesetzt wird.

## Dateien

```
index.html                     Passwortschutz (Zugangscode-Eingabe)
login.html                     Login (Benutzername + Passwort)
dashboard.html                 Übersicht / Startseite nach dem Login
01_Trainingsmodus.html         Modul 1: Freies Training ohne Zeitdruck
05_Trainingsmodus_Pro.html     Modul 2: Freies Training mit Zusatztastatur
04_Trainingsanalyse.html       Modul 3: Trainingsanalyse / Auswertung
06_Einzeltraining.html         Modul 4: Einzeltraining mit Anleitung
02_Spielerverwaltung.html      Modul 5: Verwaltung der Spielerprofile
02_Spielerliste.xlsx           Beispiel-/Vorlagendatei für den Excel-Import
style.css                      gemeinsames Design (Basistheme für Zugang/Login)
chrome.css                     Design des Dashboards (Header, Arena-Karte, Menü-/QR-Karten, Dark Mode)
chrome.js                      Dark-Mode-Toggle & Toast-Funktion für das Dashboard
auth.js                        zentrale, einfache Zugriffslogik (Passwort, Login, Logout)
qrcode.min.js                  QR-Code-Bibliothek (MIT-lizenziert, ohne Abhängigkeiten) für
                                die QR-Codes im Dashboard
ds18b20_bridge.py              Hintergrund-Skript für den Pi: liest zwei DS18B20-Tauchsonden
                                (Raum + Asphalt) über 1-Wire aus und schreibt sensors.json
                                (siehe RASPBERRY_PI_SENSOREN_SETUP.md)
sensors.json                   aktuelle Raum-/Asphalttemperatur fürs Dashboard (wird von
                                tuya_bridge.py automatisch überschrieben)
Defensiv Basis.jpg             Situationsbilder für das Einzeltraining
Defensiv Elite.jpg
Offensiv Basic.jpg
Offensiv Elite.jpg
```

Hinweis: Die Modulnummern in den Dateinamen sind historisch gewachsen und
entsprechen nicht der Reihenfolge im Dashboard – im Dashboard sind alle
fünf Module unter sprechenden Titeln (01–05) verlinkt.

## So legst du das Projekt auf GitHub an

1. **Repository erstellen**
   Auf github.com oben rechts auf **+ → New repository** klicken. Namen vergeben
   (z. B. `trainingsportal`), auf **Create repository** klicken.

2. **Dateien hochladen**
   Im leeren Repo auf **uploading an existing file** klicken (oder „Add file → Upload files“)
   und alle Dateien aus diesem Ordner per Drag-and-drop hochladen. Danach unten
   **Commit changes** klicken.

   Alternativ per Git auf der Kommandozeile:
   ```bash
   git init
   git add .
   git commit -m "Erste Version Trainingsportal"
   git branch -M main
   git remote add origin https://github.com/DEIN-NUTZERNAME/trainingsportal.git
   git push -u origin main
   ```

3. **GitHub Pages aktivieren** (damit die Seite im Browser aufrufbar ist)
   Im Repo auf **Settings → Pages**. Unter „Build and deployment“ als Source
   **Deploy from a branch** wählen, Branch `main` und Ordner `/ (root)` auswählen,
   **Save** klicken. Nach ein bis zwei Minuten ist die Seite unter
   `https://DEIN-NUTZERNAME.github.io/trainingsportal/` erreichbar.

4. **Zugangsdaten anpassen**
   In `auth.js` die Werte `SITE_PASSWORD`, `VALID_USER.user` und `VALID_USER.pass`
   ändern und die Datei erneut committen/pushen.

## Wichtiger Hinweis zur Sicherheit

Der Passwortschutz in `auth.js` läuft **komplett im Browser** (clientseitig).
Das Passwort steht im Klartext im Quellcode und kann von jedem, der die Seite
aufruft, im „Seitenquelltext anzeigen“ ausgelesen werden. Das reicht, um
neugierige Besucher fernzuhalten, ist aber **kein echter Zugriffsschutz** für
vertrauliche Inhalte.

Für echten Schutz gibt es zwei gängige Wege:
- **GitHub Pages bleibt öffentlich, aber mit echtem Login:** Statt reinem HTML
  ein Hosting mit serverseitiger Logik verwenden, z. B. Cloudflare Pages +
  Cloudflare Access, oder Netlify mit Netlify Identity.
- **Repository privat halten:** GitHub Pages kann auch aus einem privaten
  Repository veröffentlicht werden (bei GitHub Pro/Team/Enterprise, oder als
  privates Deployment über Vercel/Netlify), sodass nur eingeladene Personen
  überhaupt Zugriff auf den Code haben.

## Betrieb auf Raspberry Pi & Tablet (Kiosk-Modus, über GitHub Pages)

Das aktuelle Betriebskonzept: Das Gesamtpaket liegt auf GitHub und wird über
**GitHub Pages** veröffentlicht. Sowohl der Raspberry Pi (Touch-Monitor) als
auch das SVITOO P11-T Tablet greifen als reine Clients per Browser auf
dieselbe GitHub-Pages-Adresse zu – ein eigener lokaler Webserver ist dafür
nicht nötig. Eigene Schritt-für-Schritt-Anleitungen:

- [`RASPBERRY_PI_SETUP.md`](RASPBERRY_PI_SETUP.md) – Chromium-Kiosk-Modus
  gegen die GitHub-Pages-URL, Touch-Kalibrierung, Autostart,
  Internetabhängigkeit.
- [`TABLET_SVITOO_P11-T_SETUP.md`](TABLET_SVITOO_P11-T_SETUP.md) – Zugriff
  per WLAN auf dieselbe GitHub-Pages-URL, Vollbild/Kiosk-Modus, wichtiger
  Hinweis zum Modul „Trainingsmodus Pro“ (benötigt Tastatur).

**Zu beachten:** Beide Geräte müssen für den Zugriff online sein
(Internetverbindung nötig), und jedes Gerät hat seinen **eigenen**
lokalen Datenstand (`localStorage`) für Spielerliste/Trainingsergebnisse –
dazu mehr im Abschnitt „Wichtiger Hinweis zur Sicherheit“ unten sowie in
den beiden Anleitungen.

- [`RASPBERRY_PI_SENSOREN_SETUP.md`](RASPBERRY_PI_SENSOREN_SETUP.md) – Raum-
  und Asphalttemperatur per kabelgebundener DS18B20-Tauchsonde im
  Dashboard anzeigen. Die Sonden hängen direkt per 1-Wire am Pi (kein
  WLAN, keine Cloud, kein API-Key nötig), das Hintergrund-Skript
  `ds18b20_bridge.py` liest sie aus und schreibt die Werte in
  `sensors.json`, das automatisch ins GitHub-Repo gepusht wird.
- [`SUPABASE_SETUP.md`](SUPABASE_SETUP.md) – **neu:** zentrale
  Temperatur-Historie statt nur Momentaufnahme. Das Dashboard zeigt einen
  48-Stunden-Verlauf, gespeist aus einer kleinen, kostenlosen
  Supabase-Datenbank (sicherer Lesezugriff für den Browser, Schreibzugriff
  nur vom Pi). Baut auf `RASPBERRY_PI_SENSOREN_SETUP.md` auf. Siehe auch
  `ROADMAP.md` für den größeren Zusammenhang.

## Kehren-Eingabe in „Trainingsmodus" (01)
Die Eingabe der Kehren-Ergebnisse wurde überarbeitet: Statt in jeder
Kehren-Zeile einzeln auf einen Punktwert zu tippen, gibt es jetzt eine
kombinierte Ergebnistabelle (Kehre / Team W / Team E / Aktionen) und
darunter ein **Schnell-Eingabe-Panel** nur für die gerade aktive Kehre –
Wert für beide Teams auswählen (mit Tausch-Button ⇄ bei Verwechslung),
dann „Kehre speichern" oder „Kehre abbrechen". Bereits gespielte Kehren
lassen sich über die Stift-/Papierkorb-Icons in der Tabelle nachträglich
bearbeiten oder löschen. Zusätzlich große, gut lesbare Gesamt-Ergebnis-
Anzeige mit Spielnummer und Status („Läuft"/„Beendet") oben in der Karte.

**Hinweis:** Der zweite Tab „Schüsse (Detailmodus)“ ist aktuell nur ein
Platzhalter (zeigt einen Hinweis-Toast) – eine Einzelschuss-Erfassung pro
Kehre gibt es noch nicht, das wäre ein eigenes, größeres Feature.

## Kehren-Eingabe in „Trainingsmodus Pro" (05)

Dieselbe Tabellen-/Schnell-Eingabe-Bedienung wie in „Trainingsmodus" (01)
wurde auch hier ergänzt – **die Tastatur-/Zusatztastatur-Bedienung bleibt
dabei vollständig erhalten** und funktioniert unverändert wie zuvor
(`-`/`+` Team wählen, `1`–`6` Spieler/Punktwert, `*` Löschmodus, `Enter`
Wertung, `/` Zuschauermonitor). Touch-Eingabe (Tabelle mit
Bearbeiten-/Löschen-Icons + Schnell-Eingabe-Panel) und Tastatur schreiben
in dieselben Daten und bleiben synchron: eine Tastatur-Eingabe setzt eine
noch nicht gespeicherte Touch-Auswahl automatisch zurück, damit die
Anzeige nie auseinanderläuft. Aufstellungs-Panels (Spielerauswahl je
Team), Spielerverwaltung und Zuschauermonitor sind unverändert.

## „Schüsse"-Tab: Spielserie & PDF-Export (01 & 05)

Der bisher als Platzhalter angelegte „Schüsse"-Tab ist jetzt eine echte
**Spielserien-Übersicht**: Jedes abgeschlossene Spiel (inkl. aller
Kehren-Ergebnisse, Uhrzeit und Endergebnis) wird gesammelt, solange das
Training läuft – bisher wurden diese Daten beim Start des nächsten
Spiels einfach überschrieben. Über den Button „📄 Als PDF exportieren /
Drucken" lässt sich die komplette Serie ausdrucken bzw. über den
Druckdialog des Browsers als PDF speichern (kein zusätzliches
Plugin/keine externe Bibliothek nötig – „Als PDF speichern" ist in jedem
modernen Browser bereits im Druckdialog enthalten).

Die Historie ist an die laufende Trainingsserie gebunden und wird bei
„Neues Spiel Starten" bzw. „Kompletter Reset" zusammen mit den übrigen
Werten zurückgesetzt (neue Serie = neue Historie, neues Startdatum).

## Roadmap

Ein priorisierter Überblick über sinnvolle nächste Verbesserungen
(Software, Hardware, Sensorik) inkl. Umsetzungsstatus steht in
[`ROADMAP.md`](ROADMAP.md).

## Struktur erweitern

Jede Modulseite hat denselben Grundaufbau: eine Topbar mit Link zurück zum
Dashboard und einem Abmelden-Button, eine Titelzeile sowie eine Karte für den
Inhalt. Eigene Inhalte einfach in die `<div class="card">` (bzw. das
entsprechende Hauptcontainer-Element) der jeweiligen Datei einfügen.

Neue Module bindest du wie folgt ein:
1. HTML-Datei nach dem bestehenden Muster anlegen (Topbar mit
   `<a href="dashboard.html">&larr; Zurück zum Dashboard</a>` und
   `<a class="logout" href="#" onclick="logout(); return false;">Abmelden</a>`).
2. `auth.js` einbinden und `requireGate(); requireLogin();` aufrufen, damit das
   Modul denselben Zugriffsschutz wie die anderen Seiten nutzt.
3. Eine neue Kachel in `dashboard.html` im `<div class="grid">` ergänzen.

## Zugriffsschutz an/aus

In `auth.js` steuert die Konstante `PROTECTION_ENABLED`, ob Passwortschutz und
Login aktiv sind:
- `true` – Zugangscode (`index.html`) und Login (`login.html`) sind Pflicht.
- `false` – alle Seiten sind frei zugänglich, `index.html` und `login.html`
  leiten automatisch zum Dashboard weiter. Das ist der aktuelle Zustand
  (praktisch für Entwicklung/Tests, siehe Sicherheitshinweis unten).

## Wetter-Anzeige im Dashboard

Das Dashboard zeigt optional das aktuelle Wetter über die OpenWeatherMap-API
an (`WEATHER_API_KEY`/`WEATHER_LOCATION` in `dashboard.html`). Ohne gültigen
Key wird automatisch ein einfacher Platzhalterwert (Tag/Nacht-Schätzung)
angezeigt. Der aktuell hinterlegte Key ist im Quelltext sichtbar – für den
produktiven Einsatz empfiehlt es sich, den Key in den OpenWeatherMap-
Einstellungen auf die eigene Domain zu beschränken oder einen eigenen Key
einzutragen.

## QR-Codes im Dashboard (Smartphone-Zugriff)

Das Dashboard zeigt zwei QR-Codes, mit denen Spieler per Smartphone direkt
zu **Trainingsanalyse** (`04_Trainingsanalyse.html`) und **Einzeltraining**
(`06_Einzeltraining.html`) springen können. Die Codes werden clientseitig
per `qrcode.min.js` erzeugt.

**Wichtig – vor dem ersten Einsatz einmalig einrichten:** In `dashboard.html`
die Konstante `GITHUB_PAGES_BASE_URL` auf deine echte GitHub-Pages-Adresse
setzen:

```js
const GITHUB_PAGES_BASE_URL = 'https://DEIN-NUTZERNAME.github.io/trainingsportal/';
```

Damit zeigen die QR-Codes **immer** auf die öffentlich erreichbare
GitHub-Pages-Adresse – unabhängig davon, ob das Dashboard gerade lokal
getestet, über die WLAN-IP des Pi oder direkt über GitHub Pages aufgerufen
wird. Das ist wichtig, weil ein Smartphone beim Scannen nur eine öffentlich
erreichbare Adresse aufrufen kann; die IP eines lokalen Testservers würde
vom Handy aus ins Leere laufen. Solange der Platzhalter
`DEIN-NUTZERNAME` nicht ersetzt ist, verwenden die QR-Codes ersatzweise die
aktuell aufgerufene Adresse (praktisch nur für schnelle lokale Tests).

**Wichtige Einschränkung:** Trainingsergebnisse in der Trainingsanalyse
werden lokal je Gerät gespeichert (`localStorage`/IndexedDB, siehe
Abschnitt „Betrieb auf Raspberry Pi & Tablet“). Scannt ein Spieler den
QR-Code für die Trainingsanalyse mit seinem eigenen Handy, sieht er dort
**nicht** die am Kiosk-Gerät (Pi/Tablet) erfassten Trainingsdaten, sondern
den (in der Regel leeren) Datenstand seines eigenen Handy-Browsers. Für
das Modul „Einzeltraining“ ist das unproblematisch, da es überwiegend
feste Trainingsinhalte (Bilder, Regeln) ohne personenbezogene Ergebnisse
zeigt. Wer die Trainingsanalyse-Ergebnisse tatsächlich geräteübergreifend
sichtbar machen möchte, bräuchte einen zentralen Speicher (z. B. ein
kleines Backend oder einen Cloud-Dienst) – bei Bedarf gerne ansprechen,
das ist ein größeres separates Vorhaben.
