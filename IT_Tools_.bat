@echo off
title IT Automation Toolkit - CMD Version
color 0A

:menu
cls
echo ================================
echo        IT TOOLKIT MENU         
echo ================================
echo 1. Network Scanner
echo 2. Ping Checker
echo 3. Check AD User Status
echo 4. Backup Folder
echo 5. Extract Logs for Last X Days
echo 6. Monitor Disk Usage
echo 7. Clean Temp and Prefetch Files
echo 8. View Network Interface Info
echo 9. System Health ^& Troubleshooting
echo 0. Exit
echo ================================
set /p choice=Select an option:

if "%choice%"=="1" goto network_scanner
if "%choice%"=="2" goto ping_checker
if "%choice%"=="3" goto check_ad_user
if "%choice%"=="4" goto backup_folder
if "%choice%"=="5" goto extract_logs
if "%choice%"=="6" goto disk_monitor
if "%choice%"=="7" goto clean_temp
if "%choice%"=="8" goto network_info
if "%choice%"=="9" goto windows_fix
if "%choice%"=="0" exit
goto menu

:network_scanner
cls
set /p baseip=Enter IP base (e.g., 192.168.1):
echo Scanning network...
for /L %%i in (1,1,254) do (
    ping -n 1 -w 100 %baseip%.%%i >nul && echo %baseip%.%%i is up
)
arp -a
pause
goto menu

:ping_checker
cls
set /p host=Enter IP or domain:
ping -n 1 %host%
pause
goto menu

:check_ad_user
cls
set /p user=Enter AD username:
net user %user% /domain
pause
goto menu

:backup_folder
cls
set /p source=Enter source folder path:
set /p dest=Enter destination base folder:
set datetime=%date:~10,4%-%date:~4,2%-%date:~7,2%_%time:~0,2%-%time:~3,2%
set datetime=%datetime: =0%
set destfolder=%dest%\backup_%datetime%
xcopy "%source%" "%destfolder%" /E /I /H /Y
echo Backup completed to: %destfolder%
pause
goto menu

:extract_logs
cls
set /p days=Enter number of days to go back:
set /p logtype=Enter log type (System/Application/Security):
set logtype=%logtype:~0,1%%logtype:~1%
powershell -Command "Get-WinEvent -LogName %logtype% | Where-Object { $_.TimeCreated -gt (Get-Date).AddDays(-%days%) } | Select-Object TimeCreated, Id, LevelDisplayName, Message -First 50 | ForEach-Object { '[Time]: ' + $_.TimeCreated; '[ID]: ' + $_.Id; '[Level]: ' + $_.LevelDisplayName; '[Message]: ' + $_.Message; '---' } | Out-File -Encoding UTF8 logs_%logtype%.txt"
notepad logs_%logtype%.txt
pause
goto menu

:disk_monitor
cls
echo Disk usage per drive (in GB and %% used):
echo ------------------------------------------
powershell -Command "Get-PSDrive -PSProvider FileSystem | ForEach-Object { $used = ($_.Used / 1GB); $free = ($_.Free / 1GB); $total = ($used + $free); if ($total -ne 0) { $percent = [math]::Round(($used / $total) * 100, 1); Write-Host $('Drive: ' + $_.Name + ' | Used: ' + [math]::Round($used,1) + ' GB | Free: ' + [math]::Round($free,1) + ' GB | Usage: ' + $percent + '%') } }"
pause
goto menu

:clean_temp
cls
echo Cleaning temporary files...
del /q /s %TEMP%\*
del /q /s C:\Windows\Temp\*
del /q /s C:\Windows\Prefetch\*
echo Done.
pause
goto menu

:network_info
cls
ipconfig /all
echo.
echo Wi-Fi Info:
for /f "tokens=2 delims=:" %%i in ('netsh wlan show interfaces ^| findstr " SSID"') do set ssid=%%i
set ssid=%ssid:~1%
echo Connected SSID: %ssid%
for /f "delims=: tokens=1,*" %%a in ('netsh wlan show profile name="%ssid%" key=clear ^| findstr "Key Content"') do (
    echo Wi-Fi Password: %%b
)
pause
goto menu

:windows_fix
cls
echo Running System Health & Troubleshooting...
echo ========================================
echo 1. Run SFC Scan
echo 2. Run DISM Restore Health
echo 3. Fix Print Spooler Issues
echo 4. List Drivers
echo 0. Return to Main Menu
echo ========================================
set /p fixchoice=Select an option:

if "%fixchoice%"=="1" (
    sfc /scannow
    pause
)
if "%fixchoice%"=="2" (
    DISM /Online /Cleanup-Image /RestoreHealth
    pause
)
if "%fixchoice%"=="3" (
    net stop spooler
    del /q /f /s %systemroot%\System32\spool\PRINTERS\*.*
    net start spooler
    echo ✅ Print Spooler restarted and cleaned.
    pause
)
if "%fixchoice%"=="4" (
    driverquery
    pause
)
if "%fixchoice%"=="0" goto menu
goto windows_fix
