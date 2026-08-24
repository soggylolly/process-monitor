import json

import common

def main():
    peak_cpu = 0   # storage for highest cpu usage seen so far
    peak_name = None  # storage for process name

    with open(common.SAMPLES_FILE) as input_file:  # read mode is the default
        for line in input_file:                # one line = one sample
            sample = json.loads(line)          # text into dict

            for proc in sample["procs"]:       # ten processes per sample

                if proc["name"] == common.IDLE_NAME:
                    continue                                # this skips System Idle Process as not a real program

                if proc["cpu"] > peak_cpu:     # Is the cpu usage highest so far
                    peak_cpu = proc["cpu"]     # store it
                    peak_name = proc["name"]

    print(f"Peak CPU: {peak_name} at {peak_cpu:.1f}%")    # After loops finish print result

if __name__ == "__main__":  # Only run when file is ran directly
    main()  # If another file imports this one than skip main()