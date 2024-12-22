#!/bin/bash

# Exit on error
set -e

echo "Starting deployment process..."

# Check prerequisites
echo "Checking for prerequisites..."
if ! command -v python3 &>/dev/null; then
    echo "Error: Python3 is not installed. Please install it and try again."
    exit 1
fi

if ! command -v ganache-cli &>/dev/null; then
    echo "Error: Ganache CLI is not installed. Please install it and try again."
    exit 1
fi

if ! command -v node &>/dev/null; then
    echo "Error: Node.js is not installed. Please install it and try again."
    exit 1
fi

# Start Ganache in the background
echo "Starting Ganache CLI..."
ganache-cli -g 0 -l 999999999999999 -d > ganache_output.log 2>&1 &
GANACHE_PID=$!

# Wait for Ganache to initialize
echo "Waiting for Ganache to initialize..."
sleep 5

# Deploy the contracts using client.py
echo "Deploying the contracts..."
python3 client.py

# Check if the deployment was successful
if [ $? -eq 0 ]; then
    echo "Deployment successful!"
else
    echo "Error during deployment. Check the logs for more details."
    kill $GANACHE_PID
    exit 1
fi

# Run the workstation client
echo "Starting the workstation client..."
python3 workstation_client.py

# Kill Ganache when the script exits
trap "echo 'Stopping Ganache...'; kill $GANACHE_PID" EXIT
