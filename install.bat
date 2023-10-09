@ECHO OFF

pyinstaller --noconsole --onefile pdf_sign.py

SET var=%cd%
set DIR=%var%
copy %DIR%\password.txt %DIR%\dist\password.txt

pyinstaller --noconsole --onefile pdf_sign_lock.py
