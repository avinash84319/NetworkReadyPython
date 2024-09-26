# run this file to start the servers in background for development

# First server
(poetry run flask --app servernode.py run --port 3000 > /dev/null 2>&1) &

# Second server
(poetry run flask --app servernode.py run --port 5000 > /dev/null 2>&1) &


