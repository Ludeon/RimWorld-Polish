@echo off
setlocal
rem Ten launcher należy odpalać z Notes\scripts; output idzie do root dwa poziomy wyżej.
set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%..\.."

py -3 "%SCRIPT_DIR%build_github_release.py" "%REPO_ROOT%"
if errorlevel 1 (
    echo.
    echo Nie udało się spakować.
)
echo.
pause
