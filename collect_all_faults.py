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
    print(f"correct = '{correct_out}'")
    
    faults = []
    for byte_idx in range(4):
        for fault_val in [0x01, 0x02]:
            gdb_cmd = f"""
break *0x401ac0
run
continue 8
set {{char}}($rsp+0x60+{byte_idx}) = {{char}}($rsp+0x60+{byte_idx}) ^ {fault_val}
continue 20
quit
"""
            out = get_output(gdb_cmd)
            print(f"faults.append('{out}')")

if __name__ == "__main__":
    main()
