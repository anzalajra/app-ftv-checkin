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

5. **Auto-Run Saat Startup (Menggunakan Task Scheduler - Direkomendasikan)**
   - Untuk memastikan aplikasi dimulai segera saat komputer menyala, gunakan Task Scheduler:
     - Buka PowerShell sebagai Administrator (klik kanan pada PowerShell dan pilih "Run as Administrator")
     - Jalankan script setup:
       ```powershell
       cd app-ftv-checkin
       .\setup_startup.ps1
       ```
     - Script ini akan membuat task scheduler yang menjalankan aplikasi secara otomatis saat login
   
   **Cara Lama (Tidak Direkomendasikan - Lambat ~20 detik):**
   - Alternatif lama menggunakan folder Startup:
      - Buat shortcut dari file `film_televisi_checkin.py`.
      - Pindahkan shortcut ke folder **Startup**:
        ```bash
        shell:startup
        ```
      - Metode ini memiliki delay sekitar 20 detik setelah desktop siap

---

## Fitur Keamanan

- **Mode Fullscreen**: Aplikasi berjalan dalam mode fullscreen untuk mencegah akses ke aplikasi lain
- **Always On Top**: Window aplikasi selalu berada di atas untuk memastikan user tidak bisa mengakses aplikasi lain
- **Timer Aktif**: Menampilkan durasi penggunaan komputer dalam format hh:mm:ss

---

## Cara Uninstall

4. **Hapus Folder Aplikasi Lokal**
   - Jika ingin menghapus aplikasi, cukup hapus folder proyek dari komputer Anda:
     ```bash
     del /F /Q C:\path\to\app-ftv-checkin
     ```

2. **Hapus Task Scheduler Entry (Jika Menggunakan Task Scheduler)**
   - Buka PowerShell sebagai Administrator
   - Jalankan script untuk menghapus task:
     ```powershell
     cd app-ftv-checkin
     .\remove_startup.ps1
     ```

3. **Hapus Shortcut dari Startup (Jika Menggunakan Metode Lama)**
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