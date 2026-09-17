# Process Monitor

Watches which programs are running on a computer, recording the CPU % and memory each one is using, showing the results in a browser. Groundwork for my final year project for spotting oddly behaving programs.

## The files

- `sampler.py` - Records ten busiest programs once a second for a minute into `samples.jsonl`
- `analyse.py` - Reads file back and reports the process using the highest CPU %
- `app.py` - Web page showing the ten busiest processes refreshing every 5 seconds
- `monitor.py` - The original version which prints to the terminal instead
- `common.py` - Settings shared by other programs
- `sockets/` - A small server and client that sends messages to each other over a network
- `notes/proc_reader.py` - Reads process information straight from `/proc` which shows what psutil does behind the scenes (Linux only)

## What you need

Python 3.12 or later

    pip install -r requirements.txt

## How to run

Record a minute of data 

    python sampler.py

Find the peak in recorded data

    python analyse.py

Start web page, then open http://127.0.0.1:5000/processes

    python app.py

## Tested using

Windows 11 and a VirtualBox running Ubuntu. The same code runs on both without any changes

## Limitations

- Socket clients address is hardcoded so needs to be edited by hand on each machine
- No authentication or encryption on echo server meaning anything can connect
- CPU and memory say nothign about network activity (Program could be uploading a file steadily using almost no CPU)
- Web page writes a line to `samples.jsonl` every time it refreshes even if data isn't wanted
- No automated tests