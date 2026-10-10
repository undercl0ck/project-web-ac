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
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)");

  function cardOf(node) {
    if (!node || !node.closest) return null;
    return node.classList && node.classList.contains("icon-card") ? node : node.closest(".icon-card");
  }

  function waitMs() {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches ? 0 : 120;
  }

  Array.prototype.forEach.call(cards, function (card) {
    card.addEventListener("pointerenter", function () {
      if (!fine.matches) return;
      clearTimeout(card._hotTimer);
      card._hotTimer = setTimeout(function () {
        if (!card.classList.contains("is-suppressed")) card.classList.add("is-hot");
      }, waitMs());
    });
    card.addEventListener("pointerleave", function () {
      clearTimeout(card._hotTimer);
      card.classList.remove("is-hot");
      card.classList.remove("is-suppressed");
    });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape" || !fine.matches) return;
    var hovered = null;
    Array.prototype.forEach.call(cards, function (card) {
      if (card.matches(":hover")) hovered = card;
    });
    var focused = cardOf(document.activeElement);
    var card = focused || hovered;
    if (!card) return;
    clearTimeout(card._hotTimer);
    card.classList.remove("is-hot");
    card.classList.add("is-suppressed");
    if (focused && document.activeElement && card.contains(document.activeElement)) {
      document.activeElement.blur();
    }
  });

  document.addEventListener("focusin", function (event) {
    var card = cardOf(event.target);
    if (card) card.classList.remove("is-suppressed");
  });

  function openFromHash() {
    var id = (location.hash || "").replace(/^#/, "");
    if (!id) return;
    var node = document.getElementById(id);
    var card = cardOf(node);
    if (!card) return;
    card.classList.remove("is-suppressed");
    card.classList.add("is-open");
  }

  openFromHash();
  window.addEventListener("hashchange", openFromHash);

  function lockRows() {
    Array.prototype.forEach.call(document.querySelectorAll(".svc-grid"), function (grid) {
      var items = grid.querySelectorAll(".icon-card");
      Array.prototype.forEach.call(items, function (card) {
        card.style.minHeight = "";
        var article = card.querySelector(".card");
        if (article) article.style.minHeight = "";
      });
      if (!fine.matches) return;
      var rows = [];
      Array.prototype.forEach.call(items, function (card) {
        var top = Math.round(card.getBoundingClientRect().top);
        var row = rows.length && Math.abs(rows[rows.length - 1].top - top) < 2 ? rows[rows.length - 1] : null;
        if (!row) {
          row = { top: top, items: [] };
          rows.push(row);
        }
        var article = card.querySelector(".card");
        var panel = card.querySelector(".icon-card-panel");
        var border = article ? parseFloat(getComputedStyle(article).borderTopWidth) || 0 : 0;
        var square = Math.round(card.getBoundingClientRect().width);
        var openH = Math.max(square, Math.ceil(panel.scrollHeight + border));
        row.items.push({ card: card, article: article, openH: openH });
      });
      rows.forEach(function (row) {
        var tall = 0;
        row.items.forEach(function (item) {
          if (item.openH > tall) tall = item.openH;
        });
        var px = tall + "px";
        row.items.forEach(function (item) {
          item.card.style.minHeight = px;
          if (item.article) item.article.style.minHeight = px;
        });
      });
    });
  }

  lockRows();
  window.addEventListener("resize", lockRows);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(lockRows);
})();
