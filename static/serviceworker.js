
// Cache name
let cacheName = 'pwa01';

// List of files to be stored in the cache
let filesToCache = [
    'twitterProject/templates/login.html',
    'twitterProject/templates/layout.html',
    'twitterProject/templates/register.html',
    'twitterProject/templates/timeline.html',
    'twitterProject/templates/profile.html',
    'twitterProject/templates/followers.html',
    'twitterProject/templates/following.html',
    'twitterProject/templates/hashtag_tweets.html',
    'twitterProject/templates/user_profile.html',
    'twitterProject/static/hashtag_tweets.css',
    'twitterProject/static/like.js',
    'twitterProject/static/login.css',
    'twitterProject/static/profile.css',
    'twitterProject/static/profile.js',
    'twitterProject/static/register.css',
    'twitterProject/static/timeline.css',
    'twitterProject/static/user_profile.css'
];

// Event listener for service worker installation
self.addEventListener('install', function (e) {
    // Wait until the cache is opened and files are added to it
        e.waitUntil(
            caches.open(cacheName).then(function (cache) {
                return cache.addAll(filesToCache);
            }).catch(function (error) {
                 // Log an error message if installation fails
                console.error('Error during service worker installation:', error);
            })
        );
});

// Event listener for service worker activation
self.addEventListener('activate', function () {
    // Log a success message upon successful activation
    console.log('ServiceWorker activated successfully');
});

// Event listener for fetching resources
self.addEventListener('fetch', function (e) {
    e.respondWith(
         // Check if the requested resource is in the cache
        caches.match(e.request).then(function (response) {
             // Return the cached response if available, otherwise fetch from the network
            return response || fetch(e.request);
        })
    );
});

