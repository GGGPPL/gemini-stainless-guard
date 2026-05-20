import sys, os, re, subprocess

# VERSION: 1.2.1
# Role: Physical Enforcer (Actionable Error Edition)

def get_git_hash(path):
    try:
        res = subprocess.run(["git", "-C", os.path.dirname(path), "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
        return res.stdout.strip()
    except: return "UNKNOWN"

def get_last_logged_version(target_path):
    history_path = os.path.join(os.path.dirname(target_path), "VERSION_HISTORY.md")
    if not os.path.exists(history_path): return None
    try:
        name = os.path.basename(target_path)
        with open(history_path, 'r', encoding='utf-8') as f:
            lines = [l for l in f.readlines() if name in l]
            if lines:
                return lines[-1].split('|')[3].strip()
    except: pass
    return None

def forensic_replace(target, old, new):
    # 1. Physical Integrity Check
    try:
        from gatekeeper import check_physical_compliance
        if not check_physical_compliance():
            # Gatekeeper already prints detailed FIX instructions
            return False
    except: return False

    # 2. Log-based SemVer Enforcement
    last_ver = get_last_logged_version(target)
    if last_ver:
        match = re.search(r"VERSION: (\d+)\.(\d+)\.(\d+)", new)
        if match:
            new_ver_str = f"{match.group(1)}.{match.group(2)}.{match.group(3)}"
            if new_ver_str == last_ver:
                print(f"[IRON_REPLACE] ERROR: Version {new_ver_str} already exists.")
                print(">>> FIX: Increment the version number in your code modification and update VERSION_HISTORY.md.")
                return False

    # 3. Physical Modification
    if not os.path.exists(target): return False
    with open(target, 'r', encoding='utf-8') as f: content = f.read()
    if old not in content:
        print('[IRON_REPLACE] FAIL: String match not found.')
        print(">>> FIX: Ensure 'old_string' exactly matches the current file content (Check Indentation/Spacing).")
        return False

    new_c = content.replace(old, new)
    try:
        is_readonly = not (os.stat(target).st_mode & 0o200)
        if is_readonly: os.chmod(target, 0o666)
        with open(target, 'w', encoding='utf-8', newline='\n') as f: f.write(new_c)
        os.chmod(target, 0o444)
        print(f'SUCCESS: Applied REF: {get_git_hash(target)}')
        return True
    except Exception as e:
        print(f"[IRON_REPLACE] DISK ERROR: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 4: sys.exit(1)
    target_path = sys.argv[1]
    with open(sys.argv[2], 'r', encoding='utf-8') as f: o = f.read()
    with open(sys.argv[3], 'r', encoding='utf-8') as f: n = f.read()
    if forensic_replace(target_path, o, n): sys.exit(0)
    else: sys.exit(1)
