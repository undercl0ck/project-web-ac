(function () {
  var toggle = document.querySelector(".nav-toggle");
  var groups = document.getElementById("nav-groups");
  if (!toggle || !groups) return;

  function drawer() {
    return window.getComputedStyle(toggle).display !== "none";
  }

  function panelFor(button) {
    var id = button.getAttribute("aria-controls");
    return id ? document.getElementById(id) : null;
  }

  function setTrigger(button, open) {
    button.setAttribute("aria-expanded", open ? "true" : "false");
    var panel = panelFor(button);
    if (panel) panel.hidden = !open;
    button.parentNode.classList.toggle("is-open", open);
  }

  function closeTriggers(except) {
    var buttons = groups.querySelectorAll(".menu-trigger");
    Array.prototype.forEach.call(buttons, function (button) {
      if (button !== except) setTrigger(button, false);
    });
  }

  function setDrawer(open) {
    if (!drawer()) return;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    document.body.classList.toggle("nav-open", open);
    if (!open) closeTriggers(null);
  }

  toggle.addEventListener("click", function () {
    var open = toggle.getAttribute("aria-expanded") !== "true";
    setDrawer(open);
    if (open) {
      var first = groups.querySelector("a, button");
      if (first) first.focus();
    } else {
      toggle.focus();
    }
  });

  groups.addEventListener("click", function (event) {
    var button = event.target.closest(".menu-trigger");
    if (!button || !groups.contains(button)) return;
    var open = button.getAttribute("aria-expanded") !== "true";
    closeTriggers(button);
    setTrigger(button, open);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;
    var openTrigger = groups.querySelector('.menu-trigger[aria-expanded="true"]');
    if (openTrigger) {
      setTrigger(openTrigger, false);
      openTrigger.focus();
      return;
    }
    if (drawer() && toggle.getAttribute("aria-expanded") === "true") {
      setDrawer(false);
      toggle.focus();
    }
  });

  window.addEventListener("resize", function () {
    if (!drawer()) {
      document.body.classList.remove("nav-open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Open menu");
    }
  });
})();
(function () {
  var cards = document.querySelectorAll(".icon-card");
  if (!cards.length) return;

  function setOpen(card, open) {
    var button = card.querySelector(".icon-card-toggle");
    if (!button) return;
    card.classList.toggle("is-open", open);
    button.setAttribute("aria-expanded", open ? "true" : "false");
    var link = card.querySelector(".svc-more");
    if (link) {
      if (open) link.removeAttribute("tabindex");
      else link.setAttribute("tabindex", "-1");
    }
  }

  Array.prototype.forEach.call(cards, function (card) {
    var button = card.querySelector(".icon-card-toggle");
    var link = card.querySelector(".svc-more");
    if (link) link.setAttribute("tabindex", "-1");
    if (!button) return;
    button.addEventListener("click", function () {
      setOpen(card, button.getAttribute("aria-expanded") !== "true");
    });
  });

  function openFromHash() {
    var id = (location.hash || "").replace(/^#/, "");
    if (!id) return;
    var node = document.getElementById(id);
    if (!node) return;
    var card = node.classList.contains("icon-card") ? node : node.closest(".icon-card");
    if (!card) return;
    setOpen(card, true);
  }

  openFromHash();
  window.addEventListener("hashchange", openFromHash);
})();
