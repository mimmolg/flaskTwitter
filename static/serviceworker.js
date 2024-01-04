// Nome della cache
let cacheName = 'pwa01';

// Lista dei file da memorizzare nella cache
let filesToCache = [
    'flaskTwitter/templates/login.html',
    'flaskTwitter/templates/layout.html',
    'flaskTwitter/templates/register.html',
    'flaskTwitter/templates/timeline.html',
    'flaskTwitter/templates/profile.html',
    'flaskTwitter/templates/followers.html',
    'flaskTwitter/templates/following.html',
    'flaskTwitter/templates/hashtag_tweets.html',
    'flaskTwitter/templates/user_profile.html',
    'flaskTwitter/static/hashtag_tweets.css',
    'flaskTwitter/static/like.js',
    'flaskTwitter/static/login.css',
    'flaskTwitter/static/profile.css',
    'flaskTwitter/static/profile.js',
    'flaskTwitter/static/register.css',
    'flaskTwitter/static/timeline.css',
    'flaskTwitter/static/user_profile.css'
];

self.addEventListener('install', function (e) {
        e.waitUntil(
            caches.open(cacheName).then(function (cache) {
                return cache.addAll(filesToCache);
            }).catch(function (error) {
                console.error('Error during service worker installation:', error);
            })
        );
});

self.addEventListener('activate', function () {
    console.log('ServiceWorker activated successfully');
});

self.addEventListener('fetch', function (e) {
    e.respondWith(
        caches.match(e.request).then(function (response) {
            return response || fetch(e.request);
        })
    );
});

