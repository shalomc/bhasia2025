:: Block Python in Excel, April 2025
:: This script disables the Python in Excel feature by modifying the registry settings.
:: It sets the PythonFunctionWarnings value to 2, which disables the feature.
::   0 = allow (default)
::   1 = warn
::   2 = block

reg add HKCU\software\policies\microsoft\office\16.0\excel\security /v PythonFunctionWarnings /t REG_DWORD /d 2 /f
