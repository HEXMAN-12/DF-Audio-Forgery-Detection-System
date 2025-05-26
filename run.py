import os

# Try to import dotenv, but continue even if it's not installed
try:
    from dotenv import load_dotenv
    # Load environment variables from .env file, if it exists
    load_dotenv()
except ImportError:
    print("Note: python-dotenv not installed. Environment variables will not be loaded from .env file.")
    # Set a default secret key if none is available
    if not os.environ.get('SECRET_KEY'):
        os.environ['SECRET_KEY'] = 'dev-key-for-testing'

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
