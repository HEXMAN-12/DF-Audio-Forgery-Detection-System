# Deployment Guide

This guide provides instructions for deploying the DF Audio Forensics application in different environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Kali Linux](#kali-linux)
3. [Production Deployment](#production-deployment)
   - [Systemd Service](#systemd-service)
   - [Nginx Configuration](#nginx-configuration)
4. [Docker Deployment](#docker-deployment)
5. [Troubleshooting](#troubleshooting)

## Local Development

For local development, use the provided scripts:

### Windows

```
run.bat
```

### Linux

```
chmod +x run.sh
./run.sh
```

The application will be available at `http://127.0.0.1:5000` in development mode.

## Kali Linux

To deploy on Kali Linux:

1. Clone the repository

   ```
   git clone <repository-url> DF-Audio-Forensics
   cd DF-Audio-Forensics
   ```

2. Make the script executable

   ```
   chmod +x run.sh
   ```

3. Run the application

   ```
   ./run.sh
   ```

4. Access the application at `http://127.0.0.1:8000`

### Dependencies on Kali Linux

If you encounter issues with dependencies, you may need to install additional system packages:

```
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip python3-venv libsndfile1 ffmpeg portaudio19-dev
```

## Production Deployment

### Systemd Service

For a more robust deployment using systemd:

1. Create a systemd service file:

   ```
   sudo nano /etc/systemd/system/dfaudio.service
   ```

2. Add the following content (adjust paths as needed):

   ```
   [Unit]
   Description=DF Audio Forensics Web Application
   After=network.target

   [Service]
   User=<your-username>
   WorkingDirectory=/path/to/DF-Audio-Forensics
   Environment="PATH=/path/to/DF-Audio-Forensics/venv/bin"
   ExecStart=/path/to/DF-Audio-Forensics/venv/bin/gunicorn -c gunicorn.conf.py run:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start the service:

   ```
   sudo systemctl enable dfaudio
   sudo systemctl start dfaudio
   ```

4. Check the status:
   ```
   sudo systemctl status dfaudio
   ```

### Nginx Configuration

To serve the application through Nginx:

1. Install Nginx:

   ```
   sudo apt-get install nginx
   ```

2. Create a new site configuration:

   ```
   sudo nano /etc/nginx/sites-available/dfaudio
   ```

3. Add the following configuration:

   ```
   server {
       listen 80;
       server_name your_domain.com;  # Replace with your domain or IP

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       # Configure max upload size
       client_max_body_size 16M;
   }
   ```

4. Enable the site and restart Nginx:
   ```
   sudo ln -s /etc/nginx/sites-available/dfaudio /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## Docker Deployment

You can also deploy the application using Docker:

1. Create a Dockerfile in the project root:

```
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create instance folder
RUN mkdir -p instance/uploads

# Set environment variables
ENV FLASK_APP=run.py
ENV SECRET_KEY=your_secret_key_here

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "-c", "gunicorn.conf.py", "run:app"]
```

2. Build and run the Docker container:

```
docker build -t dfaudio .
docker run -p 8000:8000 dfaudio
```

The application will be available at `http://localhost:8000`.

## Troubleshooting

### Dependency Issues

If you encounter issues with audio libraries:

```
# On Debian/Ubuntu/Kali:
sudo apt-get install -y libsndfile1 ffmpeg portaudio19-dev

# On Red Hat/CentOS:
sudo yum install -y libsndfile ffmpeg portaudio-devel
```

### Permission Issues

If you experience permission issues with the uploads directory:

```
sudo chown -R <your-user>:<your-group> instance/uploads
sudo chmod 755 instance/uploads
```

### Memory Issues

If you're processing large audio files and encounter memory issues, adjust the Gunicorn worker settings in `gunicorn.conf.py`:

```python
# Reduce number of workers
workers = 2

# Use threads instead
threads = 4

# Adjust worker class
worker_class = 'gthread'
```
