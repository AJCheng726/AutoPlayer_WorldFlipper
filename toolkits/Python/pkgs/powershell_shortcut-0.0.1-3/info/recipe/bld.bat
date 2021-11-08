set MENU_DIR=%PREFIX%\Menu
IF NOT EXIST (%MENU_DIR%) mkdir %MENU_DIR%

copy %RECIPE_DIR%\Iconleak-Atrous-PSConsole.ico %MENU_DIR%
if errorlevel 1 exit 1

copy %RECIPE_DIR%\menu-windows-ps.json %MENU_DIR%\powershell_shortcut.json
if errorlevel 1 exit 1
