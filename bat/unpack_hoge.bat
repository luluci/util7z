@echo off
@setlocal

cd /D %~dp0
cd ..

set RUN_CMD=""
set SCRIPT_FILE=util7z\unpacker_hoge.py

if exist ".venv" (
	set RUN_CMD=pipenv run python %SCRIPT_FILE% %1%
) else (
	set RUN_CMD=python %SCRIPT_FILE% %1%
)

@echo %RUN_CMD%
%RUN_CMD%

@rem @pause
@endlocal
