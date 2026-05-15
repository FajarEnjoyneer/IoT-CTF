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
    # Correct ciphertext
    correct_out = get_output("run\n")
    print(f"Correct: {correct_out}")
    
    faulty_outputs = []
    # Try faulting the first byte of round 9 input (which is round 8 output)
    for fault_val in [0x01, 0x02, 0x40, 0x80, 0xff]:
        gdb_cmd = f"""
break *0x401ac0
run
continue 7
# Round 9 start (9th hit, so continue 8 times total including the first 'run')
# Wait, 'run' hits the first time. 'continue 1' hits the second time.
# So 'continue 7' hits the 9th time.
set {{char}}($rsp+0x60) = {{char}}($rsp+0x60) ^ {fault_val}
continue 10
quit
"""
        # Wait, there are 10 rounds total.
        # Round 1 (1st hit), Round 2 (2nd), ..., Round 9 (9th), Round 10 (not a loop hit?)
        # Let's check the loop.
        # Round 1..9 are in the loop. Round 10 is after the loop.
        # So we want to fault at the 9th hit of 0x401ac0.
        
        out = get_output(gdb_cmd)
        if out and out != correct_out:
            print(f"Faulty ({fault_val}): {out}")
            faulty_outputs.append(out)
        else:
            print(f"Failed to get faulty output for {fault_val}: {out}")

if __name__ == "__main__":
    main()
