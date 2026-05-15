# Toolbox CTF Sentinel

## Automotive Tools
- **can-utils**: `candump`, `cansniffer`, `cansend`, `canplayer`.
- **SavvyCAN**: Analisis visual lalu lintas CAN.
- **Caring Caribou**: Framework untuk audit keamanan otomotif.

## IoT & Firmware Tools
- **binwalk**: Ekstraksi dan analisis firmware.
- **qemu**: Emulasi arsitektur CPU yang berbeda (MIPS, ARM) untuk menjalankan biner IoT.
- **Flashrom**: Membaca dan menulis chip memori flash.
- **Ghidra**: Reverse engineering framework dari NSA.

## Binary & Exploitation Tools
- **pwntools**: Library Python untuk pengembangan exploit yang cepat.
- **GDB + GEF/Peda**: Debugger dengan ekstensi untuk analisis biner.
- **Ropper/RP++**: Mencari gadget untuk ROP chains.

## Signal Analysis Tools
- **Universal Radio Hacker (URH)**: Tool investigasi protokol nirkabel.
- **GNU Radio**: Software development toolkit untuk pemrosesan sinyal radio.
- **Inspectrum**: Tool visualisasi sinyal frekuensi radio.

## Networking & Protocol Tools
- **Wireshark**: Analisis paket jaringan dan protokol IoT.
- **Scapy**: Manipulasi paket tingkat rendah dalam Python.
- **Nmap**: Network discovery dan security auditing.

## Cryptography Tools
- **CyberChef**: "The Cyber Swiss Army Knife" untuk encoding, decoding, dan enkripsi sederhana.
- **RsaCtfTool**: Mencari serangan pada kunci RSA yang lemah.
- **Hashcat/John the Ripper**: Pemecahan hash password.

---

## Prosedur Instalasi (Autonomous)
Jika sebuah alat belum terinstal, gunakan perintah berikut (contoh untuk `can-utils`):
```bash
echo "s3cret" | sudo -S apt-get update
echo "s3cret" | sudo -S apt-get install -y can-utils
```
Pastikan untuk memeriksa ketersediaan alat dengan `which <tool>` sebelum mencoba menginstal.
