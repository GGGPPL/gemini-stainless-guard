import os

import hashlib

import json



# Rule Sensor v2.0 - Dual-Layer Compliance Witness

REPO_PATH = r"C:\\Users\\Eric Wang\.gemini\PREVENTION_REPOSITORY.md"

STATE_PATH = r"C:\\Users\\Eric Wang\.gemini\state.json"

VERSION_PATH = r"C:\\Users\\Eric Wang\.gemini\Workspaces\Web_Memory_Bridge\Config\STAINLESS_VERSION.json"

LOCK_FILE = r"C:\\Users\\Eric Wang\.gemini\tmp\anonymous\last_read_repo.timestamp"



def generate_compliance_token():

    if not os.path.exists(REPO_PATH) or not os.path.exists(STATE_PATH) or not os.path.exists(VERSION_PATH):

        print("[ERROR] Physical components missing.")

        return False



    # 1. Physical Read (Mandatory Reading Protocol)

    with open(REPO_PATH, 'r', encoding='utf-8') as f: repo_data = f.read()

    with open(STATE_PATH, 'r', encoding='utf-8') as f: seed = json.load(f).get("SESSION_SEED", "")

    with open(VERSION_PATH, 'r', encoding='utf-8') as f: ver = json.load(f).get("CORE_VERSION", "")



    # 2. Cryptographic Interlock (Rules + Seed + Version Anchor)

    combined = (repo_data + seed + ver).encode('utf-8')

    compliance_hash = hashlib.sha256(combined).hexdigest()



    # 3. Physical State Commit

    with open(LOCK_FILE, 'w', encoding='utf-8') as f:

        f.write(compliance_hash)

    

    print(f"[SENSOR] Compliance verified. Hash: {compliance_hash[:16]}...")

    return True



if __name__ == "__main__":

    generate_compliance_token()

