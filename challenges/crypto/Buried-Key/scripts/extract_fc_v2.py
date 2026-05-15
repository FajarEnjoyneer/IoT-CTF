import re

def extract_flow_control_per_id(log_file, target_id):
    pattern = re.compile(r'\((\d+\.\d+)\)\s+\S+\s+([0-9A-F]+)\s+\[\d+\]\s+(.*)')
    res = ""
    with open(log_file, 'r') as f:
        for line in f:
            match = pattern.match(line)
            if not match: continue
            can_id = match.group(2).lower()
            if can_id != target_id.lower(): continue
            data = bytes.fromhex(match.group(3))
            if data[0] == 0x30:
                # Flow Control: 30 BS STmin
                for b in data[1:3]:
                    if 0x20 <= b <= 0x7e:
                        res += chr(b)
                    elif b != 0:
                        res += f"[{b:02x}]"
    return res

log_path = 'challange/can/I-Saw-Our-Time-Pass/can.log'
for cid in ['708', '709', '70a', '70b']:
    print(f"\nID {cid}: {extract_flow_control_per_id(log_path, cid)}")
