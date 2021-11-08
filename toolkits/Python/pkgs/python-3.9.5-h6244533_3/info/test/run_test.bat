



echo on
IF %ERRORLEVEL% NEQ 0 exit /B 1
set
IF %ERRORLEVEL% NEQ 0 exit /B 1
python -V
IF %ERRORLEVEL% NEQ 0 exit /B 1
2to3 -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
pydoc -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
python run_test.py
IF %ERRORLEVEL% NEQ 0 exit /B 1
set "PIP_NO_BUILD_ISOLATION=False"
IF %ERRORLEVEL% NEQ 0 exit /B 1
set "PIP_NO_DEPENDENCIES=True"
IF %ERRORLEVEL% NEQ 0 exit /B 1
set "PIP_IGNORE_INSTALLED=True"
IF %ERRORLEVEL% NEQ 0 exit /B 1
set "PIP_NO_INDEX=True"
IF %ERRORLEVEL% NEQ 0 exit /B 1
set "PIP_CACHE_DIR=%CONDA_PREFIX%/pip_cache"
IF %ERRORLEVEL% NEQ 0 exit /B 1
set "TEMP=%CONDA_PREFIX%/tmp"
IF %ERRORLEVEL% NEQ 0 exit /B 1
mkdir "%TEMP%"
IF %ERRORLEVEL% NEQ 0 exit /B 1
python -Im ensurepip --upgrade --default-pip
IF %ERRORLEVEL% NEQ 0 exit /B 1
python -c "from zoneinfo import ZoneInfo; from datetime import datetime; dt = datetime(2020, 10, 31, 12, tzinfo=ZoneInfo('America/Los_Angeles')); print(dt.tzname())"
IF %ERRORLEVEL% NEQ 0 exit /B 1
python -m venv test-venv
IF %ERRORLEVEL% NEQ 0 exit /B 1
if exist %PREFIX%\\Scripts\\pydoc exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if exist %PREFIX%\\Scripts\\idle exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if exist %PREFIX%\\Scripts\\2to3 exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Scripts\\pydoc-script.py exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Scripts\\idle-script.py exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Scripts\\2to3-script.py exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Scripts\\idle.exe exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Scripts\\2to3.exe exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Scripts\\pydoc.exe exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
pushd tests
IF %ERRORLEVEL% NEQ 0 exit /B 1
pushd distutils
IF %ERRORLEVEL% NEQ 0 exit /B 1
python setup.py install -v -v
IF %ERRORLEVEL% NEQ 0 exit /B 1
python -c "import foobar"
IF %ERRORLEVEL% NEQ 0 exit /B 1
popd
IF %ERRORLEVEL% NEQ 0 exit /B 1
pushd cmake
IF %ERRORLEVEL% NEQ 0 exit /B 1
run_cmake_test.bat 3.9.5
IF %ERRORLEVEL% NEQ 0 exit /B 1
popd
IF %ERRORLEVEL% NEQ 0 exit /B 1
pushd processpoolexecutor-max_workers-61
IF %ERRORLEVEL% NEQ 0 exit /B 1
python ppe.py
IF %ERRORLEVEL% NEQ 0 exit /B 1
popd
IF %ERRORLEVEL% NEQ 0 exit /B 1
popd
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
