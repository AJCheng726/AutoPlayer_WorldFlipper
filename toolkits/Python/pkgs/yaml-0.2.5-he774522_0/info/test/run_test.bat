



if not exist "%LIBRARY_INC%\\yaml.h" exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist "%LIBRARY_LIB%\\yaml.lib" exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist "%LIBRARY_BIN%\\yaml.dll" exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
