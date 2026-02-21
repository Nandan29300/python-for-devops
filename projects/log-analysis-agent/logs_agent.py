"""
Log Analysis Agent
==================
An AI-powered agent that reads and analyzes log files using a local LLM
via Ollama (llama3.2) and the Strands Agents framework.

Usage:
    python logs_agent.py                      # interactive mode
    python logs_agent.py --file app.log       # analyze a specific log file
    python logs_agent.py --query "summarize errors"  # single query mode
"""

import argparse
import sys
import os

from strands import Agent                      # Agentic framework
from strands_tools import file_read            # Built-in file read tool
from strands.models.ollama import OllamaModel  # Local LLM via Ollama


# ── System Prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are an expert Log Analysis Agent with a strong DevOps mindset.

Your capabilities:
- Read and parse log files (.log, system logs, application logs, etc.)
- Identify patterns, anomalies, and root causes
- Count occurrences of log levels: INFO, WARNING, ERROR, DEBUG, CRITICAL
- Summarize findings in a short, crisp, actionable manner
- Suggest remediation ideas (but never take production actions)

Rules:
- Never hallucinate log content — only analyze what is actually in the file
- Always reference the exact log lines or timestamps when citing issues
- Keep responses concise and focused on DevOps-relevant insights
- If a log file path is provided, always use the file_read tool to read it first
"""

# ── Pre-built Queries ─────────────────────────────────────────────────────────
PRESET_QUERIES = {
    "1": {
        "label": "Count log levels",
        "query": "Read app.log and count how many times INFO, WARNING, ERROR, DEBUG, and CRITICAL appear. Return only the counts in a clear table."
    },
    "2": {
        "label": "Summarize errors",
        "query": "Read app.log. List all ERROR and CRITICAL log entries with their timestamps and messages. Then provide a brief root cause analysis."
    },
    "3": {
        "label": "Warnings analysis",
        "query": "Read app.log. List all WARNING entries with timestamps. Identify any recurring warning patterns and suggest what a DevOps engineer should investigate."
    },
    "4": {
        "label": "Full health report",
        "query": "Read app.log. Provide a complete health report including: total log lines, counts per level, timeline of issues, most critical problems, and 3 actionable recommendations for the DevOps team."
    },
    "5": {
        "label": "Timeline of events",
        "query": "Read app.log. Build a chronological timeline of significant events (WARNING, ERROR, CRITICAL only) with timestamps. Highlight any time windows where multiple issues occurred."
    },
}


def build_agent(ollama_host: str, model_id: str) -> Agent:
    """Initialize the Strands Agent with Ollama LLM and file_read tool."""
    ollama_model = OllamaModel(
        host=ollama_host,
        model_id=model_id
    )
    agent = Agent(
        system_prompt=SYSTEM_PROMPT,
        model=ollama_model,
        tools=[file_read]
    )
    return agent


def run_single_query(agent: Agent, query: str, log_file: str = None):
    """Run a single query, optionally injecting the log file path."""
    if log_file:
        full_query = f"Analyze the log file at: {os.path.abspath(log_file)}\n\n{query}"
    else:
        full_query = query

    print("\n" + "=" * 60)
    print(f"🤖 Query: {query}")
    print("=" * 60)
    agent(full_query)
    print("=" * 60 + "\n")


def run_interactive(agent: Agent, log_file: str):
    """Run the agent in interactive mode with preset + custom queries."""
    abs_path = os.path.abspath(log_file)

    print("\n" + "=" * 60)
    print("  🔍 Log Analysis Agent — Interactive Mode")
    print(f"  📄 Log file: {abs_path}")
    print("=" * 60)

    while True:
        print("\nChoose an option:")
        for key, val in PRESET_QUERIES.items():
            print(f"  [{key}] {val['label']}")
        print("  [c] Custom query")
        print("  [q] Quit")

        choice = input("\nYour choice: ").strip().lower()

        if choice == "q":
            print("\n👋 Goodbye!")
            break
        elif choice == "c":
            custom = input("Enter your query: ").strip()
            if custom:
                run_single_query(agent, custom, log_file=log_file)
        elif choice in PRESET_QUERIES:
            run_single_query(agent, PRESET_QUERIES[choice]["query"], log_file=log_file)
        else:
            print("❌ Invalid choice. Please try again.")


def main():
    parser = argparse.ArgumentParser(
        description="AI-powered Log Analysis Agent using Strands + Ollama"
    )
    parser.add_argument(
        "--file", "-f",
        default="app.log",
        help="Path to the log file to analyze (default: app.log)"
    )
    parser.add_argument(
        "--query", "-q",
        default=None,
        help="Run a single query and exit (non-interactive mode)"
    )
    parser.add_argument(
        "--host",
        default="http://localhost:11434",
        help="Ollama server address (default: http://localhost:11434)"
    )
    parser.add_argument(
        "--model",
        default="llama3.2",
        help="Ollama model to use (default: llama3.2)"
    )
    args = parser.parse_args()

    # Validate log file exists
    if not os.path.exists(args.file):
        print(f"❌ Error: Log file '{args.file}' not found.")
        sys.exit(1)

    print(f"🚀 Connecting to Ollama at {args.host} using model '{args.model}'...")

    try:
        agent = build_agent(ollama_host=args.host, model_id=args.model)
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        print("   Make sure Ollama is running: ollama serve")
        print(f"   And the model is pulled:    ollama pull {args.model}")
        sys.exit(1)

    if args.query:
        # Non-interactive: single query mode
        run_single_query(agent, args.query, log_file=args.file)
    else:
        # Interactive mode
        run_interactive(agent, log_file=args.file)


if __name__ == "__main__":
    main()