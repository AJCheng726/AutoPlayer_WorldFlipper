@echo on
SET CONDA_SHLVL=
REM don't inherit these from the build env setup
SET _CE_CONDA=
SET _CE_M=
SET _CONDA_EXE=
SET
REM CALL stuff is necessary because conda in condabin is a bat script
REM    running bat files within other bat files requires CALL or else
REM    the outer script (our test script) exits when the inner completes
CALL %PREFIX%\condabin\conda_hook.bat
CALL conda.bat activate base
FOR /F "delims=" %%i IN ('python -c "import sys; print(sys.version_info[0])"') DO set "PYTHON_MAJOR_VERSION=%%i"
SET TEST_PLATFORM=win
FOR /F "delims=" %%i IN ('python -c "import random as r; print(r.randint(0,4294967296))"') DO set "PYTHONHASHSEED=%%i"
where conda
CALL conda info
CALL conda create -y -p .\built-conda-test-env python=3.8
CALL conda.bat activate .\built-conda-test-env
ECHO %CONDA_PREFIX%
IF NOT "%CONDA_PREFIX%"=="%CD%\built-conda-test-env" EXIT /B 1
FOR /F "delims=" %%i IN ('python -c "import sys; print(sys.version_info[1])"') DO set "ENV_PYTHON_MINOR_VERSION=%%i"
IF NOT "%ENV_PYTHON_MINOR_VERSION%" == "8" EXIT /B 1
CALL conda deactivate
SET MSYSTEM=MINGW%ARCH%
SET MSYS2_PATH_TYPE=inherit
SET CHERE_INVOKING=1
FOR /F "delims=" %%i IN ('cygpath.exe -u "%PREFIX%"') DO set "PREFIXP=%%i"
bash -lc "source %PREFIXP%/Scripts/activate"
REM 2019-04-16 MCS disabling this to get 4.6.13 out.  Tests pass on CI, but fail when building packages on concourse.
REM py.test tests -m "not integration and not installed" -vv