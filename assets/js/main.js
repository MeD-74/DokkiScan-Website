/* Dokki Scan — shared behaviour: mobile menu, animated counters, booking -> WhatsApp. */
(function () {
  "use strict";

  // Mobile menu
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Animated counters: count up when the stats section scrolls into view.
  var counters = document.querySelectorAll("[data-count]");
  if ("IntersectionObserver" in window && counters.length) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        observer.unobserve(el);
        var target = parseInt(el.getAttribute("data-count"), 10) || 0;
        var suffix = el.getAttribute("data-suffix") || "";
        var start = null;
        function tick(ts) {
          if (!start) start = ts;
          var p = Math.min((ts - start) / 1200, 1);
          el.textContent = Math.round(target * p) + suffix;
          if (p < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
      });
    }, { threshold: 0.4 });
    counters.forEach(function (el) { observer.observe(el); });
  }

  // Booking form -> WhatsApp (same behaviour as the original site:
  // the form does not book a slot; reception confirms on WhatsApp).
  var form = document.getElementById("booking-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var lang = form.getAttribute("data-lang") || "ar";
      var name = document.getElementById("f-name").value.trim();
      var mobile = document.getElementById("f-mobile").value.trim();
      var exam = document.getElementById("f-exam").value;
      var day = document.getElementById("f-day").value;
      var hour = document.getElementById("f-hour").value;
      var flex = document.getElementById("f-flex").value;
      var notes = document.getElementById("f-notes").value.trim();
      var error = document.getElementById("form-error");
      var ok = document.getElementById("form-ok");

      function fail(msg) {
        if (error) error.textContent = msg;
        if (ok) ok.style.display = "none";
      }
      if (name.length < 2) return fail(lang === "ar" ? "من فضلك اكتب الاسم بالكامل." : "Please enter your full name.");
      if (!/^[0-9+\s]{10,15}$/.test(mobile)) return fail(lang === "ar" ? "من فضلك اكتب رقم موبايل صحيح (10 أرقام على الأقل)." : "Please enter a valid mobile number (at least 10 digits).");
      if (!exam) return fail(lang === "ar" ? "من فضلك اختر نوع الفحص." : "Please choose the exam type.");
      if (!day) return fail(lang === "ar" ? "من فضلك اختر يوم الحجز." : "Please choose the booking day.");
      if (!hour) return fail(lang === "ar" ? "من فضلك اختر ساعة الحجز." : "Please choose the booking hour.");
      if (error) error.textContent = "";

      var lines = lang === "ar" ? [
        "طلب حجز — دقي سكان",
        "الاسم: " + name,
        "الموبايل: " + mobile,
        "نوع الفحص: " + exam,
        "اليوم: " + day,
        "الساعة: " + hour,
        "مرونة الموعد: " + flex,
        "ملاحظات / اسم الطبيب: " + (notes || "—")
      ] : [
        "Booking request — Dokki Scan",
        "Name: " + name,
        "Mobile: " + mobile,
        "Exam: " + exam,
        "Day: " + day,
        "Hour: " + hour,
        "Flexibility: " + flex,
        "Notes / doctor: " + (notes || "—")
      ];
      if (ok) ok.style.display = "block";
      window.open("https://wa.me/201000010144?text=" + encodeURIComponent(lines.join("\n")), "_blank");
    });
  }
})();
