# Trainingsportal auf dem SVITOO P11-T Tablet

Das SVITOO P11-T ist ein 11″-Android-Tablet (Android 16, Unisoc T7250,
4 GB physischer RAM, WLAN 802.11 a/b/g/n/ac) mit einer **Displayauflösung
von 1280×800 Pixel**. Die Website ist bereits so gebaut, dass sie bei dieser
Breite ohne horizontales Scrollen und mit ausreichend großen Touch-Flächen
funktioniert – es ist keine separate „mobile Version“ nötig.

Diese Anleitung geht – wie `RASPBERRY_PI_SETUP.md` – davon aus, dass das
Gesamtpaket **auf GitHub liegt** und über **GitHub Pages** veröffentlicht
ist. Das Tablet greift dann einfach per WLAN/Internet auf dieselbe
Adresse zu wie der Pi – beide Geräte müssen dafür **nicht** im selben
lokalen Netzwerk sein.

## 1. Seite aufrufen

1. Tablet mit WLAN verbinden (Einstellungen → WLAN).
2. **Chrome** öffnen und die GitHub-Pages-Adresse eingeben, z. B.:
   ```
   https://DEIN-NUTZERNAME.github.io/trainingsportal/
   ```

> ⚠️ **Wichtig zur Datenhaltung:** Spielerliste und Trainingsergebnisse
> werden im `localStorage` des jeweiligen **Browsers/Geräts** gespeichert,
> nicht zentral auf GitHub. Pi und Tablet haben also – auch wenn beide
> dieselbe URL aufrufen – jeweils **ihren eigenen Datenstand**. Für einen
> Abgleich die Export-/Import-Funktion (CSV/Excel) in der
> Spielerverwaltung nutzen, oder das Tablet nur als Zweitanzeige ohne
> eigene Dateneingabe verwenden.

## Vollbild / Kiosk-Modus auf dem Tablet

### Einfach: Als Web-App zum Startbildschirm hinzufügen
1. Seite in Chrome öffnen (die GitHub-Pages-Adresse).
2. Menü (⋮) → **„Zum Startbildschirm hinzufügen“**.
3. Von dort startet die Seite ohne Adressleiste, fast wie eine eigene App.

### Für einen echten Kiosk-Betrieb (Gerät nur für das Trainingsportal)
Für ein Gerät, das dauerhaft nur diese Seite zeigen soll und das
Verlassen der App verhindert, empfiehlt sich eine kostenlose Kiosk-Browser-
App aus dem Play Store, z. B. **„Fully Kiosk Browser“**:
1. App installieren, als Start-URL die GitHub-Pages-Adresse eintragen.
2. In den Einstellungen der App: *Kiosk-Modus / „Lock Screen“* aktivieren,
   Bildschirm-Timeout deaktivieren, Startseite beim Hochfahren automatisch
   laden.
3. Optional die App als Standard-Startbildschirm (Launcher) festlegen,
   damit das Tablet nach dem Einschalten direkt in der Seite landet.

### Grundeinstellungen des Tablets
- **Bildschirm-Timeout**: Einstellungen → Display → „Bildschirm-Timeout“
  auf „Nie“/max. Wert stellen (bzw. über die Kiosk-App steuern), damit der
  Monitor während des Trainings nicht abdunkelt.
- **Ausrichtung sperren**: Landscape (Querformat) empfohlen, da die Module
  für 1280×800 im Querformat ausgelegt sind. Schnelleinstellungen →
  Auto-Drehen deaktivieren.
- **WLAN „immer verbunden“**: Einstellungen → WLAN → erweitert →
  „WLAN im Ruhezustand aktiv lassen: Immer“, damit die Verbindung zu
  GitHub Pages nicht abbricht, wenn das Tablet kurz nicht bedient wird.

## Internetverbindung ist Voraussetzung

Da die Seite direkt von GitHub Pages geladen wird, braucht auch das Tablet
eine funktionierende Internetverbindung (WLAN oder mobile Daten). Es gibt
aktuell keine Offline-Speicherung im Projekt. Nach einem `git push` von
Änderungen kann es 1–2 Minuten dauern, bis GitHub Pages die neue Version
ausliefert – erst danach zeigt ein Neuladen der Seite die Änderung.

## Wichtiger Hinweis: Modul „Trainingsmodus Pro“ (05) braucht eine Tastatur

`05_Trainingsmodus_Pro.html` ist bewusst für eine **physische
Zusatztastatur/Nummernblock** gebaut (Eingabetaste, `+`, `-`, `*`, `/`,
`Esc` steuern das Training). Auf einem reinen Touch-Tablet ohne
angeschlossene Tastatur lassen sich diese Kurzbefehle **nicht** auslösen.
Für dieses Modul auf dem Tablet entweder:
- eine kleine **Bluetooth-Tastatur/Nummernblock** mit dem Tablet koppeln, oder
- auf dem Tablet stattdessen die anderen, rein touch-bedienbaren Module
  nutzen (01 Trainingsmodus, 02 Spielerverwaltung, 04 Trainingsanalyse,
  06 Einzeltraining) und „Trainingsmodus Pro“ dem Pi mit angeschlossener
  Tastatur vorbehalten.

## Browser-Empfehlung

Chrome (vorinstalliert) verwenden – nicht ältere/alternative Browser-Apps
aus Drittanbieter-App-Stores, da diese teils veraltete WebView-Versionen
nutzen und moderne Funktionen (z. B. die IndexedDB-Nutzung im Modul
„Trainingsanalyse“) nicht zuverlässig unterstützen.
