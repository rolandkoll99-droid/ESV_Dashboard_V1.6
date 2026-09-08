# ESV Grein Trainingsportal – eigene App

Dieses Paket macht aus den drei Trainingsmodulen (**Pro**, **Tablet**, **Handy**) eine eigene, installierbare Web-App für den ESV Grein – mit einer zentralen Startseite, eigenem Vereinslogo/-namen und frei einstellbaren Farben, Schriftart und Buttongrößen. Bearbeitet wird alles in **Visual Studio Code**.

## Enthaltene Dateien

| Datei / Ordner | Zweck |
|---|---|
| `index.html` | Startseite mit den drei Kacheln zu den Modulen |
| `05_Trainingsmodus_Pro.html` | Modul 01 – Zuschauermonitor, externer Ziffernblock |
| `05_Trainingsmodus_Pro_Tablet.html` | Modul 02 – Touch-Version für Tablets |
| `05_Trainingsmodus_Pro_Handy.html` | Modul 03 – kompakte Version fürs Smartphone |
| `theme.css` | **Zentrale Design-Datei**: Farben, Schriftart, Buttongrößen für alle drei Module + Startseite |
| `club.js` | **Vereinslogo & Vereinsname** (wirkt auf alle drei Module + Startseite) |
| `manifest.json` | App-Name/-Icon für die Installation (siehe unten) |
| `sw.js` | Service Worker – macht die App installierbar & offline-fähig |
| `icons/` | App-Icons (`icon-192.png`, `icon-512.png`) + Platzhalter-Vereinslogo |
| `vendor/qrcode.min.js` | Bibliothek zur Erzeugung der QR-Codes auf der Startseite (läuft lokal, ohne Internet) |

Alle Dateien müssen im **gleichen Ordner** bleiben, damit die Verlinkung funktioniert.

---

## 1) Farben ändern

Datei **`theme.css`** in VS Code öffnen, Abschnitt „2) FARBEN“. Jede Zeile ist kommentiert, z. B.:

```css
--bg-main:#0a0e14;   /* Seitenhintergrund */
--accent:#33c5ff;    /* Akzentfarbe für Buttons/Auswahl */
--text-main:#eef2f6; /* Haupttext */
```

Einfach den Hex-Code (`#rrggbb`) ändern, Datei speichern, Seite im Browser neu laden – die Änderung wirkt automatisch auf **alle drei Module gleichzeitig**, es muss nichts in den einzelnen Modul-Dateien gesucht werden.

> Die Mannschaftsfarben (`--w-color` / `--e-color`) sind der Startwert. In den Modulen **Pro** und **Tablet** lassen sie sich zusätzlich direkt in der App pro Training umschalten (Leuchtgrün RAL 6038 / Leuchtrot RAL 3024, über die Buttons neben den Mannschaftsnamen) – wählt eine Mannschaft eine Farbe, bekommt die andere automatisch die verbleibende zugewiesen.

## 2) Schriftart ändern

Ebenfalls in `theme.css`, ganz oben, Abschnitt „1) SCHRIFTART“:

1. Auf [fonts.google.com](https://fonts.google.com) die gewünschte Schriftart suchen → **„Get font“** → **„Get embed code“** → den `@import`-Link kopieren.
2. Die vorhandene `@import url(...)`-Zeile ganz oben in `theme.css` durch den neuen Link ersetzen.
3. Die Namen in `--font-display` (Überschriften) und `--font-body` (Fließtext) entsprechend anpassen.

## 3) Vereinslogo & Vereinsname ändern

Datei **`club.js`** öffnen:

```js
const CLUB_CONFIG = {
    name: "ESV Grein",
    logo: "icons/logo-placeholder.svg"
};
```

- **Name**: einfach den Text zwischen den Anführungszeichen ändern.
- **Logo**: eigene Bilddatei (PNG/JPG/SVG, am besten quadratisch) in den Ordner `icons` kopieren, z. B. `icons/logo.png`, und den Dateinamen bei `logo:` eintragen.

Das Logo erscheint danach automatisch in der Kopfleiste aller drei Module sowie oben auf der Startseite.

> **Falls das Logo nicht angezeigt wird** (nur der Alt-Text „ESV Grein Logo“ bzw. ein „kaputtes Bild“-Symbol erscheint): Das liegt so gut wie immer daran, dass der Pfad bei `logo:` nicht **exakt** zur tatsächlichen Datei im `icons`-Ordner passt. Häufigste Ursachen:
> 1. **Gross-/Kleinschreibung** – `icons/Logo.PNG` ist nicht dasselbe wie `icons/logo.png`. Der eingetragene Pfad muss zeichengenau mit dem echten Dateinamen übereinstimmen.
> 2. **Falsche Dateiendung** – die Datei heisst z. B. wirklich `.jpeg`, im Code steht aber `.jpg` (oder umgekehrt).
> 3. **Datei liegt nicht im `icons`-Ordner** – ggf. beim Kopieren versehentlich in einen anderen Ordner gelegt.
>
> Zur Kontrolle: Seite im Browser öffnen, **F12** drücken (Entwicklertools) → Reiter **„Console“**. Dort erscheint jetzt automatisch eine genaue Fehlermeldung mit dem exakten Pfad, der nicht gefunden wurde – bis das behoben ist, wird übergangsweise wieder das Platzhalter-Logo angezeigt, damit nie ein „kaputtes Bild“-Symbol sichtbar ist.

## 4) Buttongrößen anpassen

Ebenfalls in `theme.css`, Abschnitt „3) BUTTONGRÖSSEN“. Für jedes Modul gibt es einen eigenen Skalierungsfaktor:

```css
--btn-scale-pro: 1;
--btn-scale-tablet: 1;
--btn-scale-handy: 1;
```

`1` = Standardgröße, `1.2` = 20 % größer, `0.8` = 20 % kleiner. Der Faktor wirkt auf die Haupt-Buttons (Kopf- und Fußzeile) sowie – bei Tablet und Handy – auf den Bildschirm-Ziffernblock. Sinnvoller Bereich: etwa `0.8`–`1.6`. Auf sehr kleinen Bildschirmen greifen zusätzlich automatische Verkleinerungen, damit nichts abgeschnitten wird.

---

## 5) Als eigene App bereitstellen (installierbar)

Diese App lässt sich – wie z. B. eine App aus dem Store – auf Tablet, Handy oder Desktop **installieren** (eigenes Icon, startet im Vollbild ohne Browserleiste, funktioniert auch offline). Dafür sind zwei Dinge nötig:

### a) App-Icon festlegen

Das Icon fürs Homescreen/Startmenü kommt aus `icons/icon-192.png` und `icons/icon-512.png` (aktuell ein Platzhalter mit „ESV“). Eigenes Icon einsetzen:

1. Ein quadratisches Vereinslogo als PNG in zwei Größen bereitstellen: 192×192 Pixel und 512×512 Pixel (z. B. mit einem kostenlosen Tool wie [realfavicongenerator.net](https://realfavicongenerator.net) oder [appicon.co](https://appicon.co) aus einem großen Logo erzeugen lassen).
2. Die beiden Dateien in den Ordner `icons` legen und **exakt** `icon-192.png` bzw. `icon-512.png` nennen (bestehende Platzhalter-Dateien überschreiben).
3. Optional in `manifest.json` den Namen anpassen (`name`, `short_name`) – dieser erscheint unter dem Icon auf dem Homescreen.

> Technischer Hinweis: Das App-Icon kann – anders als Logo/Name in der App selbst – nicht automatisch aus `club.js` übernommen werden, da Betriebssysteme dafür fertige Bilddateien in festen Größen benötigen.

### b) Die App online bereitstellen

Ein Service Worker (für Installierbarkeit & Offline-Nutzung) funktioniert nur, wenn die Seite über **http(s)** aufgerufen wird – nicht per Doppelklick auf die Datei (`file://`). Zwei gängige, kostenlose Wege:

**Variante 1 – GitHub Pages (empfohlen, kostenlos):**
1. Kostenloses GitHub-Konto anlegen, neues Repository erstellen.
2. Alle Dateien dieses Ordners hochladen (per Drag & Drop im Browser oder mit Git).
3. Unter *Settings → Pages* die Veröffentlichung aktivieren (Branch `main`, Ordner `/root`).
4. Nach kurzer Zeit ist die App unter `https://<benutzername>.github.io/<repository-name>/` erreichbar.

**Variante 2 – jeder andere Web-Hoster**, der statische HTML-Dateien ausliefert (z. B. Netlify, ein bestehender Vereins-Webspace). Einfach den kompletten Ordnerinhalt hochladen.

### c) App installieren

Die veröffentlichte Adresse (z. B. die GitHub-Pages-URL) auf dem gewünschten Gerät im Browser öffnen:

- **Android (Chrome)**: Menü (⋮) → „App installieren“ bzw. „Zum Startbildschirm hinzufügen“.
- **iPhone/iPad (Safari)**: Teilen-Symbol → „Zum Home-Bildschirm“.
- **Windows/Mac (Chrome/Edge)**: Klick auf das Installieren-Symbol in der Adressleiste.

Die App startet danach mit eigenem Icon im Vollbild, ganz ohne Browserleiste.

---

## 6) QR-Codes fürs eigene Gerät

Auf der Startseite (`index.html`) sind unter „📱 Eigenes Gerät verbinden“ zwei QR-Codes eingeblendet – einer für **Trainingsmodus Tablet**, einer für **Trainingsmodus Handy**. Bringt ein Mitspieler sein eigenes Tablet oder Smartphone mit, reicht ein Scan mit der Handykamera, um direkt im passenden Modul zu landen – ohne Adresse abtippen zu müssen.

Die Codes werden **automatisch** aus der Adresse gebildet, unter der `index.html` gerade aufgerufen wird – es ist **keine Konfiguration nötig**. Sobald die App auf GitHub Pages (oder einem anderen Hoster) liegt, zeigen die Codes von selbst auf die richtige Adresse dort. Lokal per Doppelklick (`file://`) angezeigt, funktionieren die Codes nicht zum Scannen (das steht dann auch so als Adresse darunter) – für einen echten Test siehe Abschnitt 7 unten.

> Modul **Pro** hat bewusst keinen eigenen QR-Code, da es als Zuschauermonitor für den gemeinsamen Bildschirm gedacht ist, nicht fürs eigene Gerät.

---

## 7) Lokal in VS Code testen

Farben/Schrift/Logo lassen sich auch einfach per Doppelklick auf `index.html` im Browser testen. Für einen vollständigen Test inkl. Installierbarkeit/Offline-Funktion empfiehlt sich die kostenlose VS-Code-Erweiterung **„Live Server“**:

1. Erweiterung „Live Server“ (Ritwick Dey) in VS Code installieren.
2. Rechtsklick auf `index.html` → **„Open with Live Server“**.
3. Der Browser öffnet die App über `http://127.0.0.1:...` – jetzt funktionieren auch Installierbarkeit und Offline-Cache wie später online.

> Tipp zum Testen der QR-Codes ohne GitHub: Live Server zeigt meist auch eine Netzwerk-Adresse wie `http://192.168.x.x:5500` an (bzw. über „Go Live“ unten in der Statusleiste einsehbar). Ruft man `index.html` über diese Adresse statt über `127.0.0.1` auf, sind die QR-Codes von jedem Handy im selben WLAN aus scannbar.

## Hinweis

Alle drei Module funktionieren technisch weiterhin unabhängig voneinander (können auch einzeln geöffnet werden) – `theme.css` und `club.js` sorgen lediglich dafür, dass Design und Branding an einer zentralen Stelle gepflegt werden.
