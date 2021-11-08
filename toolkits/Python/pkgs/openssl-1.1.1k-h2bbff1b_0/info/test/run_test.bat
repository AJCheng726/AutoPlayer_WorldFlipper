



copy NUL checksum.txt
IF %ERRORLEVEL% NEQ 0 exit /B 1
openssl sha256 checksum.txt
IF %ERRORLEVEL% NEQ 0 exit /B 1
python -c "from six.moves import urllib; urllib.request.urlopen('https://pypi.org')"
IF %ERRORLEVEL% NEQ 0 exit /B 1
exit /B 0
