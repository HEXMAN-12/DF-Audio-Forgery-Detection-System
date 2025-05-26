#!/bin/bash

# Exit script if any command fails
set -e

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create instance directory and upload folder if they don't exist
echo "Setting up instance directory..."
mkdir -p instance/uploads

# Generate a random secret key for Flask
if [ ! -f .env ]; then
    echo "Creating .env file with secret key..."
    python -c "import secrets; print(f'SECRET_KEY={secrets.token_hex(16)}')" > .env
fi

# Run the application with Gunicorn
echo "Starting the application..."
gunicorn -c gunicorn.conf.py run:app
