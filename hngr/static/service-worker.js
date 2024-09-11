"use strict";

const version = 7;
const cacheName = `hngr-v${version}`;
let isOnline = true;

const urlsToCache = [
  "/",
  "/static/styles.css",
  "/static/base-css/reset.css",
  "/static/script.js",
];

self.addEventListener("install", onInstall);
self.addEventListener("activate", onActivate);
self.addEventListener("message", onMessage);
self.addEventListener("fetch", onFetch);

main().catch(console.error);

async function main() {
  console.log(`Service worker (${version}) is starting`);
  await sendMessage({ requestStatusUpdate: true });
  await cacheFiles({});
}

async function onInstall() {
  console.log(`Service worker (${version}) is installed`);
  self.skipWaiting();
}

async function onActivate(event) {
  event.waitUntil(
    (async () => {
      await clearCaches();
      await cacheFiles({ forceReload: true });
      await clients.claim();
      console.log(`Service worker (${version}) is activated`);
    })(),
  );
}

function onMessage({ data }) {
  console.log("Received message", data);
  if (data.statusUpdate) {
    isOnline = data.statusUpdate.isOnline;
    console.log(
      `Service worker (${version}) statusUpdate, isOnline: ${isOnline}`,
    );
  }
}

function onFetch(event) {
  event.respondWith(router(event.request));
}

async function router(request) {
  const url = new URL(request.url);
  const requestPathname = url.pathname;
  const cache = await caches.open(cacheName);

  // TODO: handle html, js and styles differently?
  if (url.origin == location.origin && request.method === "GET") {
    let response;

    if (isOnline) {
      try {
        response = await fetch(request, {
          method: request.method,
          headers: request.headers,
          cache: "no-store",
        });

        if (response && response.ok) {
          await cache.put(requestPathname, response.clone());
          return response;
        }
      } catch (error) {
        console.error(error);
      }
    }

    response = await cache.match(requestPathname);
    if (response) {
      return response;
    }

    return new Response("", {
      status: 404,
      statusText: "Not found",
    });
  }

  // just pass all other origins through
  return fetch(request);
}

async function sendMessage(message) {
  console.log("Sending message", message);
  const allClients = await clients.matchAll({ includeUncontrolled: true });
  return Promise.all(
    allClients.map((client) => {
      var channel = new MessageChannel();
      channel.port1.onmessage = onMessage;
      client.postMessage(message, [channel.port2]);
    }),
  );
}

async function clearCaches() {
  const cacheNames = await caches.keys();
  const oldCacheNames = cacheNames.filter((name) => {
    if (/^hngr-v\d+$/.test(name)) {
      let [, cacheVersion] = name.match(/^hngr-v(\d+)$/);
      cacheVersion = cacheVersion != null ? Number(cacheVersion) : cacheVersion;
      return cacheVersion && cacheVersion != version;
    }
  });
  return Promise.all(
    oldCacheNames.map((name) => {
      return caches.delete(name);
    }),
  );
}

async function cacheFiles({ forceReload = false }) {
  const cache = await caches.open(cacheName);

  return Promise.all(
    urlsToCache.map(async (url) => {
      try {
        let response;
        if (!forceReload) {
          response = await cache.match(url);
          if (response) {
            return response;
          }
        }

        response = await fetch(url, {
          method: "GET",
          cache: "no-cache",
        });

        if (response.ok) {
          await cache.put(url, response.clone());
        }
      } catch (error) {
        console.error(`Failed to cache ${url} file: ${error}`);
      }
    }),
  );
}
