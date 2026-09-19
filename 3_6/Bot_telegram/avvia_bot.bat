@echo off
chcp 65001 >nul
title PandaMem bot
cd /d "%~dp0"

REM Python di sistema: preferisco il launcher "py -3" (quello di Spyder e' vecchio)
set PY=python
where py >nul 2>&1 && set PY=py -3

%PY% --version >nul 2>&1
if errorlevel 1 (
    echo Python non trovato. Installalo da https://www.python.org/downloads/ e spunta "Add to PATH".
    pause
    exit /b 1
)

REM Ambiente virtuale dedicato: creato solo la prima volta
if not exist ".venv\Scripts\python.exe" (
    echo Primo avvio: creo l'ambiente virtuale .venv ...
    %PY% -m venv .venv
    if errorlevel 1 (
        echo Creazione dell'ambiente virtuale fallita.
        pause
        exit /b 1
    )
)

set VPY=.venv\Scripts\python.exe

REM Installo le dipendenze solo se manca qualcosa
%VPY% -c "import telegram.ext, requests, bs4, PIL" >nul 2>&1
if errorlevel 1 (
    echo Installo le dipendenze nel venv, un attimo...
    %VPY% -m pip show telegram >nul 2>&1 && %VPY% -m pip uninstall -y telegram >nul
    %VPY% -m pip install -q --upgrade pip
    %VPY% -m pip install -q -r requirements.txt
    if errorlevel 1 (
        echo Installazione dipendenze fallita, controlla la connessione e riprova.
        pause
        exit /b 1
    )
)

echo.
echo Avvio PandaMem... (Ctrl+C per fermarlo)
echo.
%VPY% main.py

echo.
pause
