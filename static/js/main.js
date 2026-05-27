(function () {
  "use strict";

  var API_BASE = window.SECUREREPO_API_BASE || (location.protocol === "file:" ? "http://localhost:5000" : "");
  var STORAGE_KEY = "securerepoUserId";
  var HISTORY_KEY = "securerepoScanHistory";
  var logs = [
    "Resolving repository input...",
    "Preparing scanner workspace...",
    "Running secret detection rules...",
    "Checking risky files and credentials...",
    "Reviewing API and configuration patterns...",
    "Calculating score and severity summary...",
    "Preparing student-friendly report..."
  ];

  var scanForm = document.querySelector("[data-scan-form]");
  var alertBox = document.querySelector("[data-alert]");
  var loadingPanel = document.querySelector("[data-loading]");
  var logOutput = document.querySelector("[data-log-output]");
  var reportPanel = document.querySelector("[data-report-panel]");
  var resultsPlaceholder = document.getElementById("results-placeholder");
  var scanButton = document.querySelector("[data-scan-button]");
  var userIdInput = document.querySelector("[data-user-id-input]");
  var healthStatus = document.querySelector("[data-health-status]");
  var historyList = document.querySelector("[data-history-list]");
  var primaryNav = document.querySelector("[data-primary-nav]");
  var menuButton = document.querySelector("[data-menu-button]");
  var logTimer = null;

  function apiUrl(path) {
    return API_BASE + path;
  }

  function getUserId() {
    var existing = localStorage.getItem(STORAGE_KEY);
    if (existing) {
      return existing;
    }
    var generated = "local-" + Math.random().toString(16).slice(2) + Date.now().toString(16);
    localStorage.setItem(STORAGE_KEY, generated);
    return generated;
  }

  function setUserId(value) {
    var clean = value.trim() || getUserId();
    localStorage.setItem(STORAGE_KEY, clean);
    if (userIdInput) {
      userIdInput.value = clean;
    }
    showAlert("Saved local profile id.", "success");
  }

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function showAlert(message, type) {
    alertBox.textContent = message;
    alertBox.classList.remove("hidden");
    alertBox.style.borderColor = type === "success" ? "#a6d9c2" : "";
    alertBox.style.background = type === "success" ? "#ecfdf3" : "";
    alertBox.style.color = type === "success" ? "#027a48" : "";
  }

  function hideAlert() {
    alertBox.classList.add("hidden");
    alertBox.textContent = "";
    alertBox.removeAttribute("style");
  }

  function startLoading() {
    var index = 0;
    loadingPanel.classList.remove("hidden");
    if (scanButton) {
      scanButton.disabled = true;
      scanButton.textContent = "Scanning...";
    }
    logOutput.textContent = "[INIT] Starting SecureRepo scanner...";
    clearInterval(logTimer);
    logTimer = setInterval(function () {
      if (index >= logs.length) {
        return;
      }
      logOutput.textContent += "\n[" + new Date().toLocaleTimeString() + "] " + logs[index];
      logOutput.scrollTop = logOutput.scrollHeight;
      index += 1;
    }, 850);
  }

  function stopLoading() {
    clearInterval(logTimer);
    loadingPanel.classList.add("hidden");
    if (scanButton) {
      scanButton.disabled = false;
      scanButton.textContent = "Start Scan";
    }
  }

  function request(path, options) {
    return fetch(apiUrl(path), options).then(function (response) {
      return response.text().then(function (text) {
        var data = text ? JSON.parse(text) : {};
        if (!response.ok) {
          throw new Error(data.detail || data.message || "Request failed.");
        }
        return data;
      });
    });
  }

  function runScan(repoUrl, useAi) {
    hideAlert();
    startLoading();
    request("/api/scan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        repo_url: repoUrl,
        use_ai_explanation: useAi
      })
    })
      .then(function (report) {
        stopLoading();
        saveReport(report);
        renderReport(report);
        loadHistory(false);
        location.hash = "reports";
      })
      .catch(function (error) {
        stopLoading();
        showAlert(error.message || "Scan failed. Make sure the repository is public or try the local demo repository.");
      });
  }

  function renderReport(report) {
    var summary = report.summary || {};
    var issues = report.findings || [];

    reportPanel.classList.remove("hidden");
    if (resultsPlaceholder) {
      resultsPlaceholder.classList.add("hidden");
    }
    document.querySelector("[data-report-title]").textContent = report.repository ? report.repository + " scan report" : "Scan report";
    document.querySelector("[data-report-repo]").textContent = report.repository || "";
    document.querySelector("[data-report-score]").textContent = report.score == null ? "0" : report.score;
    document.querySelector("[data-report-risk]").textContent = report.risk_level || "Unknown risk";

    var ring = document.querySelector(".score-ring");
    if (ring) {
      ring.className = "score-ring " + String(report.risk_level || "").toLowerCase();
    }

    document.querySelector("[data-summary-grid]").innerHTML = [
      ["critical", summary.critical || 0],
      ["high", summary.high || 0],
      ["medium", summary.medium || 0],
      ["low", summary.low || 0]
    ].map(function (item) {
      return '<div class="summary-count ' + item[0] + '"><strong>' + item[1] + '</strong><span>' + item[0] + '</span></div>';
    }).join("");

    document.querySelector("[data-ai-summary]").innerHTML = "<strong>Report summary</strong><p>SecureRepo found " + issues.length + " issue(s). Review each finding and apply the recommended fixes before sharing this repository.</p>";

    document.querySelector("[data-issue-list]").innerHTML = issues.length ? issues.map(renderIssue).join("") : '<div class="issue-card">No issues found. Nice clean scan.</div>';
  }

  function renderIssue(issue) {
    var severity = String(issue.severity || "low").toLowerCase();
    var explanation = issue.beginner_explanation || issue.studentExplanation || "";
    return '<article class="finding-card">' +
      '<div class="finding-bar ' + escapeHtml(severity) + '"></div>' +
      '<div class="finding-body">' +
      '<div class="finding-header">' +
      '<div class="finding-title"><span class="severity ' + escapeHtml(severity) + '">' + escapeHtml(issue.severity || "Low") + '</span><h3>' + escapeHtml(issue.type || "Issue") + '</h3></div>' +
      '</div>' +
      '<span class="file-path"><span class="material-symbols-outlined">description</span>' + escapeHtml(issue.file || "unknown file") + (issue.line ? " : Line " + escapeHtml(issue.line) : "") + '</span>' +
      '<p>' + escapeHtml(issue.message || "") + '</p>' +
      (explanation ? '<div class="beginner-box"><h4><span class="material-symbols-outlined">lightbulb</span> Beginner Explanation</h4><p>' + escapeHtml(explanation) + '</p></div>' : "") +
      '<div class="finding-fix"><span><span class="material-symbols-outlined">warning</span> Recommended: ' + escapeHtml(issue.fix || "Review this finding and update the affected code.") + '</span><button class="button primary" type="button">View Fix Guide</button></div>' +
      '</div>' +
      '</article>';
  }

  function loadHistory(showMessage) {
    var scans = getSavedReports();
    if (!scans.length) {
      historyList.innerHTML = '<div class="history-card"><strong>No scans yet</strong><p>Run your first scan above.</p></div>';
      if (showMessage) {
        showAlert("No local scan history found for this browser.", "success");
      }
      return;
    }
    historyList.innerHTML = scans.map(renderHistoryItem).join("");
  }

  function renderHistoryItem(entry) {
    var scan = entry.report;
    var counts = scan.summary || {};
    var date = entry.createdAt ? new Date(entry.createdAt).toLocaleString() : "Unknown date";
    return '<article class="history-card">' +
      '<div class="history-top">' +
      '<div><strong>' + escapeHtml(scan.repository || "Repository") + '</strong><p class="muted">' + escapeHtml(date) + '</p></div>' +
      '<span class="mini-status ' + escapeHtml(String(scan.risk_level || "low").toLowerCase()) + '">' + escapeHtml(scan.risk_level || "Risk") + '</span>' +
      '</div>' +
      '<p>Critical: ' + (counts.critical || 0) + ' | High: ' + (counts.high || 0) + ' | Medium: ' + (counts.medium || 0) + ' | Low: ' + (counts.low || 0) + '</p>' +
      '<button class="link-button" type="button" data-open-scan="' + escapeHtml(entry.id) + '">Open report</button> ' +
      '<button class="link-button" type="button" data-delete-scan="' + escapeHtml(entry.id) + '">Delete</button>' +
      '</article>';
  }

  function openExistingReport(scanId) {
    var match = getSavedReports().find(function (entry) {
      return entry.id === scanId;
    });
    if (!match) {
      showAlert("Could not open that local report.");
      return;
    }
    renderReport(match.report);
    location.hash = "reports";
  }

  function deleteScan(scanId) {
    var remaining = getSavedReports().filter(function (entry) {
      return entry.id !== scanId;
    });
    localStorage.setItem(HISTORY_KEY, JSON.stringify(remaining));
    loadHistory(false);
    showAlert("Scan deleted from local history.", "success");
  }

  function saveReport(report) {
    var scans = getSavedReports();
    scans.unshift({
      id: "scan-" + Date.now().toString(16),
      createdAt: new Date().toISOString(),
      report: report
    });
    localStorage.setItem(HISTORY_KEY, JSON.stringify(scans.slice(0, 20)));
  }

  function getSavedReports() {
    try {
      return JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
    } catch (error) {
      return [];
    }
  }

  function checkHealth() {
    request("/health")
      .then(function (health) {
        healthStatus.textContent = "API status: " + health.status + " | " + (health.service || "SecureRepo");
      })
      .catch(function () {
        healthStatus.textContent = "API status: offline";
      });
  }

  function bindEvents() {
    scanForm.addEventListener("submit", function (event) {
      event.preventDefault();
      var data = new FormData(scanForm);
      var repoUrl = String(data.get("repoUrl") || "").trim();
      if (!repoUrl) {
        showAlert("Please enter a repository URL or local path.");
        return;
      }
      runScan(repoUrl, data.get("useAi") === "on");
    });

    document.querySelectorAll("[data-example]").forEach(function (button) {
      button.addEventListener("click", function () {
        document.getElementById("repo-url").value = button.getAttribute("data-example");
        hideAlert();
      });
    });

    var saveUserButton = document.querySelector("[data-save-user]");
    if (saveUserButton && userIdInput) {
      saveUserButton.addEventListener("click", function () {
        setUserId(userIdInput.value);
      });
    }

    document.querySelectorAll("[data-load-history]").forEach(function (button) {
      button.addEventListener("click", function () {
        loadHistory(true);
      });
    });

    historyList.addEventListener("click", function (event) {
      var openButton = event.target.closest("[data-open-scan]");
      var deleteButton = event.target.closest("[data-delete-scan]");
      if (openButton) {
        openExistingReport(openButton.getAttribute("data-open-scan"));
      }
      if (deleteButton && confirm("Delete this scan from history?")) {
        deleteScan(deleteButton.getAttribute("data-delete-scan"));
      }
    });

    menuButton.addEventListener("click", function () {
      var open = primaryNav.classList.toggle("open");
      menuButton.setAttribute("aria-expanded", String(open));
    });

    primaryNav.addEventListener("click", function () {
      primaryNav.classList.remove("open");
      menuButton.setAttribute("aria-expanded", "false");
    });
  }

  function init() {
    if (userIdInput) {
      userIdInput.value = getUserId();
    } else {
      getUserId();
    }
    bindEvents();
    checkHealth();
    loadHistory(false);
  }

  init();
}());
