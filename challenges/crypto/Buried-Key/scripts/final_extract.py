import re

def extract_zip_from_id(log_file, target_id):
    pattern = re.compile(r'\((\d+\.\d+)\)\s+\S+\s+([0-9A-F]+)\s+\[\d+\]\s+(.*)')
    
    current_transfers = {}
    
    with open(log_file, 'r') as f:
        for line in f:
            match = pattern.match(line)
            if not match: continue
            
            can_id = match.group(2).lower()
            if can_id != target_id.lower(): continue
            
            data = bytes.fromhex(match.group(3))
            pci = data[0]
            
            if (pci & 0xF0) == 0x10: # First Frame
                length = ((pci & 0x0F) << 8) | data[1]
                current_transfers[can_id] = {'len': length, 'data': bytearray(data[2:])}
            elif (pci & 0xF0) == 0x20: # Consecutive Frame
                if can_id in current_transfers:
                    current_transfers[can_id]['data'].extend(data[1:])
                    if len(current_transfers[can_id]['data']) >= current_transfers[can_id]['len']:
                        payload = current_transfers[can_id]['data'][:current_transfers[can_id]['len']]
                        # Check for ZIP magic
                        zip_start = payload.find(b'PK\x03\x04')
                        if zip_start != -1:
                            return payload[zip_start:]
                        del current_transfers[can_id]
    return None

log_path = 'challange/can/I-Saw-Our-Time-Pass/can.log'
zip_data = extract_zip_from_id(log_path, '700')
if zip_data:
    with open('challenge_flag.zip', 'wb') as f:
        f.write(zip_data)
    print("ZIP extracted to challenge_flag.zip")
else:
    print("ZIP not found")
