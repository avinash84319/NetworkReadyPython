#run this file to stop the servers started in background by setup.sh

#!/bin/bash

#!/bin/bash

# Function to stop processes on a given port
stop_process_on_port() {
    local port=$1
    # Get all PIDs on the specified port
    pids=$(lsof -ti :$port)

    if [ -n "$pids" ]; then
        echo "Stopping processes on port $port (PIDs: $pids)"
        # Loop through each PID and kill them
        for pid in $pids; do
            sudo kill -9 "$pid"
            echo "Killed PID $pid on port $port"
        done
    else
        echo "No process found on port $port"
    fi
}

# Stop processes on port 3000 and 5000
stop_process_on_port 3000
stop_process_on_port 5000

