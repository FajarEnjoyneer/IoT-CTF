import re

def get_payloads_for_id(log_file, target_id):
    pattern = re.compile(r'\((\d+\.\d+)\)\s+\S+\s+([0-9A-F]+)\s+\[\d+\]\s+(.*)')
    current_transfers = {}
    payloads = []
    with open(log_file, 'r') as f:
        for line in f:
            match = pattern.match(line)
            if not match: continue
            can_id = match.group(2).lower()
            if can_id != target_id.lower(): continue
            data = bytes.fromhex(match.group(3))
            pci = data[0]
            if (pci & 0xF0) == 0x10:
                length = ((pci & 0x0F) << 8) | data[1]
                current_transfers[can_id] = {'len': length, 'data': bytearray(data[2:])}
            elif (pci & 0xF0) == 0x20:
                if can_id in current_transfers:
                    current_transfers[can_id]['data'].extend(data[1:])
                    if len(current_transfers[can_id]['data']) >= current_transfers[can_id]['len']:
                        payloads.append(bytes(current_transfers[can_id]['data'][:current_transfers[can_id]['len']]))
                        del current_transfers[can_id]
    return payloads

log_path = 'challange/can/I-Saw-Our-Time-Pass/can.log'
p700 = get_payloads_for_id(log_path, '700')

# Combine Payload 1 and 2 (ignoring UDS header 36 XX)
if len(p700) >= 2:
    full_zip = p700[0][2:] + p700[1][2:]
    with open('full_700.zip', 'wb') as f:
        f.write(full_zip)
    print("Combined ZIP saved to full_700.zip")
