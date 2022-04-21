del .\release\wanted\* /Q
xcopy .\screen .\release\screen /s/y/i
xcopy .\utils .\release\utils /s/y/i
xcopy .\wanted .\release\wanted /s/y/i
xcopy .\World_Flipper .\release\World_Flipper /s/y/i
xcopy gui.bat .\release\ /y
xcopy *.ini .\release\ /y
xcopy *.exe .\release\ /y
del .\release\screen\* /Q