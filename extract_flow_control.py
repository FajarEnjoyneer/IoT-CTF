import re

def extract_flow_control(log_file):
    pattern = re.compile(r'\((\d+\.\d+)\)\s+\S+\s+([0-9A-F]+)\s+\[\d+\]\s+(.*)')
    
    # We want to track BS (byte 1) and STmin (byte 2) of Flow Control (PCI 30)
    # Flow Control: 30 BS STmin ...
    
    results = []
    
    with open(log_file, 'r') as f:
        for line in f:
            match = pattern.match(line)
            if not match: continue
            
            ts = float(match.group(1))
            can_id = match.group(2).lower()
            data = bytes.fromhex(match.group(3))
            pci = data[0]
            
            if pci == 0x30:
                bs = data[1]
                stmin = data[2]
                if bs != 0: results.append((ts, bs))
                if stmin != 0: results.append((ts, stmin))
    
    # Sort by timestamp
    results.sort()
    
    res = ""
    for ts, b in results:
        if 0x20 <= b <= 0x7e:
            res += chr(b)
        else:
            res += f"[{b:02x}]"
    return res

log_path = 'challange/can/I-Saw-Our-Time-Pass/can.log'
flag_data = extract_flow_control(log_path)
print(f"Extracted String: {flag_data}")
