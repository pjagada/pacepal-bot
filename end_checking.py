import tail
from watcher import Watcher

INSTANCES_DIRECTORY = 'C:/MultiMC/instances'
INSTANCES = ["/1.17.1_1", "/1.17.1_2", "/1.17.1_3"]
LOG_FILE = "/.minecraft/logs/latest.log"

LOG_FILES = [INSTANCES_DIRECTORY + instance + LOG_FILE for instance in INSTANCES]
last_end_lines = {}
for log_file in LOG_FILES:
    last_end_lines[log_file] = ""

def send_pacepal():
	print("peej has entered the end!")

def compare_and_update_line(file, line):
    if last_end_lines[file] != line:
        last_end_lines[file] = line
        send_pacepal()

def check_log_file(file):
	print("log file updated")
	lines = tail(file, 25)
	for line in lines:
		if "has made the advancement [The End?]" in line:
			compare_and_update_line(file, line)

# watchers = [Watcher(log_file, check_log_file, file=log_file) for log_file in log_files]