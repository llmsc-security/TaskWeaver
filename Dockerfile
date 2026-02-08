# Multi-stage build for TaskWeaver
# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim AS runtime

# Create non-root user
ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} taskweaver && \
    useradd -u ${UID} -g ${GID} -m -s /bin/bash taskweaver

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        curl \
        && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project files
COPY taskweaver /app/taskweaver
COPY project /app/project
COPY playground /app/playground
COPY requirements.txt .

# Copy Chainlit config
COPY playground/UI/.chainlit /app/playground/UI/.chainlit

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV EXECUTION_SERVICE_KERNEL_MODE="container"
ENV TASKWEAVER_UID=${UID}
ENV TASKWEAVER_GID=${GID}

# Expose port for Chainlit UI
EXPOSE 8000

# Change ownership and switch to non-root user
RUN chown -R taskweaver:taskweaver /app

USER taskweaver

# Set working directory
WORKDIR /app/playground/UI

# Entrypoint
ENTRYPOINT ["sh", "/app/playground/UI/entrypoint.sh"]
