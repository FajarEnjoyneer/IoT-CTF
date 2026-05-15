import re

def get_flag_from_sequence(log_file):
    pattern = re.compile(r'\((\d+\.\d+)\)\s+\S+\s+([0-9A-F]+)\s+\[\d+\]\s+(.*)')
    
    # We want to track the second byte of UDS 36 Service
    # UDS 36 XX ... -> XX is the character
    
    chars = []
    current_transfers = {} # can_id -> {total_length, data}
    
    with open(log_file, 'r') as f:
        for line in f:
            match = pattern.match(line)
            if not match: continue
            
            ts = float(match.group(1))
            can_id = match.group(2).lower()
            data = bytes.fromhex(match.group(3))
            pci = data[0]
            
            payload = None
            if (pci & 0xF0) == 0x00: # Single Frame
                payload = data[1:1+(pci & 0x0F)]
            elif (pci & 0xF0) == 0x10: # First Frame
                length = ((pci & 0x0F) << 8) | data[1]
                current_transfers[can_id] = {'len': length, 'data': bytearray(data[2:])}
            elif (pci & 0xF0) == 0x20: # Consecutive Frame
                if can_id in current_transfers:
                    current_transfers[can_id]['data'].extend(data[1:])
                    if len(current_transfers[can_id]['data']) >= current_transfers[can_id]['len']:
                        payload = current_transfers[can_id]['data'][:current_transfers[can_id]['len']]
                        del current_transfers[can_id]
            
            if payload and len(payload) >= 2 and payload[0] == 0x36:
                char_byte = payload[1]
                chars.append((ts, char_byte))
    
    # Sort by timestamp
    chars.sort()
    
    res = ""
    for ts, b in chars:
        res += chr(b)
    return res

log_path = 'challange/can/I-Saw-Our-Time-Pass/can.log'
full_string = get_flag_from_sequence(log_path)
print(f"Full String:\n{full_string}")

# Look for flag{...} in the full string
if 'flag{' in full_string:
    import re
    flag = re.findall(r'flag\{.*?\}', full_string)
    print(f"Found Flags: {flag}")
