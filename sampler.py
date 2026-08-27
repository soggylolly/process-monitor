import time
import json

import psutil

import common

class ProcessSampler:
    """Takes snapshots of the busiest processes and appends them to a file"""

    def __init__(self, top_n=common.TOP_N, path=common.SAMPLES_FILE):
        self.top_n = top_n  # How many processes to keep
        self.path = path  # Where to write them
        self.cores = psutil.cpu_count()  # For scaling CPU like Task Manager

        list(psutil.process_iter(['cpu_percent'])) #  Priming the measuremnt of CPU as the first reading is always 0.0 which needs to be thrown away
        time.sleep(1)


    def sample(self):
        """Take one snapshot, append to file and then return the readings"""

        procs = list(psutil.process_iter(common.FIELDS))    #  snapshot of all processes, fetching only the fields in common.FIELDS

        procs = [p for p in procs if p.info['cpu_percent'] is not None]  # Build list from procs when cpu_percent IS NOT None

        procs.sort(key=lambda p: p.info['cpu_percent'], reverse=True)   #  Descending order of CPU usage

        readings = []        # Empty list before loop

        for p in procs[:self.top_n]:   # only list TOP_N busiest processes
            try:   # The process could vanish whilst being read
                cpu = p.info['cpu_percent'] / self.cores  # Scales calcualtion of CPU % to match Task Manager

                mem_mb = p.info['memory_info'].rss / (1024 *1024)  # Converts memory from bytes to MegaBytes

                readings.append({        # Add a plain dict for JSON
                    "pid": p.info['pid'],
                    "name": p.info['name'],
                    "cpu": cpu,
                    "mem_mb": mem_mb,
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):  # Process died or is protected (so skip it)
                continue   # Skip this one, carry on with the rest

        record = {"time": time.time(), "procs": readings}  # Timestamp + readings

        with open(self.path, "a") as output_file: # "a" to append as "w" would overwrite data (meaning no reviews of past logs)

            output_file.write(json.dumps(record) + "\n") # dumps so a newline can be added

        return readings  # so callers can use data directly

def main():
    sampler = ProcessSampler(top_n=10)

    for _ in range(60): # _ is just a throwaway as i just want 60 passes
        sampler.sample()
        print(f"sample {_ + 1} of 60")  # test to ensure program is running
        time.sleep(1)

if __name__ == "__main__":  # Only run when file is ran directly
    main()  # If another file imports this one than skip main()

