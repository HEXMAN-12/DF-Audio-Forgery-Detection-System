# Gunicorn configuration file

# Number of worker processes
workers = 4

# Socket to bind
bind = '0.0.0.0:8000'

# Worker class
worker_class = 'sync'

# Timeout (in seconds)
timeout = 60

# Log level
loglevel = 'info'
