# Memori & Progress CTF

## Lokasi Target
Semua tantangan berada di folder: `challange/`

## Daftar Tantangan & Status
| ID | Nama Tantangan | Kategori | Status | Flag | Catatan |
|---|---|---|---|---|---|
| 02 | VIN-Hunter | Automotive | Selesai | flag{v1n_r3ad_succ3ss} | Berhasil direkonstruksi dari DID 0xF190 via ISO-TP |

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
