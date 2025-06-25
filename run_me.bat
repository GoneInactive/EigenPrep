@echo off
setlocal
set CONFIG_FILE=config\config.yaml
set DEBUG_FLAG=false

REM Check if requirements are installed by trying to import dearpygui and pandas
python -c "import dearpygui.dearpygui, pandas" 2>NUL
if errorlevel 1 (
    echo Installing required Python packages...
    pip install -r requirements.txt
)

if exist %CONFIG_FILE% (
    for /f "tokens=2 delims=: " %%a in ('findstr /i "debug:" %CONFIG_FILE%') do set DEBUG_FLAG=%%a
)

color 71

if /i "%DEBUG_FLAG%"=="true" (
    echo ">>> DEBUG MODE ON <<<"
    python -m src.main
    @PAUSE
) else (
    pythonw -m src.main
)
endlocal 