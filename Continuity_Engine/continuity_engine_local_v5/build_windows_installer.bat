@echo off
setlocal
call build_windows_portable.bat
if errorlevel 1 exit /b 1
where iscc >nul 2>nul
if errorlevel 1 (
  echo Inno Setup compiler not found.
  echo Install Inno Setup, then run this script again.
  echo It should provide ISCC.exe on PATH.
  pause
  exit /b 1
)
iscc installer_windows.iss
if errorlevel 1 (
  echo Installer build failed.
  pause
  exit /b 1
)
echo.
echo Installer build complete.
echo Output: installer_dist\ContinuityEngineInstaller_v6.exe
pause
