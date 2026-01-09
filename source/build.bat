@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   Building Film Televisi Check-In App
echo ========================================
echo.

REM Auto detect version dari file Python
set VERSION=unknown

REM Cari baris yang mengandung APP_VERSION dan extract nilainya
for /f "tokens=*" %%a in ('findstr /C:"APP_VERSION" film_televisi_checkin.py') do (
    set LINE=%%a
)

REM Extract version dari LINE (ambil text di antara tanda kutip)
for /f tokens^=2^ delims^=^" %%v in ("!LINE!") do (
    set VERSION=%%v
)

echo Detected Version: v%VERSION%
echo.

REM Validasi version
if "%VERSION%"=="unknown" (
    echo WARNING:  Tidak bisa detect versi otomatis!
    echo.
    set /p VERSION="Masukkan versi manual (contoh: 1.0.0): "
)

REM Cek apakah pyinstaller ada
where pyinstaller >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo PyInstaller tidak ditemukan!
    echo.
    echo Menginstall PyInstaller...
    pip install pyinstaller
    echo.
)

REM Build aplikasi dengan nama + versi
echo Building FTV-CheckIn v%VERSION%...
echo.
python -m PyInstaller --onefile --windowed --name "FTV-CheckIn-v%VERSION%" film_televisi_checkin.py

if exist "dist\FTV-CheckIn-v%VERSION%.exe" (
    echo.
    echo ========================================
    echo   Build SUKSES! 
    echo   Version:  %VERSION%
    echo   File: dist\FTV-CheckIn-v%VERSION%.exe
    echo ========================================
    
    REM Cleanup temp files
    echo.
    echo Cleaning up temp files...
    if exist "build" rmdir /s /q build
    if exist "FTV-CheckIn-v%VERSION%.spec" del "FTV-CheckIn-v%VERSION%.spec"
    echo Done!
    
    echo.
    echo Copy file dari dist\ ke C:\checkin\ untuk update
) else (
    echo.
    echo ========================================
    echo   Build GAGAL!
    echo   Cek error message di atas
    echo ========================================
)

echo.
pause