



menuinst -h
IF %ERRORLEVEL% NEQ 0 exit /B 1
menuinst --version
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
