@echo off
setlocal
pushd "%~dp0"

IF NOT EXIST "%IPY_PATH%"  set IPY_PATH=%~dp0..\..\external\IronPython
IF NOT EXIST "%IPY_PATH%"  for %%I in (ipy.exe) do @IF EXIST "%%~dp$PATH:I" set IPY_PATH=%%~dp$PATH:I
IF NOT EXIST "%IPY_PATH%"  set IPY_PATH=%ProgramFiles%\IronPython 2.7
IF NOT EXIST "%IPY_PATH%"  set IPY_PATH=%ProgramFiles(x86)%\IronPython 2.7
IF NOT EXIST "%IPY_PATH%" (
	Echo ipy.exe not found on PATH or in common folders.  Aborting
	goto exit
)

set PATH=%~dp0;%PATH%
set IRONPYTHONPATH=%~dp0;%IPY_PATH%;%IPY_PATH%\lib

call "%IPY_PATH%\ipy64.exe" ..\..\examples\%~n0\Program.py

:exit
popd
endlocal