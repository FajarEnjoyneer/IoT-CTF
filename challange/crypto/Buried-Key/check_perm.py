import struct

with open("round1_tboxes.bin", "rb") as f:
    data = f.read()

for i in range(16):
    table_data = data[i*1024 : (i+1)*1024]
    entries = struct.unpack("<256I", table_data)
    
    for b in range(4):
        byte_vals = [(e >> (b*8)) & 0xff for e in entries]
        is_perm = len(set(byte_vals)) == 256
        if is_perm:
            print(f"Table {i}, Byte {b} is a permutation")
        else:
            print(f"Table {i}, Byte {b} has {len(set(byte_vals))} unique values")
