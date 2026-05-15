import math

def entropy(data):
    if not data:
        return 0
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    ent = 0
    for count in counts:
        if count > 0:
            p = count / len(data)
            ent -= p * math.log2(p)
    return ent

with open("buried_key", "rb") as f:
    data = f.read()

best_ent = 0
best_offset = 0
for i in range(0, len(data) - 16):
    ent = entropy(data[i:i+16])
    if ent > best_ent:
        best_ent = ent
        best_offset = i

# Print top 10 entropy blocks
blocks = []
for i in range(0, len(data) - 16):
    ent = entropy(data[i:i+16])
    blocks.append((ent, i))

blocks.sort(reverse=True)
for ent, offset in blocks[:20]:
    print(f"Offset 0x{offset:x}: {data[offset:offset+16].hex()} (ent: {ent})")
