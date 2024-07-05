import psutil


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    memory_info = psutil.virtual_memory()
    return memory_info.percent


def get_disk_usage():
    disk_info = psutil.disk_usage('/')
    return disk_info.percent


if __name__ == "__main__":
    print(f"CPU Usage: {get_cpu_usage()}%")
    print(f"Memory Usage: {get_memory_usage()}%")
    print(f"Disk Usage: {get_disk_usage()}%")
