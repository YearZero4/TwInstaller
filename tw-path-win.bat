@echo off
move tw.bat C:\Users\%USERNAME%\.tw
move *.py C:\Users\%USERNAME%\.tw
powershell -command "[Environment]::SetEnvironmentVariable('PATH', [Environment]::GetEnvironmentVariable('PATH', 'User') + ';C:\Users\%USERNAME%\.tw', 'User')"

echo.
echo Ahora puedes ejecutar desde cualquier lugar:
echo.
echo tw [OPCION]
pause>nul