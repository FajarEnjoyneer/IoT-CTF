import re

def get_flag_per_id(log_file):
    pattern = re.compile(r'\((\d+\.\d+)\)\s+\S+\s+([0-9A-F]+)\s+\[\d+\]\s+(.*)')
    
    id_chars = {} # can_id -> list of chars
    current_transfers = {}
    
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
                if can_id not in id_chars: id_chars[can_id] = []
                id_chars[can_id].append(chr(payload[1]))
    
    return id_chars

log_path = 'challange/can/I-Saw-Our-Time-Pass/can.log'
id_data = get_flag_per_id(log_path)

for cid, chars in id_data.items():
    s = "".join(chars)
    print(f"\nID {cid}:")
    print(s[:200]) # Print first 200 chars
    if 'flag{' in s:
        flags = re.findall(r'flag\{.*?\}', s)
        print(f"FOUND FLAG in ID {cid}: {flags}")
