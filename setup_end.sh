#run this file to stop the servers started in background by setup.sh

#!/bin/bash

# Find the process IDs (PIDs) of Flask servers running on port 3000 and 5000
pid_3000=$(lsof -ti :3000)
pid_5000=$(lsof -ti :5000)

# Check if a process is running on port 3000 and kill it
if [ -n "$pid_3000" ]; then
    echo "Stopping Flask server on port 3000 (PID: $pid_3000)"
    kill -9 "$pid_3000"
else
    echo "No Flask server found on port 3000"
fi

# Check if a process is running on port 5000 and kill it
if [ -n "$pid_5000" ]; then
    echo "Stopping Flask server on port 5000 (PID: $pid_5000)"
    kill -9 "$pid_5000"
else
    echo "No Flask server found on port 5000"
fi
