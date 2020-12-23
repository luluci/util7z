@echo off
@setlocal

cd /D %~dp0
cd ..

set RUN_CMD=""
set SCRIPT_FILE=util7z\packer_hoge.py

if exist ".venv" (
	set RUN_CMD=pipenv run python %SCRIPT_FILE% %*%
) else (
	set RUN_CMD=python %SCRIPT_FILE% %*%
)

@echo %RUN_CMD%
%RUN_CMD%

@pause
@endlocal
