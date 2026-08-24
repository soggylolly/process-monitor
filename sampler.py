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
import json
import psutil

import common

CORES = psutil.cpu_count()  # Fetch core count to scale cpu usage like task managers

def main():
    list(psutil.process_iter(['cpu_percent'])) #  Priming the measuremnt of CPU as the first reading is always 0.0 which needs to be thrown away
    time.sleep(1)

    for _ in range(60): # _ is just a throwaway as i just want 60 passes

        procs = list(psutil.process_iter(common.FIELDS))    #  snapshot of each process named

        procs.sort(key=lambda p: p.info['cpu_percent'], reverse=True)   #  Descending order of CPU usage

        top_ten = []        # Empty list before loop

        for p in procs[:common.TOP_N]:   # only list 10 busiest processes

            cpu = p.info['cpu_percent'] / CORES  # Scales calcualtion of CPU % to match Task Manager

            mem_mb = p.info['memory_info'].rss / (1024 *1024)  # Converts memory from bytes to MegaBytes

            top_ten.append({        # Add a plain dict for JSON
                "pid": p.info['pid'],
                "name": p.info['name'],
                "cpu": cpu,
                "mem_mb": mem_mb,
            })

        sample = {"time": time.time(), "procs": top_ten}  # Timestamp + top ten processes

        with open(common.SAMPLES_FILE, "a") as output_file: # "a" to append as "w" would overwrite data (meaning no reviews of past logs)

            output_file.write(json.dumps(sample) + "\n") # dumps so a newline can be added

        print(f"sample {_ + 1} of 60")  # test to ensure program is running (TO BE REMOVED)
        time.sleep(1)

if __name__ == "__main__":  # Only run when file is ran directly
    main()  # If another file imports this one than skip main()