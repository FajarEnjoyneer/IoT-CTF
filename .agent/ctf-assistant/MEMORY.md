# Memori & Progress CTF

## Lokasi Target
Semua tantangan berada di folder: `challenges/`

## Daftar Tantangan & Status
| ID | Nama Tantangan | Kategori | Status | Flag | Catatan |
|---|---|---|---|---|---|
| 03 | I-Saw-Our-Time-Pass | Automotive | Sedang Berjalan | - | Ditemukan PW1 & PW2 di parameter Flow Control; flag kemungkinan tersembunyi di dalam payload terenkripsi/terkompresi UDS 0x36. |

## Temuan Penting (General)
- **Flag Format**: `FLAG{...}` atau `flag{...}` (Case Sensitive).
- **Scoring**: Dynamic scoring (Base: 1000).

## Snippet & Perintah Berguna
### CAN Utilities
```bash
# Sniffing CAN traffic
candump can0

# Injecting packet
cansend can0 123#DEADBEEF
```

### Firmware Analysis
```bash
# Extracting firmware
binwalk -e firmware.bin
```

## Kredensial yang Ditemukan
(Kosong)

---

## Strategic Next Steps (Current Focus)
*Belum ada tantangan aktif. Silakan masukkan file ke folder `challange/` untuk memulai.*
