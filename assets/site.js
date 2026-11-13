// T1 Research & Development — shared script
// One file for the whole site. Each feature guards for its own elements,
// so pages only run what they actually contain.

(function () {
  "use strict";

  // ---------- Sticky header shadow ----------
  var header = document.querySelector(".site-header");
  function onScroll() {
    if (!header) return;
    if (window.scrollY > 4) {
      header.classList.add("scrolled");
    } else {
      header.classList.remove("scrolled");
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // ---------- Mobile menu ----------
  // The hamburger opens a slide-in drawer; the X (top-left), the
  // backdrop, a link tap, or Escape closes it.
  var navToggle = document.querySelector(".nav-toggle");
  var siteNav = document.querySelector(".site-nav");
  var navClose = document.querySelector(".nav-close");
  var backdrop = null;

  function getBackdrop() {
    if (!backdrop) {
      backdrop = document.createElement("div");
      backdrop.className = "nav-backdrop";
      backdrop.addEventListener("click", closeMenu);
      document.body.appendChild(backdrop);
    }
    return backdrop;
  }

  function openMenu() {
    if (!siteNav) return;
    siteNav.classList.add("open");
    getBackdrop().classList.add("visible");
    document.body.style.overflow = "hidden";
    if (navToggle) navToggle.setAttribute("aria-expanded", "true");
  }

  function closeMenu() {
    if (!siteNav) return;
    siteNav.classList.remove("open");
    if (backdrop) backdrop.classList.remove("visible");
    document.body.style.overflow = "";
    if (navToggle) navToggle.setAttribute("aria-expanded", "false");
  }

  if (navToggle && siteNav) {
    navToggle.addEventListener("click", openMenu);
    if (navClose) navClose.addEventListener("click", closeMenu);
    siteNav.addEventListener("click", function (event) {
      if (event.target.tagName === "A") closeMenu();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && siteNav.classList.contains("open")) {
        closeMenu();
      }
    });
    // If the viewport grows past the mobile breakpoint, reset the drawer.
    window.addEventListener("resize", function () {
      if (window.innerWidth > 640 && siteNav.classList.contains("open")) {
        closeMenu();
      }
    });
  }

  // ---------- Copy buttons (phone / email) ----------
  function copyText(text, button) {
    function done() {
      var original = button.textContent;
      button.textContent = "Copied ✓";
      setTimeout(function () { button.textContent = original; }, 2000);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { fallbackCopy(text, button, done); });
    } else {
      fallbackCopy(text, button, done);
    }
  }

  function fallbackCopy(text, button, done) {
    var area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.appendChild(area);
    area.select();
    try { document.execCommand("copy"); } catch (err) { /* clipboard unavailable */ }
    document.body.removeChild(area);
    done();
  }

  document.querySelectorAll("[data-copy]").forEach(function (button) {
    button.addEventListener("click", function () {
      copyText(button.getAttribute("data-copy"), button);
    });
  });

  // ---------- FAQ accordion ----------
  document.querySelectorAll(".faq-question").forEach(function (question) {
    question.addEventListener("click", function () {
      var item = question.closest(".faq-item");
      var wasOpen = item.classList.contains("open");
      document.querySelectorAll(".faq-item.open").forEach(function (openItem) {
        openItem.classList.remove("open");
        openItem.querySelector(".faq-question").setAttribute("aria-expanded", "false");
      });
      if (!wasOpen) {
        item.classList.add("open");
        question.setAttribute("aria-expanded", "true");
      }
    });
  });

  // ---------- Service + plan pre-select on the contact page ----------
  // Service pages link here with ?service=<slug>; hosting tier buttons
  // link with ?plan=<brochure|shop|bridge|growth|flagship|flagship-plus>
  // (which also selects the Website design & hosting service). The plan
  // field only shows when that service is chosen.
  var plans = {
    brochure: { name: "Brochure", setup: 155, monthly: 52 },
    shop: { name: "Shop", setup: 310, monthly: 105 },
    bridge: { name: "Bridge", setup: 415, monthly: 315 },
    growth: { name: "Growth", setup: 775, monthly: 520 },
    flagship: { name: "Flagship", setup: 1550, monthly: 780 },
    "flagship-plus": { name: "Flagship+", setup: 2575, monthly: 1560 }
  };
  var serviceSelect = document.getElementById("fService");
  var planField = document.getElementById("plan-field");
  var planSelect = document.getElementById("fPlan");
  var planStatus = document.getElementById("plan-status");

  function updatePlanField() {
    if (!planField || !serviceSelect) return;
    planField.style.display = serviceSelect.value === "website-hosting" ? "" : "none";
  }

  if (serviceSelect) {
    var params = new URLSearchParams(window.location.search);
    var svc = params.get("service");
    var chosen = params.get("plan");
    if (svc) {
      var opt = serviceSelect.querySelector("option[value=\"" + svc + "\"]");
      if (opt) serviceSelect.value = svc;
    }
    if (chosen && plans[chosen]) {
      serviceSelect.value = "website-hosting";
      if (planSelect) planSelect.value = chosen;
      if (planStatus) {
        planStatus.textContent = plans[chosen].name + " plan selected — tell us about your project below.";
        planStatus.classList.add("visible");
      }
    }
    updatePlanField();
    serviceSelect.addEventListener("change", function () {
      updatePlanField();
      if (planStatus) planStatus.classList.remove("visible");
    });
  }

  // ---------- Project form: submit to FormSubmit (formsubmit.co) ----------
  // No account or key needed. Submissions are emailed to the address the
  // form's action (email or alias) routes to. The FIRST real submission
  // triggers a one-time activation email to that address — click its link
  // once to confirm, then it's live. JS posts to the /ajax/ endpoint for an
  // inline status. FormSubmit answers HTTP 200 even when it rejects a
  // submission, so the reply body's success flag is checked — never trust
  // the status code alone. On failure the visitor stays on the page with
  // an inline error and the button re-enabled; the form NEVER falls back
  // to a plain POST, which would abandon the visitor on another page.
  var leadForm = document.getElementById("lead-form");
  if (leadForm) {
    leadForm.addEventListener("submit", function (event) {
      event.preventDefault();
      var status = document.getElementById("form-status");
      var submitButton = leadForm.querySelector("button[type=\"submit\"]");
      var action = leadForm.getAttribute("action");
      var ajaxUrl = action.replace("formsubmit.co/", "formsubmit.co/ajax/");

      function setStatus(text) {
        if (status) {
          status.textContent = text;
          status.classList.add("visible");
        }
      }

      if (submitButton) submitButton.disabled = true;
      setStatus("Sending…");

      fetch(ajaxUrl, {
        method: "POST",
        headers: { "Accept": "application/json" },
        body: new FormData(leadForm)
      }).then(function (response) {
        if (!response.ok) throw new Error("FormSubmit returned " + response.status);
        return response.json();
      }).then(function (data) {
        // FormSubmit returns HTTP 200 with success:"false" when it rejects
        // a submission (e.g. form not activated yet) — only a true success
        // flag counts as sent.
        if (!data || data.success !== "true") throw new Error("FormSubmit rejected the submission");
        setStatus("Thanks — your message is on its way. We'll get back to you soon.");
        leadForm.reset();
        if (submitButton) submitButton.disabled = false;
      }).catch(function () {
        // Stay on the page: show an inline error and re-enable the button
        // so the visitor can retry or email directly.
        setStatus("Sorry — that didn't send. Please email us directly at tasikxdevelopment@gmail.com and we'll get back to you.");
        if (submitButton) submitButton.disabled = false;
      });
    });
  }
})();
