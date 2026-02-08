#!/bin/bash

# TaskWeaver Docker Build and Run Script
# Builds the Docker image and runs it with port mapping 11280:8000

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Configuration
DOCKER_IMAGE_NAME="taskweaver:latest"
CONTAINER_NAME="taskweaver-app"
HOST_PORT=11280
CONTAINER_PORT=8000
UID=${TASKWEAVER_UID:-1000}
GID=${TASKWEAVER_GID:-1000}

echo "=========================================="
echo "TaskWeaver Docker Build and Run Script"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Build the Docker image
echo "Step 1: Building Docker image..."
echo "Image name: $DOCKER_IMAGE_NAME"
echo ""

docker build \
    --build-arg UID=$UID \
    --build-arg GID=$GID \
    -t "$DOCKER_IMAGE_NAME" \
    -f Dockerfile \
    .

echo ""
echo "Step 2: Stopping and removing old container (if exists)..."
docker stop "$CONTAINER_NAME" 2>/dev/null || true
docker rm "$CONTAINER_NAME" 2>/dev/null || true

echo ""
echo "Step 3: Starting new container..."
echo "Host port mapping: $HOST_PORT:$CONTAINER_PORT"
echo "Container name: $CONTAINER_NAME"
echo ""

# Run the container with port mapping
docker run \
    --name "$CONTAINER_NAME" \
    -p "$HOST_PORT:$CONTAINER_PORT" \
    -e TASKWEAVER_UID=$UID \
    -e TASKWEAVER_GID=$GID \
    --rm \
    -v "$(pwd)/project:/app/project:ro" \
    -v "$(pwd)/playground:/app/playground:ro" \
    "$DOCKER_IMAGE_NAME"

echo ""
echo "=========================================="
echo "TaskWeaver container stopped."
echo "Access the UI at: http://localhost:$HOST_PORT"
echo "=========================================="
