import multiprocessing

workers = 1
bind = "0.0.0.0:8000"
loglevel = "info"
timeout = 120
keepalive = 5
workers_per_core = 1
workers = multiprocessing.cpu_count() * workers_per_core
