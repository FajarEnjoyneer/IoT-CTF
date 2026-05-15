import re

def get_full_flag_from_fc(log_file):
    # Regex untuk menangkap Flow Control (PCI 30) pada semua ID
    pattern = re.compile(r'\((\d+\.\d+)\)\s+\S+\s+([0-9A-F]+)\s+\[\d+\]\s+30\s+([0-9A-F]{2})\s+([0-9A-F]{2})')
    
    stream = []
    with open(log_file, 'r') as f:
        for line in f:
            match = pattern.match(line)
            if match:
                ts = float(match.group(1))
                bs = int(match.group(3), 16)
                stmin = int(match.group(4), 16)
                # Kumpulkan kedua parameter sebagai karakter
                stream.append((ts, bs))
                stream.append((ts + 0.000001, stmin)) # Tambahkan offset kecil agar urut
    
    stream.sort()
    
    # Filter hanya printable ASCII yang masuk akal
    flag_candidate = "".join([chr(b) for ts, b in stream if 32 <= b <= 126])
    return flag_candidate

log_path = 'challange/can/I-Saw-Our-Time-Pass/can.log'
full_text = get_full_flag_from_fc(log_path)
print(f"Full Text Extracted:\n{full_text}")

# Cari pola flag{...}
import re
match = re.search(r'flag\{[^\}]+\}', full_text)
if match:
    print(f"\n[!] FLAG FOUND: {match.group(0)}")
else:
    print("\n[!] Flag belum ditemukan. Mencoba teknik lain...")
