@echo off
echo Setting up DF Audio Forensics application...

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Update pip and setuptools first
echo Updating pip and setuptools...
pip install --upgrade pip setuptools

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM If pip install fails, try to install essential packages
IF %ERRORLEVEL% NEQ 0 (
    echo Attempting to install essential packages individually...
    pip install Flask Werkzeug
    pip install python-dotenv
)

REM Create instance directory and upload folder if they don't exist
echo Setting up instance directory...
if not exist instance mkdir instance
if not exist instance\uploads mkdir instance\uploads

REM Generate a random secret key for Flask if .env doesn't exist
if not exist .env (
    echo Creating .env file with secret key...
    python -c "import secrets; print(f'SECRET_KEY={secrets.token_hex(16)}')" > .env
)

REM Run the application
echo Starting the application...
python run.py

pause
