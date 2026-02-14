class LogAnalyzer:
    def __init__(self, log_file):
        self.log_file = log_file
        self.counts = {"INFO": 0, "WARNING": 0, "ERROR": 0, "UNKNOWN": 0}

    def read_logs(self):
        try:
            with open(self.log_file, "r") as f:
                return f.readlines()
        except FileNotFoundError:
            print("Log file not found:", self.log_file)
            return []

    def analyze_logs(self, lines):
        for line in lines:
            if "INFO" in line:
                self.counts["INFO"] += 1
            elif "WARNING" in line:
                self.counts["WARNING"] += 1
            elif "ERROR" in line:
                self.counts["ERROR"] += 1
            else:
                self.counts["UNKNOWN"] += 1
        return self.counts

    def print_summary(self):
        print("Log Analysis Summary:")
        for level, count in self.counts.items():
            print(f"{level}: {count}")

def main():
    analyzer = LogAnalyzer("app.log")
    lines = analyzer.read_logs()
    if not lines:
        print("No logs to analyze.")
        return
    analyzer.analyze_logs(lines)
    analyzer.print_summary()

if __name__ == "__main__":
    main()