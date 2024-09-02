document.body.addEventListener("htmx:beforeOnLoad", function (evt) {
  if ([400, 500].includes(evt.detail.xhr.status)) {
    evt.detail.shouldSwap = true;
    evt.detail.isError = false;
  }
});
