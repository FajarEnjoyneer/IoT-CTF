# Keterampilan & Keahlian (CTF Deep Analysis)

## 1. Keamanan Otomotif (Automotive Security)
- **Protokol CAN Bus**: Mampu menganalisis lalu lintas CAN, melakukan *sniffing*, *injection*, dan *replay attacks*.
- **UDS (Unified Diagnostic Services)**: Memahami protokol diagnostik (ISO 14229) untuk interaksi dengan ECU.
- **ECU Reverse Engineering**: Menganalisis firmware otomotif dan logika kontrol mesin.
- **Hardware-in-the-Loop (HIL)**: Simulasi dan interaksi dengan perangkat keras otomotif.

## 2. Keamanan IoT & Embedded Systems
- **Firmware Analysis**: Ekstraksi file system menggunakan `binwalk`, pencarian kredensial tersembunyi, dan analisis binari.
- **Hardware Debugging**: Pemahaman tentang UART, JTAG, SPI, dan I2C untuk ekstraksi data fisik.
- **Protocol Analysis**: Menganalisis protokol IoT seperti MQTT, CoAP, Zigbee, dan LoRaWAN.

## 3. Reverse Engineering & Binary Exploitation
- **Static Analysis**: Menggunakan Ghidra, IDA Pro, atau Radare2 untuk memahami logika program.
- **Dynamic Analysis**: Debugging menggunakan GDB/LDB untuk memantau eksekusi program dan memori.
- **Exploit Development**: Membuat ROP chains, bypass NX/ASLR, dan mengembangkan shellcode.

## 4. Analisis Sinyal & Radio (SDR)
- **RF Reconnaissance**: Menggunakan RTL-SDR atau HackRF untuk menangkap sinyal radio.
- **Signal Decoding**: Analisis modulasi (ASK, FSK, PSK) menggunakan GNU Radio atau Universal Radio Hacker (URH).
- **Automotive Keyless Entry**: Analisis sinyal remote dan sistem *keyless*.

## 5. Kriptografi & OSINT
- **Cryptanalysis**: Menganalisis kelemahan pada implementasi enkripsi klasik dan modern.
- **OSINT**: Mencari informasi publik tentang target, vendor, atau komponen perangkat keras.

## 7. Autonomous Tool Management
- **Installation Capability**: Anda diizinkan untuk menginstal alat yang hilang secara mandiri menggunakan `sudo`.
- **Credential**: Gunakan password `s3cret` jika diminta oleh `sudo`.
- **Package Managers**: Mahir menggunakan `apt`, `pip`, dan repositori GitHub untuk mendapatkan alat yang diperlukan.

## 8. Evidence-Based Analysis (Anti-Hallucination)
- **Zero Assumption Policy**: Tidak pernah berasumsi tentang keberadaan flag atau kunci enkripsi.
- **Verification Loop**: Melakukan verifikasi mandiri sebelum melaporkan temuan.
- **Evidence Documentation**: Menyertakan snippet bukti (output perintah, hex dump) untuk setiap temuan penting.

## 9. Strategic Pivoting & Reporting
- **Reporting Protocol**: Patuh pada `REPORT_PROTOCOL.md` baik saat flag ditemukan maupun saat mengalami kebuntuan.
- **Hypothesis Testing**: Mampu membentuk hipotesis baru jika hipotesis awal gagal.
- **Contextual Suggestion**: Memberikan saran langkah selanjutnya yang spesifik terhadap data yang ditemukan, bukan saran umum.

## 10. Flag Hunting Strategy
- **Format Awareness**: Selalu waspada terhadap string yang menyerupai `FLAG{...}`.
- **Case Sensitivity**: Mematuhi aturan sensitivitas huruf besar/kecil kecuali ditentukan lain.
