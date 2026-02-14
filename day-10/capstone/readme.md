# DevOps Capstone Project: Python Log Analyzer & Automation

---

## Capstone Overview

A project demonstrating real DevOps automation skills using Python:
- Log analysis
- CLI tool usage
- Optionally, FastAPI for API access
- Clean, readable code with comments

---

## S.T.A.R. Explanation (for Interview)

**S – Situation**
- Daily log files were accumulating, and checking them manually for errors and warnings was slow and error-prone.
- The DevOps team struggled to quickly identify issues from system/application logs.

**T – Task**
- Automate log analysis to provide summary reports.
- Make the tool accessible via CLI, so any team member could use it.
- Optionally, provide an API for automated systems to trigger analysis.

**A – Action**
- Built a Python script to read log files and count INFO, WARNING, and ERROR messages.
- Added CLI support using `argparse` so users could specify log and output files, and filter by log level.
- Refactored the code using object-oriented principles to keep it organized and reusable.
- (Optional) Wrapped the logic in a FastAPI app, so the analysis could be triggered over HTTP as an internal DevOps service.

**R – Result**
- Manual log checking was eliminated; automated summaries were available in seconds.
- Team could respond to problems faster and more reliably.
- The script and API became a reusable internal tool for future automation.

---

## Project Files

- `log_analyzer.py` — Log analysis script
- `log_analyzer_cli.py` — CLI version with argparse
- `main.py` — FastAPI API version (optional)
- `app.log` — Sample log file
- `log_summary.txt` — Example output file

---

## DevOps Mindset Reflection

- This project demonstrates why Python is a *DevOps enabler* — it makes automation fast, clear, and powerful.
- The focus was not just on code, but on reliability, repeatability, and solving a real problem for the team.
- Clean structure, error handling, and user-friendly interfaces are as important as functionality.
- DevOps is about ownership: seeing a pain-point, and building automation to fix it for everyone.

---

## What's Next?

- Learn more about CI/CD, containers, Kubernetes, monitoring, and cloud platforms.
- Practice explaining not just *what* you did, but *why* and *how* you did it.
- Remember: Thinking before coding is what makes DevOps effective.

---
