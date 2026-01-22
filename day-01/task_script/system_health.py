import psutil

def get_thresholds():
    cpu_th = int(input("Enter CPU threshold (%): "))
    mem_th = int(input("Enter Memory threshold (%): "))
    disk_th = int(input("Enter Disk threshold (%): "))
    return cpu_th, mem_th, disk_th


def check_system(cpu_th, mem_th, disk_th):
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    print("\n--- System Metrics ---")
    print("CPU Usage:", cpu, "%")
    print("Memory Usage:", memory, "%")
    print("Disk Usage:", disk, "%")

    print("\n--- Status ---")

    if cpu > cpu_th:
        print("CPU ALERT!")
    else:
        print("CPU is in safe state")

    if memory > mem_th:
        print("Memory ALERT!")
    else:
        print("Memory is in safe state")

    if disk > disk_th:
        print("Disk ALERT!")
    else:
        print("Disk is in safe state")


cpu_th, mem_th, disk_th = get_thresholds()
check_system(cpu_th, mem_th, disk_th)
