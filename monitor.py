# import psutil
# import time

# # first call to prime the measurement (ignore result)
# for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
#     print(proc.info)

# time.sleep(1)   # wait for 1 second to compare

# # Second call tob give actual readings
# for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
#     print(proc.info)

import time
import psutil

CORES = psutil.cpu_count()

list(psutil.process_iter(['cpu_percent']))
time.sleep(1)

while True:
    procs = list(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']))
    procs.sort(key=lambda p: p.info['cpu_percent'], reverse=True)

    print(f"{'PID':>7}  {'CPU%':>6}  {'MEM MB':>8}  NAME")
    for p in procs[:10]:
        cpu = p.info['cpu_percent'] / CORES
        mem_mb = p.info['memory_info'].rss / (1024 *1024)
        print(f"{p.info['pid']:>7}  {cpu:>6.1f}  {mem_mb:>8.1f}  {p.info['name']}")
        
    time.sleep(1)