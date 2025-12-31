# Film dan Televisi User Check-In

**Aplikasi Python untuk check-in user komputer di lingkungan Film dan Televisi.**

## Fitur
- User diwajibkan check-in dengan nama dan NIM.
- Monitoring durasi penggunaan dengan pip window.
- Opsi Shutdown dan Sleep yang terintegrasi.
- Desain modern dengan opsi wallpaper yang bisa disesuaikan.

---

## Cara Install di Windows 11

1. **Pastikan Python Terinstal**
   - Periksa Python:
     ```bash
     python --version
     ```
   - Unduh Python jika belum tersedia: [python.org](https://www.python.org/).

2. **Clone Repository**
   - Buka Command Prompt atau terminal:
     ```bash
     git clone https://github.com/anzalajra/app-ftv-checkin.git
     ```
   - Lalu pindah ke folder proyek:
     ```bash
     cd app-ftv-checkin
     ```

3. **Instal Dependensi**
   - Instal PyQt5:
     ```bash
     pip install pyqt5
     ```

4. **Jalankan Aplikasi**
   - Jalankan aplikasi menggunakan perintah:
     ```bash
     python film_televisi_checkin.py
     ```

5. **Auto-Run Saat Startup (Opsional)**
   - Otomatiskan aplikasi di startup:
     - Buat shortcut dari file `film_televisi_checkin.py`.
     - Pindahkan shortcut ini ke folder **Startup**:
       ```bash
       shell:startup
       ```

---

## Cara Uninstall

1. **Hapus Folder Aplikasi Lokal**
   - Hapus folder proyek aplikasi:
     ```bash
     del /F /Q C:\path\to\app-ftv-checkin
     ```

2. **Hapus Shortcut dari Startup (Jika Ada)**
   - Buka folder Startup:
     ```bash
     shell:startup
     ```
   - Hapus shortcut aplikasi.

3. **Hapus Dependensi PyQt5 (Jika Diperlukan)**
   - Bersihkan dependensi PyQt5:
     ```bash
     pip uninstall pyqt5
     ```

4. **Catatan Penting**
   - Jangan hapus Python jika masih ada aplikasi lain yang membutuhkannya.

---

© 2026 Divisi IT FTV UPI