@echo on
:: Set env vars that tell distutils to use the compiler that we put on path
SET DISTUTILS_USE_SDK=1
:: This is probably not good. It is for the pre-UCRT msvccompiler.py *not* _msvccompiler.py
SET MSSdk=1

SET "VS_VERSION=16.5"
SET "VS_MAJOR=16"
SET "VS_YEAR=2019"

set "MSYS2_ARG_CONV_EXCL=/AI;/AL;/OUT;/out"
set "MSYS2_ENV_CONV_EXCL=CL"

:: For Python 3.5+, ensure that we link with the dynamic runtime.  See
:: http://stevedower.id.au/blog/building-for-python-3-5-part-two/ for more info
set "PY_VCRUNTIME_REDIST=%PREFIX%\bin\vcruntime140.dll"

:: set CC and CXX for cmake
set "CXX=cl.exe"
set "CC=cl.exe"

set "VSINSTALLDIR="
:: Try to find actual vs2017 installations
for /f "usebackq tokens=*" %%i in (`vswhere.exe -nologo -products * -version ^[16.0^,17.0^] -property installationPath`) do (
  :: There is no trailing back-slash from the vswhere, and may make vcvars64.bat fail, so force add it
  set "VSINSTALLDIR=%%i\"
)
if not exist "%VSINSTALLDIR%" (
    :: VS2019 install but with vs2017 compiler stuff installed
	for /f "usebackq tokens=*" %%i in (`vswhere.exe -nologo -products * -requires Microsoft.VisualStudio.Component.VC.v142.x86.x64 -property installationPath`) do (
	:: There is no trailing back-slash from the vswhere, and may make vcvars64.bat fail, so force add it
	set "VSINSTALLDIR=%%i\"
	)
)
if not exist "%VSINSTALLDIR%" (
set "VSINSTALLDIR=%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Professional\"
)
if not exist "%VSINSTALLDIR%" (
set "VSINSTALLDIR=%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Community\"
)
if not exist "%VSINSTALLDIR%" (
set "VSINSTALLDIR=%ProgramFiles(x86)%\Microsoft Visual Studio\2019\BuildTools\"
)
if not exist "%VSINSTALLDIR%" (
set "VSINSTALLDIR=%ProgramFiles(x86)%\Microsoft Visual Studio\2019\Enterprise\"
)

IF NOT "%CONDA_BUILD%" == "" (
  set "INCLUDE=%LIBRARY_INC%;%INCLUDE%"
  set "LIB=%LIBRARY_LIB%;%LIB%"
  set "CMAKE_PREFIX_PATH=%LIBRARY_PREFIX%;%CMAKE_PREFIX_PATH%"
)


call :GetWin10SdkDir
:: dir /ON here is sorting the list of folders, such that we use the latest one that we have
for /F %%i in ('dir /ON /B "%WindowsSdkDir%\include"') DO (
  if NOT "%%~i" == "wdf" (
    SET WindowsSDKVer=%%~i
  )
)
if errorlevel 1 (
    echo "Didn't find any windows 10 SDK. I'm not sure if things will work, but let's try..."
) else (
    echo Windows SDK version found as: "%WindowsSDKVer%"
)

IF "@cross_compiler_target_platform@" == "win-64" (
  set "target_platform=amd64"
  set "CMAKE_GEN=Visual Studio @VER@ @YEAR@ Win64"
  set "BITS=64"
) else (
  set "target_platform=x86"
  set "CMAKE_GEN=Visual Studio @VER@ @YEAR@"
  set "BITS=32"
)

pushd %VSINSTALLDIR%
set VSCMD_DEBUG=1
CALL "VC\Auxiliary\Build\vcvars%BITS%.bat" -vcvars_ver=14.2 %WindowsSDKVer%
popd

IF "%CMAKE_GENERATOR%" == "" SET "CMAKE_GENERATOR=%CMAKE_GEN%"

:GetWin10SdkDir
call :GetWin10SdkDirHelper HKLM\SOFTWARE\Wow6432Node > nul 2>&1
if errorlevel 1 call :GetWin10SdkDirHelper HKCU\SOFTWARE\Wow6432Node > nul 2>&1
if errorlevel 1 call :GetWin10SdkDirHelper HKLM\SOFTWARE > nul 2>&1
if errorlevel 1 call :GetWin10SdkDirHelper HKCU\SOFTWARE > nul 2>&1
if errorlevel 1 exit /B 1
exit /B 0


:GetWin10SdkDirHelper
@REM `Get Windows 10 SDK installed folder`
for /F "tokens=1,2*" %%i in ('reg query "%1\Microsoft\Microsoft SDKs\Windows\v10.0" /v "InstallationFolder"') DO (
    if "%%i"=="InstallationFolder" (
        SET WindowsSdkDir=%%~k
    )
)
exit /B 0
