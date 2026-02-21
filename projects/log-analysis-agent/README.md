# 🔍 Log Analysis Agent

An AI-powered agent that reads and analyzes log files using a **local LLM (llama3.2)** 
via **Ollama** and the **Strands Agents** framework.

---

## 🎯 Aim

Automate log analysis using an AI agent that can:
- Count log levels (INFO, WARNING, ERROR, DEBUG, CRITICAL)
- Identify error patterns and root causes
- Build timelines of incidents
- Generate full health reports
- Answer custom natural-language queries about any log file

---

## 🏗️ Architecture

```
logs_agent.py
│
├── Strands Agent (orchestrator)
│   ├── System Prompt  →  DevOps-focused log analysis persona
│   ├── Tool: file_read  →  reads the log file from disk
│   └── Model: OllamaModel (llama3.2 running locally)
│
└── CLI Interface
    ├── Interactive mode  →  menu of preset queries + custom input
    └── Single query mode →  --query flag for scripting/automation
```

---

## ⚙️ Prerequisites

### 1. Install Ollama
```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# macOS
brew install ollama
```

### 2. Start Ollama & pull the model
```bash
ollama serve          # start the Ollama server (runs on port 11434)
ollama pull llama3.2  # download the llama3.2 model (~2 GB)
```

### 3. Verify Ollama is running
```bash
ollama list           # should show llama3.2 in the list
curl http://localhost:11434/api/tags  # should return JSON with models
```

---

## 🚀 Setup

```bash
git clone <repo-url>
cd log-analysis-agent

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Run

### Interactive mode (menu-driven)
```bash
python logs_agent.py
```

### Analyze a specific log file
```bash
python logs_agent.py --file /var/log/syslog
python logs_agent.py --file /path/to/your/app.log
```

### Single query mode (great for automation/scripts)
```bash
python logs_agent.py --query "count all ERROR entries"
python logs_agent.py --file app.log --query "summarize the top 3 issues"
```

### Use a different Ollama model
```bash
python logs_agent.py --model llama3.1
python logs_agent.py --model mistral
```

### Use a remote Ollama server
```bash
python logs_agent.py --host http://192.168.1.100:11434
```

---

## 📋 Preset Queries (Interactive Mode)

| # | Query |
|---|-------|
| 1 | **Count log levels** — returns a table of INFO/WARNING/ERROR/DEBUG/CRITICAL counts |
| 2 | **Summarize errors** — lists all ERROR/CRITICAL lines with root cause analysis |
| 3 | **Warnings analysis** — lists warnings and suggests investigation areas |
| 4 | **Full health report** — complete analysis with actionable recommendations |
| 5 | **Timeline of events** — chronological incident timeline |
| c | **Custom query** — ask anything about the log file |

---

## 📁 Project Structure

```
log-analysis-agent/
├── logs_agent.py      # Main agent — CLI, prompts, Strands setup
├── app.log            # Sample log file for testing
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

---

## 🧠 How It Works

1. The **Strands Agent** is initialized with a DevOps-focused system prompt
2. When a query is made, the agent uses the `file_read` **tool** to read the log file from disk
3. The log content is passed to **llama3.2** running locally via Ollama
4. The LLM analyzes the content and returns structured, actionable insights
5. No data leaves your machine — fully local and private

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| `ollama: command not found` | Install Ollama from https://ollama.com |
| `Connection refused on port 11434` | Run `ollama serve` first |
| `model not found` | Run `ollama pull llama3.2` |
| Slow responses | llama3.2 requires ~4 GB RAM; use `llama3.2:1b` for a lighter model |
| `strands` import error | Run `pip install -r requirements.txt` inside the venv |

