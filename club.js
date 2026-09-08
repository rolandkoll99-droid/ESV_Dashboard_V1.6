/* =====================================================================
   CLUB.JS – Vereinslogo & Vereinsname für ALLE DREI Module
   (05_Trainingsmodus_Pro.html, 05_Trainingsmodus_Pro_Tablet.html,
   05_Trainingsmodus_Pro_Handy.html) sowie die Startseite (index.html).

   Diese Datei in Visual Studio Code öffnen und die zwei Werte unten
   eintragen - wirkt dann automatisch in der Kopfleiste aller Module
   sowie auf der Startseite.
   ===================================================================== */

const CLUB_CONFIG = {
    // Vereinsname - erscheint neben dem Logo oben in jedem Modul.
    name: "ESV Dimbach",

    // Vereinslogo - Dateiname eines Bildes im "icons"-Ordner (PNG, JPG
    // oder SVG). Eigenes Logo einsetzen:
    //   1. Bilddatei in den Ordner "icons" kopieren, z.B. "icons/logo.png".
    //   2. Den Dateinamen unten eintragen: logo: "icons/logo.png"
    // Bis dahin ist hier ein Platzhalter-Logo eingetragen.
    logo: "icons/icon-513.jpg"
};

// Trägt Vereinsname/-logo in jedes Element mit der Klasse .club-name bzw.
// .club-logo ein - muss nicht angepasst werden.
//
// Falls das eigene Logo NICHT angezeigt wird (nur der Alt-Text/ein "kaputtes
// Bild"-Symbol erscheint), liegt das so gut wie immer daran, dass der Pfad bei
// "logo:" oben nicht exakt zur tatsächlichen Datei passt - z.B. Gross-/
// Kleinschreibung ("Logo.PNG" vs. "logo.png"), eine andere Dateiendung, oder
// die Datei liegt gar nicht im "icons"-Ordner. Der Fehler wird unten
// automatisch in der Browser-Konsole angezeigt (F12 -> Reiter "Console"), mit
// dem exakten Pfad, der nicht gefunden wurde.
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.club-name').forEach(function (el) {
        el.textContent = CLUB_CONFIG.name;
    });
    document.querySelectorAll('.club-logo').forEach(function (el) {
        el.alt = CLUB_CONFIG.name + ' Logo';
        el.onerror = function () {
            console.error(
                '[club.js] Vereinslogo konnte nicht geladen werden: "' + CLUB_CONFIG.logo + '". ' +
                'Bitte pruefen: (1) Liegt die Bilddatei mit GENAU diesem Namen (Gross-/Kleinschreibung ' +
                'zaehlt!) im "icons"-Ordner? (2) Stimmt die Dateiendung (.png/.jpg/.svg)? ' +
                'Bis das behoben ist, wird ersatzweise das Platzhalter-Logo angezeigt.'
            );
            if (el.dataset.fallbackApplied !== '1') {
                el.dataset.fallbackApplied = '1';
                el.src = 'icons/logo-placeholder.svg';
            }
        };
        el.src = CLUB_CONFIG.logo;
    });
    document.title = document.title.replace('ESV Grein', CLUB_CONFIG.name);
});

// ===== APP-INSTALLATION (Service Worker) =====
// Registriert sw.js, damit die App installierbar ist und offline startet.
// Muss nicht angepasst werden (siehe sw.js für Details).
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
        navigator.serviceWorker.register('sw.js').catch(function () { /* z.B. beim Öffnen per Doppelklick (file://) ohne Server - dann läuft die App normal weiter, nur ohne Installierbarkeit/Offline-Cache */ });
    });
}
