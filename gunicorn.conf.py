# Gunicorn configuration file for production

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = 3
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 5

# Restart workers after this many requests, to help control memory leaks
max_requests = 1000
max_requests_jitter = 100

# Logging
errorlog = "/var/log/gunicorn/error.log"
accesslog = "/var/log/gunicorn/access.log"
loglevel = "info"

# Process naming
proc_name = "avanti_django"

# Server mechanics
daemon = False
pidfile = "/var/run/gunicorn/avanti.pid"
user = "www-data"
group = "www-data"
umask = 0

# SSL (uncomment when SSL certificates are configured)
# keyfile = "/path/to/private.key"
# certfile = "/path/to/certificate.crt"
