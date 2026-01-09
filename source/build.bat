@echo off
echo ========================================
echo   Building Film Televisi Check-In App
echo ========================================
echo. 

REM Cek apakah pyinstaller ada
where pyinstaller >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo PyInstaller tidak ditemukan!
    echo. 
    echo Menginstall PyInstaller... 
    pip install pyinstaller
    echo. 
)

REM Build aplikasi
echo Building...
python -m PyInstaller --onefile --windowed --name "FTV-CheckIn" film_televisi_checkin. py

if exist "dist\FTV-CheckIn.exe" (
    echo. 
    echo ========================================
    echo   Build SUKSES!
    echo   File: dist\FTV-CheckIn.exe
    echo ========================================
    echo.
    echo Copy file ini ke C:\checkin\ untuk update
) else (
    echo.
    echo ========================================
    echo   Build GAGAL!
    echo   Cek error message di atas
    echo ========================================
)

pause