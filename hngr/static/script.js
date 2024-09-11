"use strict";

let isOnline = "onLine" in navigator ? navigator.onLine : true;
let swRegistration;
let sw;

registerServiceWorker();
setupHtmx();
ready();

async function registerServiceWorker() {
  if ("serviceWorker" in navigator) {
    try {
      const registration = await navigator.serviceWorker.register(
        "/service-worker.js",
        { updateViaCache: "none", scope: "/" },
      );

      sw =
        registration.installing || registration.waiting || registration.active;
      sendStatusUpdate(sw);

      navigator.serviceWorker.addEventListener("controllerchange", () => {
        sw = navigator.serviceWorker.controller;
        sendStatusUpdate(sw);
      });

      navigator.serviceWorker.addEventListener("message", (event) => {
        console.log("onMessage");
        var { data } = event;
        if (data.requestStatusUpdate) {
          sendStatusUpdate(event.ports && event.ports[0]);
        }
      });
    } catch (error) {
      console.error(`Service worker registration failed: ${error}`);
    }
  }
}

function setupHtmx() {
  document.body.addEventListener("htmx:beforeOnLoad", function (evt) {
    if ([400, 500].includes(evt.detail.xhr.status)) {
      evt.detail.shouldSwap = true;
      evt.detail.isError = false;
    }
  });
}

async function ready() {
  if (!isOnline) {
    console.log("You are offline");
  } else {
    console.log("You are back online! Yay!");
  }

  window.addEventListener("online", () => {
    console.log("online");
    isOnline = true;
    sendStatusUpdate();
  });

  window.addEventListener("offline", () => {
    console.log("offline");
    isOnline = false;
    sendStatusUpdate();
  });
}

function sendStatusUpdate(target) {
  console.log("sendStatusUpdate");
  sendSwMessage({ statusUpdate: { isOnline } }, target);
}

function sendSwMessage(message, target) {
  console.log("sendSwMessage", message, target);
  if (target) {
    target.postMessage(message);
  } else if (sw) {
    sw.postMessage(message);
  } else {
    navigator.serviceWorker.controller.postMessage(message);
  }
}
