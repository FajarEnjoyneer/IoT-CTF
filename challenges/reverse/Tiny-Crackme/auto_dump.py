import subprocess
import time
import os

# Start QEMU in debug mode
# -s (gdb on 1234), -S (freeze at startup)
qemu_proc = subprocess.Popen([
    "qemu-system-arm",
    "-machine", "mps2-an385",
    "-cpu", "cortex-m3",
    "-kernel", "kernel",
    "-nographic",
    "-serial", "stdio",
    "-semihosting",
    "-semihosting-config", "enable=on,target=native",
    "-s", "-S"
], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Give QEMU a moment to start
time.sleep(1)

# Start GDB
gdb_script = """
target remote :1234
set architecture arm
break *0x13234
continue
# After reaching the breakpoint, dump the transformation result
x/32bx $sp+8
# And the target
x/32bx $r0
detach
quit
"""
with open("dump.gdb", "w") as f:
    f.write(gdb_script)

gdb_proc = subprocess.Popen([
    "gdb-multiarch", "-x", "dump.gdb", "--batch", "kernel"
], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Wait for QEMU to reach the input prompt (it won't until we continue in GDB)
# But we already did 'continue' in GDB script.
# So QEMU should be running now.

time.sleep(2) # Wait for it to print "Input flag: "
qemu_proc.stdin.write("FLAG{012345678901234567890123456789}\n")
qemu_proc.stdin.flush()

# Wait for GDB to finish
stdout, stderr = gdb_proc.communicate()
print("GDB Output:")
print(stdout)
print(stderr)

qemu_proc.terminate()
