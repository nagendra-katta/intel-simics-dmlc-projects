
@echo off
rem this file will be overwritten by the project setup script
setlocal
set SIMICS_BASE_PACKAGE=C:\Users\nagen\AppData\Local\Programs\Simics\simics-7.38.0
set SIMICS_PYTHON_PACKAGE=C:\Users\nagen\AppData\Local\Programs\Simics\simics-python-7.10.0
if "%SIMICS_PYTHON%"=="" (
    set SIMICS_PYTHON=
)
if exist "C:\Users\nagen\simics-projects\my-intel-simics-project-1\.package-list" set SIMICS_EPL=--package-list "C:\Users\nagen\simics-projects\my-intel-simics-project-1\.package-list"
if not exist "C:\Users\nagen\simics-projects\my-intel-simics-project-1\.package-list" set SIMICS_EPL=
"C:\Users\nagen\AppData\Local\Programs\Simics\simics-7.38.0\bin\test-runner.bat" %SIMICS_EPL% --project "C:\Users\nagen\simics-projects\my-intel-simics-project-1" %*
