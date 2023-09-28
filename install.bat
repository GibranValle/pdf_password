@ECHO OFF

pyinstaller --noconsole --onefile pdf_password.py

SET var=%cd%
set DIR=%var%
copy %DIR%\password.txt %DIR%\dist\password.txt