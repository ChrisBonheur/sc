var staticCacheName = "spectrecorp-v"; 
var filesToCache = [ 
	'/no_connection/', '/static/images/icons/logo.png', '/static/css/no_connection.css',
	'/static/images/icons/illustration.png'
]; 

self.addEventListener("install", event => { 
	this.skipWaiting(); 
	event.waitUntil( 
		caches.open(staticCacheName) 
			.then(cache => { 
				return cache.addAll(filesToCache); 
			}) 
	) 
}); 

self.addEventListener("fetch", event => { 
	event.respondWith( 
		caches.match(event.request) 
			.then(response => { 
				return response || fetch(event.request); 
			}) 
			.catch(() => { 
				return caches.match('/no_connection/'); 
			}) 
	) 
}); 
