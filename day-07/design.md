# Design Plan for Day 06: Log Analyzer CLI Tool

## 1. What problem am I solving?
- I want to quickly analyze log files to count how many INFO, WARNING, and ERROR messages there are.
- This helps DevOps engineers understand system/application health just by looking at logs without reading each line.

---

## 2. What input does my script need?
- Path to the log file (required), e.g., `app.log`
- Optional: Path for the output summary file, e.g., `summary.txt`
- Optional: Log level to filter (INFO, WARNING, ERROR)

---

## 3. What output should my script give?
- Print a summary to the terminal showing the count of each log level (or the filtered log level)
- Write the same summary to the output file (e.g., `log_summary.txt` or user-specified file)

---

## 4. What are the main steps?

- **Step 1:** Parse CLI arguments (`--file`, `--out`, `--level`) using `argparse`
- **Step 2:** Read all lines from the provided log file
  - If the log file is missing or empty, print an error and exit
- **Step 3:** For each log entry, analyze if it is INFO, WARNING, or ERROR (and count)
  - If a log level filter is provided, only count those
- **Step 4:** Display the summary on the terminal
- **Step 5:** Save the summary to an output file

---

## Summary

- User gives a log file, and (optionally) output file or log level to count.
- Script checks and counts entries, then prints and saves summary.
- Planning all steps before writing code reduces errors and makes logic clear.