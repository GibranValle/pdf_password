@ECHO OFF

pyinstaller --onefile pdf_sign.py
pause
//SET var=%cd%
//set DIR=%var%
//copy %DIR%\password.txt %DIR%\dist\password.txt
