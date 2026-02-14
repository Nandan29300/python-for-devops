import argparse

class LogAnalyzer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.counts = {"INFO": 0, "WARNING": 0, "ERROR": 0, "UNKNOWN": 0}

    def read_logs(self):
        try:
            with open(self.log_file, "r") as f:
                return f.readlines()
        except FileNotFoundError:
            print(f"Error: Log file '{self.log_file}' not found.")
            return []

    def analyze_logs(self, lines, level_filter=None):
        for line in lines:
            if "INFO" in line:
                self.counts["INFO"] += 1
            elif "WARNING" in line:
                self.counts["WARNING"] += 1
            elif "ERROR" in line:
                self.counts["ERROR"] += 1
            else:
                self.counts["UNKNOWN"] += 1
        if level_filter:
            # Only keep the requested log level and 'UNKNOWN'
            self.counts = {k: v for k, v in self.counts.items() if k == level_filter or k == "UNKNOWN"}
        return self.counts

    def write_summary(self, output_file):
        try:
            with open(output_file, "w") as f:
                f.write("Log Analysis Summary:\n")
                for level, count in self.counts.items():
                    f.write(f"{level}: {count}\n")
        except Exception as e:
            print(f"Error writing summary file: {e}")

    def print_summary(self):
        print("Log Analysis Summary:")
        for level, count in self.counts.items():
            print(f"{level}: {count}")

def main():
    parser = argparse.ArgumentParser(description="Analyze logs and print summary.")
    parser.add_argument("--file", required=True, help="Path to log file (input)")
    parser.add_argument("--out", default="log_summary.txt", help="Output file for summary")
    parser.add_argument("--level", choices=["INFO", "WARNING", "ERROR"], help="Filter by log level")
    args = parser.parse_args()

    analyzer = LogAnalyzer(args.file)
    lines = analyzer.read_logs()
    if not lines:
        print("No logs to analyze or file not found.")
        return
    analyzer.analyze_logs(lines, level_filter=args.level)
    analyzer.print_summary()
    analyzer.write_summary(args.out)
    print(f"\nSummary written to {args.out}")

if __name__ == "__main__":
    main()