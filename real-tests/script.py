import sys
import subprocess
import os

for lox_file in filter(lambda f: f.endswith(".lox"), sorted(os.listdir("real-tests"))):
    print(f"$ python3 -m lox real-tests/{lox_file}")
    result = subprocess.run(
        ["python3", "-m", "lox", f"real-tests/{lox_file}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
    )
    out = result.stdout.decode().strip()
    err = result.stderr.decode().strip()
    print(out)
    if err:
        print(f"STDERR: {err}")
    print()
    if "ERROR".lower() in out.lower() or "ERROR".lower() in err.lower() or result.returncode != 0:
        sys.exit(1)
