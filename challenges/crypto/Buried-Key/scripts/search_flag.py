import re

def get_all_payloads(log_file):
    # Regex to match: (timestamp) interface ID [length] data...
    pattern = re.compile(r'\(\d+\.\d+\)\s+\S+\s+([0-9A-F]+)\s+\[\d+\]\s+(.*)')
    
    id_payloads = {} # can_id -> list of completed payloads
    current_transfers = {} # can_id -> {length, data, expected_sn}
    
    with open(log_file, 'r') as f:
        for line in f:
            match = pattern.match(line)
            if not match:
                continue
            
            can_id = match.group(1).lower()
            data = bytes.fromhex(match.group(2))
            pci = data[0]
            
            if (pci & 0xF0) == 0x00: # Single Frame
                length = pci & 0x0F
                payload = data[1:1+length]
                if can_id not in id_payloads: id_payloads[can_id] = []
                id_payloads[can_id].append(payload)
                
            elif (pci & 0xF0) == 0x10: # First Frame
                length = ((pci & 0x0F) << 8) | data[1]
                current_transfers[can_id] = {
                    'total_length': length,
                    'data': bytearray(data[2:]),
                    'expected_sn': 1
                }
            elif (pci & 0xF0) == 0x20: # Consecutive Frame
                if can_id in current_transfers:
                    sn = pci & 0x0F
                    # We should check SN but for simplicity let's just append
                    current_transfers[can_id]['data'].extend(data[1:])
                    # Check if finished (this is a bit naive but works for UDS if we know the length)
                    if len(current_transfers[can_id]['data']) >= current_transfers[can_id]['total_length']:
                        payload = current_transfers[can_id]['data'][:current_transfers[can_id]['total_length']]
                        if can_id not in id_payloads: id_payloads[can_id] = []
                        id_payloads[can_id].append(payload)
                        del current_transfers[can_id]

    return id_payloads

log_path = 'challange/can/I-Saw-Our-Time-Pass/can.log'
all_data = get_all_payloads(log_path)

for can_id, payloads in all_data.items():
    for i, p in enumerate(payloads):
        # Look for flag in payload
        if b'flag' in p.lower():
            print(f"ID: {can_id}, Payload {i}: {p}")
            ascii_str = "".join([chr(b) if 0x20 <= b <= 0x7e else "." for b in p])
            print(f"ASCII: {ascii_str}")
