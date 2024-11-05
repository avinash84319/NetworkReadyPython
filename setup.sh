# run this file to start the servers in background for development

# First server
(poetry run flask --app servernode.py --debug run --port 3000) &

# Second server
(poetry run flask --app servernode.py --debug run --port 5000) &

# Third server
(poetry run flask --app servernode.py --debug run --port 4000) &


