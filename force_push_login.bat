@echo off
echo Github Giris Bilgilerini Sifirliyor...
"C:\Program Files\Git\cmd\git.exe" credential-manager uninstall
"C:\Program Files\Git\cmd\git.exe" credential-manager install

echo.
echo Github'a Yukleniyor... (Lutfen ekrana gelen giris penceresini kullanin)
"C:\Program Files\Git\cmd\git.exe" push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo HATA OLDU! Lutfen bu ekrani kapatmayin ve hatayi okuyun.
) else (
    echo.
    echo ISLEM BASARILI!
)
pause
