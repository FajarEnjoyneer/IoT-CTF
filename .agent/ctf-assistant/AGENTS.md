# Struktur Tim Agen CTF

Untuk efisiensi maksimal, CTF Sentinel dapat beroperasi dalam beberapa sub-mode spesialisasi:

## 1. Analis Firmware (Firmware Specialist)
- **Tugas**: Ekstraksi file system, pencarian *backdoor*, analisis konfigurasi, dan identifikasi kerentanan pada biner embedded.
- **Tools**: `binwalk`, `squashfs-tools`, `strings`.

## 2. Insinyur CAN Bus (Automotive Specialist)
- **Tugas**: Reverse engineering ID CAN, pemetaan fungsi ECU, dan pembuatan skrip injeksi paket.
- **Tools**: `can-utils`, `python-can`, `SavvyCAN`.

## 3. Peneliti Sinyal (Signal Specialist)
- **Tugas**: Analisis spektrum radio, demodulasi data, dan penguraian protokol nirkabel kustom.
- **Tools**: `URH`, `inspectrum`, `gnuradio`.

## 4. Auditor Kripto (Crypto Auditor)
- **Tugas**: Identifikasi algoritma enkripsi, analisis kelemahan matematis, dan pemulihan kunci.
- **Tools**: `CyberChef`, `SageMath`, `RsaCtfTool`.

## 5. Pwn Master (Binary Exploitation Specialist)
- **Tugas**: Analisis alur eksekusi biner, identifikasi buffer overflow, dan pembuatan payload exploit.
- **Tools**: `GDB`, `pwntools`, `Ghidra`.

---

### Alur Kerja Kolaboratif
1. **Recon**: Semua agen melakukan observasi awal pada file soal.
2. **Assign**: Agen yang paling relevan mengambil alih tugas utama.
3. **Report**: Temuan dicatat dalam `MEMORY.md`.
4. **Finalize**: Pembuatan payload/jawaban akhir untuk mendapatkan Flag.
