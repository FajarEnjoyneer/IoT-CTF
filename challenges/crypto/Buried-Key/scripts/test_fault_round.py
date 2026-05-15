import subprocess
import re

def get_output(gdb_command):
    with open("gdb_script", "w") as f:
        f.write(gdb_command)
    
    process = subprocess.Popen(
        ["gdb", "-batch", "-x", "gdb_script", "--args", "challange/crypto/Buried-Key/buried_key", "00000000000000000000000000000000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()
    match = re.search(r"([0-9a-f]{32})", stdout)
    if match:
        return match.group(1)
    return None

def main():
    correct_out = get_output("run\n")
    print(f"Correct: {correct_out}")
    
    # Try different continue values to hit Round 9
    for c in [8]:
        print(f"Testing continue {c}...")
        gdb_cmd = f"""
break *0x401ac0
run
continue {c}
set {{char}}($rsp+0x60) = {{char}}($rsp+0x60) ^ 0x01
continue 20
quit
"""
        out = get_output(gdb_cmd)
        print(f"Result: {out}")

if __name__ == "__main__":
    main()
