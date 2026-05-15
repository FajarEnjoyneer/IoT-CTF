import re

def extract_isotp(log_file, target_id):
    # Regex to match: (timestamp) interface ID [length] data...
    pattern = re.compile(r'\(\d+\.\d+\)\s+\S+\s+([0-9A-F]+)\s+\[\d+\]\s+(.*)')
    
    payload = bytearray()
    expected_sn = 1
    
    with open(log_file, 'r') as f:
        for line in f:
            match = pattern.match(line)
            if not match:
                continue
            
            can_id = match.group(1).lower()
            if can_id != target_id.lower():
                continue
            
            data = bytes.fromhex(match.group(2))
            pci = data[0]
            
            if (pci & 0xF0) == 0x10: # First Frame
                length = ((pci & 0x0F) << 8) | data[1]
                # In UDS TransferData (36), the first two bytes of payload are 36 and counter
                # but ISO-TP FF has 2 bytes PCI. So payload starts at index 2.
                payload = bytearray(data[2:])
                expected_sn = 1
                print(f"Start FF: ID={can_id}, Total Length={length}")
            elif (pci & 0xF0) == 0x20: # Consecutive Frame
                sn = pci & 0x0F
                # Note: sequence number 0 comes after 15
                payload.extend(data[1:])
                expected_sn = (sn + 1) % 16

    return payload

log_path = 'challange/can/I-Saw-Our-Time-Pass/can.log'

for cid in ['703', '700', '701']:
    print(f"\nExtracting from ID: {cid}")
    data = extract_isotp(log_path, cid)
    if data:
        # Find ZIP magic PK..
        zip_start = data.find(b'PK\x03\x04')
        if zip_start != -1:
            # We skip the UDS header (36 XX)
            output_file = f'extracted_{cid}.zip'
            with open(output_file, 'wb') as f:
                f.write(data[zip_start:])
            print(f"Saved to {output_file}, size={len(data[zip_start:])}")
        else:
            print("ZIP magic not found in payload")
