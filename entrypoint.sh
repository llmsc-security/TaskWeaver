#!/bin/bash

# TaskWeaver Chainlit entrypoint script
# Starts the Chainlit UI for TaskWeaver

echo "Starting TaskWeaver Chainlit UI..."

# Switch to the app directory
cd /app/playground/UI

# Start the Chainlit app
echo "Launching Chainlit on port 8000..."
python -m chainlit run --host 0.0.0.0 --port 8000 app.py
