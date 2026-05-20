import os

# VERSION: 1.0.0
# Role: Watchman Sensor - Physical Health Monitor

def check_watchman_alive():
    try:
        # Check for python.exe or pythonw.exe running sync.py
        output = os.popen('wmic process where "name=\'python.exe\' or name=\'pythonw.exe\'" get CommandLine').read()
        if "sync.py" in output:
            return True
        print("[WATCHMAN ERROR] Background Sync service (sync.py) is OFFLINE.")
        return False
    except Exception:
        return False

if __name__ == "__main__":
    if check_watchman_alive():
        print("WATCHMAN: ACTIVE")
    else:
        print("WATCHMAN: OFFLINE")
