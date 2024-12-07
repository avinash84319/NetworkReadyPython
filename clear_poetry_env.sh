#!/bin/bash

# Check if the script received a Poetry file as an argument
if [ $# -ne 1 ]; then
  echo "Usage: $0 /path/to/pyproject.toml"
  exit 1
fi

# Get the directory of the provided pyproject.toml
PROJECT_DIR=$(dirname "$1")

# Change to the project directory
cd "$PROJECT_DIR" || { echo "Error: Unable to change to project directory."; exit 1; }

# Remove the virtual environment
echo "Removing Poetry virtual environment for project..."
poetry env remove python || { echo "Error: Failed to remove virtual environment."; exit 1; }

echo "Virtual environment successfully cleared for project: $PROJECT_DIR"