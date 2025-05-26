# DF Audio Forensics

A comprehensive web-based tool for audio forgery detection using background noise analysis.

## Features

- Upload and analyze WAV audio files
- Advanced forgery detection using multiple techniques:
  - Background noise analysis
  - ENF (Electrical Network Frequency) analysis
  - Spectral discontinuity detection
  - Noise level consistency analysis
- Detailed visual results with interactive components
- Modern, responsive user interface with animations
- Comprehensive analysis reports

## Requirements

- Python 3.8 or higher
- Flask and dependencies (see requirements.txt)
- Web browser

## Installation

### On Windows

1. Clone or download this repository
2. Navigate to the project directory
3. Run the setup script:
   ```
   run.bat
   ```

### On Linux (including Kali Linux)

1. Clone or download this repository
2. Navigate to the project directory
3. Make the setup script executable:
   ```
   chmod +x run.sh
   ```
4. Run the setup script:
   ```
   ./run.sh
   ```

### Using Docker

1. Clone or download this repository
2. Navigate to the project directory
3. Build and run with Docker Compose:
   ```
   docker-compose up -d
   ```
4. The application will be available at `http://localhost:8000`

For more detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

## Manual Setup

If you prefer to set up the project manually:

1. Create a virtual environment:

   ```
   python -m venv venv
   ```

2. Activate the virtual environment:

   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with a secret key:

   ```
   SECRET_KEY=your_secret_key_here
   ```

5. Run the setup check to verify everything is configured properly:

   ```
   python check_setup.py
   ```

6. Run the application:
   - Development mode: `python run.py`
   - Production mode: `gunicorn -c gunicorn.conf.py run:app`

## Usage

1. Start the application using one of the methods above
2. Open your web browser and navigate to:
   - Development mode: `http://127.0.0.1:5000`
   - Production mode: `http://127.0.0.1:8000`
3. Upload a WAV audio file through the web interface
4. View the detailed analysis results

### Test Data

The repository includes a script to generate test audio files for system validation:

```
python create_test_audio.py
```

This will create two WAV files in the `test_audio` directory:

- `clean_audio.wav`: An unmodified audio file
- `tampered_audio.wav`: A modified version with detectable forgery

You can use these files to test the system's detection capabilities.

## Project Structure

```
DF-Audio-Forensics/
├── app/                        # Application package
│   ├── __init__.py             # Application factory
│   ├── views.py                # Route handlers
│   ├── forms.py                # Form definitions
│   ├── audio_analysis.py       # Audio analysis functions
│   ├── static/                 # Static files (CSS, JS, images)
│   │   └── css/
│   │       └── styles.css      # Application styles
│   └── templates/              # HTML templates
│       ├── base.html           # Base template
│       ├── index.html          # Home page
│       ├── results.html        # Analysis results page
│       ├── about.html          # About page
│       └── contact.html        # Contact page
├── instance/                   # Instance-specific files
│   └── uploads/                # Uploaded audio files
├── venv/                       # Virtual environment (created during setup)
├── requirements.txt            # Python dependencies
├── run.py                      # Application entry point
├── run.sh                      # Linux setup script
├── run.bat                     # Windows setup script
├── gunicorn.conf.py            # Gunicorn configuration
└── README.md                   # Project documentation
```

## Technologies Used

- **Backend**: Flask, Python
- **Audio Analysis**: Librosa, NumPy, SciPy, Matplotlib
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Gunicorn (for production)

## Audio Forensics Methods

This application employs several forensic methods to detect audio forgeries:

### 1. Background Noise Analysis

Every recording environment has a unique acoustic fingerprint in its background noise. This tool analyzes this fingerprint for inconsistencies that may indicate editing or splicing.

### 2. ENF (Electrical Network Frequency) Analysis

The electrical network frequency (50 Hz in Europe, 60 Hz in North America) creates a subtle hum in recordings. This frequency displays minute variations over time that can serve as a timestamp. Inconsistencies in this pattern can reveal tampering.

### 3. Spectral Discontinuity Detection

When audio is spliced, it often creates sudden changes in the frequency spectrum. The tool analyzes the MFCC (Mel-frequency cepstral coefficients) pattern to detect these abrupt changes.

### 4. Noise Level Consistency Analysis

This method examines the consistency of background noise levels throughout a recording. Sudden changes in noise levels can indicate that different recording segments have been combined.

## License

This project is part of a Digital Forensics academic project.

## Acknowledgements

- Flask team for the web framework
- Librosa team for audio analysis capabilities
- Contributors to NumPy, SciPy, and Matplotlib
