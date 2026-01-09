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
   - Periksa versi Python:
     ```bash
     python --version
     ```
   - Jika Python tidak tersedia di sistem, unduh dari situs resmi:
     [python.org](https://www.python.org/).

2. **Instal Dependensi**
   - Gunakan **pip** untuk menginstal dependensi aplikasi (modul PyQt5):
     ```bash
     python -m pip install pyqt5
     ```

3. **Clone Repository**
   - Clone repository GitHub menggunakan perintah berikut:
     ```bash
     git clone https://github.com/anzalajra/app-ftv-checkin.git
     ```
   - Berpindah ke folder hasil clone:
     ```bash
     cd app-ftv-checkin
     ```

4. **Jalankan Aplikasi**
   - Pada Command Prompt, jalankan perintah:
     ```bash
     python film_televisi_checkin.py
     ```

5. **Auto-Run Saat Startup (Opsional)**
   - Otomatiskan aplikasi agar berjalan otomatis saat komputer menyala:
     - Buat shortcut dari file `film_televisi_checkin.py`.
     - Pindahkan shortcut ke folder **Startup**:
       ```bash
       shell:startup
       ```

---

## Cara Uninstall

1. **Hapus Folder Aplikasi Lokal**
   - Jika ingin menghapus aplikasi, cukup hapus folder proyek dari komputer Anda:
     ```bash
     del /F /Q C:\path\to\app-ftv-checkin
     ```

2. **Hapus Shortcut dari Startup (Jika Ada)**
   - Buka folder Startup menggunakan perintah:
     ```bash
     shell:startup
     ```
   - Hapus shortcut aplikasi dari folder tersebut.

3. **Uninstall Library PyQt5 (Opsional)**
   - Jika PyQt5 tidak lagi dibutuhkan di sistem, hapus dengan perintah:
     ```bash
     python -m pip uninstall pyqt5
     ```

---

**Catatan Penting**
- Pastikan untuk tidak menghapus Python jika masih digunakan untuk aplikasi lain di sistem Anda.

© 2026 Divisi IT FTV UPI