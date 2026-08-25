import time
import json

import psutil

import common

CORES = psutil.cpu_count()  # Fetch core count to scale cpu usage like task managers

def main():
    list(psutil.process_iter(['cpu_percent'])) #  Priming the measuremnt of CPU as the first reading is always 0.0 which needs to be thrown away
    time.sleep(1)

    for _ in range(60): # _ is just a throwaway as i just want 60 passes

        procs = list(psutil.process_iter(common.FIELDS))    #  snapshot of all processes, fetching only the fields in common.FIELDS

        procs = [p for p in procs if p.info['cpu_percent'] is not None]  # Build list from procs when cpu_percent IS NOT None

        procs.sort(key=lambda p: p.info['cpu_percent'], reverse=True)   #  Descending order of CPU usage

        top_ten = []        # Empty list before loop

        for p in procs[:common.TOP_N]:   # only list TOP_N busiest processes
            try:   # The process could vanish whilst being read
                cpu = p.info['cpu_percent'] / CORES  # Scales calcualtion of CPU % to match Task Manager

                mem_mb = p.info['memory_info'].rss / (1024 *1024)  # Converts memory from bytes to MegaBytes

                top_ten.append({        # Add a plain dict for JSON
                    "pid": p.info['pid'],
                    "name": p.info['name'],
                    "cpu": cpu,
                    "mem_mb": mem_mb,
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):  # Process died or is protected (so skip it)
                continue   # Skip this one, carry on with the rest

        sample = {"time": time.time(), "procs": top_ten}  # Timestamp + top ten processes

        with open(common.SAMPLES_FILE, "a") as output_file: # "a" to append as "w" would overwrite data (meaning no reviews of past logs)

            output_file.write(json.dumps(sample) + "\n") # dumps so a newline can be added

        print(f"sample {_ + 1} of 60")  # test to ensure program is running
        time.sleep(1)

if __name__ == "__main__":  # Only run when file is ran directly
    main()  # If another file imports this one than skip main()