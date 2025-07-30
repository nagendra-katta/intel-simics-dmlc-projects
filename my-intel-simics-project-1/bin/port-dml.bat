@echo off
rem this file will be overwritten by the project setup script
setlocal
set SIMICS_BASE_PACKAGE=C:\Users\nagen\AppData\Local\Programs\Simics\simics-7.38.0
set SIMICS_PYTHON_PACKAGE=C:\Users\nagen\AppData\Local\Programs\Simics\simics-python-7.10.0
if "%SIMICS_PYTHON%"=="" (
    set SIMICS_PYTHON=
)
"C:\Users\nagen\AppData\Local\Programs\Simics\simics-7.38.0\bin\port-dml.bat"  %*
