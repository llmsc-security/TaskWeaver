#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for license information.
#-------------------------------------------------------------------------------------------------------------

FROM mcr.microsoft.com/devcontainers/python:3.11

#
# Update the OS and maybe install packages
#
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
   && apt-get upgrade -y  \
   && apt-get -y install --no-install-recommends build-essential \
   && apt-get autoremove -y \
   && apt-get clean -y \
   && rm -rf /var/lib/apt/lists/*


```dockerfile
#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for license information.
#-------------------------------------------------------------------------------------------------------------

FROM mcr.microsoft.com/devcontainers/python:3.11

# Update the OS and install required packages in a single, clean layer
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential && \
    rm -rf /var/lib/apt/lists/*
```


```dockerfile
# syntax=docker/dockerfile:1
#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for license information.
#-------------------------------------------------------------------------------------------------------------

FROM mcr.microsoft.com/devcontainers/python:3.11

# Set non‑interactive mode for apt
ENV DEBIAN_FRONTEND=noninteractive

# Update the package index and install required build tools in a single, tidy layer.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential && \
    rm -rf /var/lib/apt/lists/*
```


# syntax=docker/dockerfile:1

# Base image with Python 3.11
FROM mcr.microsoft.com/devcontainers/python:3.11

# Prevent interactive prompts during apt operations
ENV DEBIAN_FRONTEND=noninteractive

# Update package index and install only the required build tools in a single layer.
# Clean up apt caches to keep the image size small.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential && \
    rm -rf /var/lib/apt/lists/*



```dockerfile
# syntax=docker/dockerfile:1
#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for license information.
#-------------------------------------------------------------------------------------------------------------

# Base image with Python 3.11
FROM mcr.microsoft.com/devcontainers/python:3.11

# Prevent interactive prompts during apt operations
ENV DEBIAN_FRONTEND=noninteractive

# Update package index and install only the required build tools in a single layer.
# Clean up apt caches to keep the image size small.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential && \
    rm -rf /var/lib/apt/lists/*

# (Add any additional steps you need below)
```
