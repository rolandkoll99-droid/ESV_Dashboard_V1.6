/* =====================================================================
   SW.JS – Service Worker für die installierbare Web-App.
   Sorgt dafür, dass die App nach dem ersten Öffnen auch ohne
   Internetverbindung startet (App-Shell-Cache) und beim Installieren
   aufs Homescreen/Startmenü ein eigenes Icon bekommt.

   Muss normalerweise NICHT angepasst werden. Einzige Ausnahme: Wird
   eine neue Datei zum Projekt hinzugefügt (z.B. ein zweites Logo-Bild),
   sollte sie unten in APP_SHELL ergänzt werden, damit sie auch offline
   verfügbar ist. Nach inhaltlichen Änderungen an den HTML/CSS/JS-Dateien
   CACHE_NAME hochzählen (z.B. 'v2'), damit installierte Apps die neue
   Version laden statt eine alte aus dem Cache zu zeigen.
   ===================================================================== */

const CACHE_NAME = 'esv-grein-app-v2';

const APP_SHELL = [
    './',
    './index.html',
    './theme.css',
    './club.js',
    './manifest.json',
    './05_Trainingsmodus_Pro.html',
    './05_Trainingsmodus_Pro_Tablet.html',
    './05_Trainingsmodus_Pro_Handy.html',
    './vendor/qrcode.min.js',
    './icons/icon-192.png',
    './icons/icon-512.png',
    './icons/logo-placeholder.svg'
];

self.addEventListener('install', function (event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function (cache) { return cache.addAll(APP_SHELL); })
            .catch(function () { /* z.B. kein Internet beim allerersten Aufruf - kein Problem */ })
    );
    self.skipWaiting();
});

self.addEventListener('activate', function (event) {
    event.waitUntil(
        caches.keys().then(function (keys) {
            return Promise.all(keys.filter(function (k) { return k !== CACHE_NAME; }).map(function (k) { return caches.delete(k); }));
        })
    );
    self.clients.claim();
});

// Strategie: erst aus dem Cache antworten (sofort startbereit, auch offline),
// im Hintergrund parallel die aktuelle Version nachladen und für das nächste
// Mal im Cache aktualisieren ("stale-while-revalidate").
self.addEventListener('fetch', function (event) {
    if (event.request.method !== 'GET') return;
    event.respondWith(
        caches.match(event.request).then(function (cached) {
            const networkFetch = fetch(event.request).then(function (response) {
                if (response && response.ok) {
                    const clone = response.clone();
                    caches.open(CACHE_NAME).then(function (cache) { cache.put(event.request, clone); });
                }
                return response;
            }).catch(function () { return cached; });
            return cached || networkFetch;
        })
    );
});
