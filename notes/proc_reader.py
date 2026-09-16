"""Linux only, reads process names and memory straight from /proc, using nothing but open(), and produces the same figures as psutil"""
import os

PAGE_SIZE = 4096  # byte per memory page on x86-64

for entry in os.listdir("/proc"):
    if not entry.isdigit():  # only numbered folders are processes
        continue
    try:
        with open(f"/proc/{entry}/comm") as f:
            name = f.read().strip()
        with open(f"/proc/{entry}/statm") as f:
            pages = int(f.read().split()[1])  # field 2 = resident pages
    except (FileNotFoundError, PermissionError):
        continue  # vanished, or not ours to read

    mem_mb = pages * PAGE_SIZE / (1024 * 1024)
    print(f"{entry:>7}  {mem_mb:>8.1f}  {name}")