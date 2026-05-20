import sys
import os
import hashlib
import json
import subprocess

# VERSION: 1.1.1
# Role: Gatekeeper - The Stainless Shield (Actionable Error Edition)

USER_PROFILE = os.environ.get("USERPROFILE", "C:\\Users\\Default")
GEMINI_DIR = os.path.join(USER_PROFILE, ".gemini")
REPO_PATH = os.path.join(GEMINI_DIR, "PREVENTION_REPOSITORY.md")
STATE_PATH = os.path.join(GEMINI_DIR, "state.json")
VERSION_PATH = os.path.join(GEMINI_DIR, "Workspaces", "Web_Memory_Bridge", "Config", "STAINLESS_VERSION.json")
LOCK_FILE = os.path.join(GEMINI_DIR, "tmp", "anonymous", "last_read_repo.timestamp")

def check_physical_compliance():
    # 1. Watchman Integrity
    try:
        sys.path.append(os.path.dirname(__file__))
        from watchman_sensor import check_watchman_alive
        if not check_watchman_alive():
            print("[GATEKEEPER] ERROR: Background Sync service is OFFLINE.")
            print(">>> FIX: Run 'python System_Core/sync.py' manually or check PID.")
            return False
    except: return False

    # 2. Git Cleanliness Audit
    try:
        status = subprocess.run(["git", "-C", GEMINI_DIR, "status", "--porcelain", "System_Core/"], capture_output=True, text=True)
        if status.stdout.strip():
            print("[GATEKEEPER] ERROR: Uncommitted core changes detected.")
            print(">>> FIX: Commit current changes to System_Core before making new modifications.")
            return False
    except: return False

    # 3. Cryptographic Compliance
    if not os.path.exists(LOCK_FILE):
        print("[GATEKEEPER] ERROR: Compliance token missing.")
        print(">>> FIX: Run 'python System_Core/rule_sensor.py' to generate token.")
        return False
    
    with open(LOCK_FILE, 'r', encoding='utf-8') as f: stored_hash = f.read().strip()

    try:
        with open(REPO_PATH, 'r', encoding='utf-8') as f: repo_data = f.read()
        with open(STATE_PATH, 'r', encoding='utf-8') as f: seed = json.load(f).get("SESSION_SEED", "")
        with open(VERSION_PATH, 'r', encoding='utf-8') as f: ver = json.load(f).get("CORE_VERSION", "")
        expected_hash = hashlib.sha256((repo_data + seed + ver).encode('utf-8')).hexdigest()
        if stored_hash != expected_hash:
            print("[GATEKEEPER] ERROR: Compliance token MISMATCH.")
            print(">>> FIX: Re-read PREVENTION_REPOSITORY.md and run 'python System_Core/rule_sensor.py'.")
            return False
    except: return False

    print("[GATEKEEPER] Physical alignment verified.")
    return True

if __name__ == "__main__":
    if not check_physical_compliance(): sys.exit(1)
    sys.exit(0)
