def analyze_log_file(log_file_path):
    log_counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}

    try:
        with open(log_file_path, "r") as file:
            lines = file.readlines()
            if not lines:
                print("Log file is empty.")
                return log_counts
            for line in lines:
                if "INFO" in line:
                    log_counts["INFO"] += 1
                if "WARNING" in line:
                    log_counts["WARNING"] += 1
                if "ERROR" in line:
                    log_counts["ERROR"] += 1
    except FileNotFoundError:
        print(f"Log file '{log_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred while reading the log file: {e}")
    return log_counts

def write_summary(output_path, counts):
    try:
        with open(output_path, "w") as file:
            summary = (
                f"Log Summary:\n"
                f"INFO: {counts['INFO']}\n"
                f"WARNING: {counts['WARNING']}\n"
                f"ERROR: {counts['ERROR']}\n"
            )
            file.write(summary)
    except Exception as e:
        print(f"Error writing summary file: {e}")

def print_summary(counts):
    print("Log Summary:")
    print(f"INFO: {counts['INFO']}")
    print(f"WARNING: {counts['WARNING']}")
    print(f"ERROR: {counts['ERROR']}")

def main():
    log_file = "app.log"
    output_file = "log_summary.txt"
    counts = analyze_log_file(log_file)
    print_summary(counts)
    write_summary(output_file, counts)

if __name__ == "__main__":
    main()