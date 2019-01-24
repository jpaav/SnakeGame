:: Check for Python Installation
python --version 2>NUL
if errorlevel 1 goto errorNoPython

python -m pip install pygame numpy google-api-python-client oauth2client

python main.py

:: Once done, exit the batch file -- skips executing the errorNoPython section
goto:eof

:errorNoPython
echo.
echo Error^: Python not installed