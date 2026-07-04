(function () {
  const formatInr = (value) => {
    if (!Number.isFinite(value)) return "INR 0";
    return `INR ${Math.round(value).toLocaleString("en-IN")}`;
  };

  const byId = (id) => document.getElementById(id);

  const animateCounters = () => {
    const counters = document.querySelectorAll(".counter");
    if (!counters.length) return;

    const runCounter = (counter) => {
      const target = Number(counter.dataset.target || 0);
      const duration = 1300;
      const start = performance.now();

      const tick = (now) => {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        counter.textContent = Math.floor(target * eased).toLocaleString("en-IN");
        if (progress < 1) requestAnimationFrame(tick);
      };

      requestAnimationFrame(tick);
    };

    const observer = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            runCounter(entry.target);
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.45 }
    );

    counters.forEach((counter) => observer.observe(counter));
  };

  const setupSipCalculator = () => {
    const amountEl = byId("sipAmount");
    const yearsEl = byId("sipYears");
    const rateEl = byId("sipReturn");
    const resultEl = byId("sipResult");
    if (!amountEl || !yearsEl || !rateEl || !resultEl) return;

    const calc = () => {
      const monthly = Number(amountEl.value);
      const years = Number(yearsEl.value);
      const annualRate = Number(rateEl.value) / 100;
      const monthlyRate = annualRate / 12;
      const months = years * 12;

      let corpus = 0;
      if (monthlyRate > 0 && months > 0) {
        corpus = monthly * (((Math.pow(1 + monthlyRate, months) - 1) / monthlyRate) * (1 + monthlyRate));
      } else if (months > 0) {
        corpus = monthly * months;
      }

      resultEl.textContent = `Estimated Corpus: ${formatInr(corpus)}`;
    };

    [amountEl, yearsEl, rateEl].forEach((el) => el.addEventListener("input", calc));
    calc();
  };

  const setupGoalPlanner = () => {
    const targetEl = byId("goalTarget");
    const yearsEl = byId("goalYears");
    const rateEl = byId("goalReturn");
    const resultEl = byId("goalResult");
    if (!targetEl || !yearsEl || !rateEl || !resultEl) return;

    const calc = () => {
      const target = Number(targetEl.value);
      const years = Number(yearsEl.value);
      const annualRate = Number(rateEl.value) / 100;
      const monthlyRate = annualRate / 12;
      const months = years * 12;

      let sip = 0;
      if (monthlyRate > 0 && months > 0) {
        sip = target / ((((Math.pow(1 + monthlyRate, months) - 1) / monthlyRate) * (1 + monthlyRate)) || 1);
      } else if (months > 0) {
        sip = target / months;
      }

      resultEl.textContent = `Required SIP: ${formatInr(sip)} / month`;
    };

    [targetEl, yearsEl, rateEl].forEach((el) => el.addEventListener("input", calc));
    calc();
  };

  const setupRiskQuiz = () => {
    const assessBtn = byId("riskAssessBtn");
    const resultEl = byId("riskResult");
    if (!assessBtn || !resultEl) return;

    assessBtn.addEventListener("click", () => {
      const age = Number(byId("riskAge")?.value || 0);
      const horizon = Number(byId("riskHorizon")?.value || 0);
      const volatility = Number(byId("riskVolatility")?.value || 0);
      const score = age + horizon + volatility;

      let profile = "Conservative";
      if (score >= 8) profile = "Aggressive";
      else if (score >= 6) profile = "Moderate";

      resultEl.textContent = `Profile: ${profile} (Indicative)`;
    });
  };

  const setupExitIntent = () => {
    const modalEl = byId("exitModal");
    if (!modalEl || typeof bootstrap === "undefined") return;

    let shown = false;
    const modal = new bootstrap.Modal(modalEl);

    document.addEventListener("mouseout", (event) => {
      if (shown) return;
      if (event.clientY <= 0) {
        shown = true;
        modal.show();
      }
    });
  };

  const setupConsultForm = () => {
    const form = byId("consultForm");
    if (!form) return;

    form.addEventListener("submit", () => {
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.textContent = "Sending...";
        submitBtn.disabled = true;
      }
    });
  };

  const setupAnimations = () => {
    const revealEls = document.querySelectorAll(".reveal");

    if (typeof gsap === "undefined") {
      revealEls.forEach((el) => {
        el.style.opacity = "1";
        el.style.transform = "none";
      });
      return;
    }

    if (typeof ScrollTrigger !== "undefined") {
      gsap.registerPlugin(ScrollTrigger);
    }

    gsap.fromTo(
      ".hero-title, .hero-subtitle, .hero .btn",
      { y: 18, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.8, stagger: 0.1, ease: "power2.out" }
    );

    gsap.to(".line-graph polyline", {
      strokeDashoffset: 0,
      duration: 1.8,
      ease: "power2.out",
      delay: 0.3,
    });

    gsap.to(".float-icon", {
      y: -8,
      duration: 2.2,
      repeat: -1,
      yoyo: true,
      stagger: 0.35,
      ease: "sine.inOut",
    });

    revealEls.forEach((el) => {
      gsap.to(el, {
        y: 0,
        opacity: 1,
        duration: 0.65,
        ease: "power2.out",
        scrollTrigger: {
          trigger: el,
          start: "top 86%",
          once: true,
        },
      });
    });
  };

  document.addEventListener("DOMContentLoaded", () => {
    setupAnimations();
    animateCounters();
    setupSipCalculator();
    setupGoalPlanner();
    setupRiskQuiz();
    setupExitIntent();
    setupConsultForm();
  });
})();
