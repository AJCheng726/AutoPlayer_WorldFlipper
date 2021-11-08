



sqlite3 --version
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\bin\sqlite3.dll exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\lib\sqlite3.lib exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\include\sqlite3.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
if not exist %PREFIX%\\Library\include\sqlite3ext.h exit 1
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
