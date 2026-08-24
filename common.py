"""
Shared settings for sampler.py and analyse.py

The file only holds values to import so the filename is only written in one place
"""

SAMPLES_FILE = "samples.jsonl"  
FIELDS = ['pid', 'name', 'cpu_percent', 'memory_info']
TOP_N = 10
IDLE_NAME = "System Idle Process"