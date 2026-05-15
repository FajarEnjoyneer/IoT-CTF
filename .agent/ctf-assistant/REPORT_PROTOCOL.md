# Protokol Pelaporan & Strategi Lanjutan

Gunakan protokol ini untuk mendokumentasikan setiap sesi analisis tantangan.

---

## [SKENARIO A] - FLAG BERHASIL DITEMUKAN
Jika Flag ditemukan, buat laporan singkat di `MEMORY.md` dengan format:
- **Tantangan**: [Nama Soal]
- **Flag**: `FLAG{...}`
- **Langkah Penemuan**:
    1. [Langkah 1]
    2. [Langkah 2]
    3. dst.
- **Alat yang Digunakan**: [Misal: binwalk, pwntools]
- **Bukti (Snippet)**: [Output perintah atau screenshot hex]

---

## [SKENARIO B] - FLAG BELUM DITEMUKAN (STUCK)
Jika setelah analisis mendalam Flag belum ditemukan, Agen **WAJIB** memberikan minimal 3 saran strategis berdasarkan temuan saat ini:

### 1. Analisis Hambatan
Jelaskan mengapa Flag belum ditemukan (misal: file terenkripsi, biner diproteksi canary/PIE, atau protokol tidak dikenal).

### 2. Saran Langkah Alternatif (Pivoting)
Berikan opsi langkah selanjutnya, contoh:
- **Opsi 1 (Bruteforce)**: Mencoba serangan dictionary pada password yang ditemukan.
- **Opsi 2 (Deep RE)**: Melakukan dekompilasi fungsi tertentu di Ghidra yang terlihat mencurigakan.
- **Opsi 3 (OSINT)**: Mencari dokumen teknis vendor terkait untuk mencari default password.

### 3. Rekomendasi Alat Baru
Sebutkan alat yang belum digunakan yang mungkin bisa memecahkan masalah tersebut.

---

### Instruksi untuk Agen:
Setiap kali Anda selesai melakukan serangkaian perintah tanpa hasil, Anda **HARUS** menutup respon Anda dengan bagian **"Saran Strategis Selanjutnya"** mengikuti format di atas.
