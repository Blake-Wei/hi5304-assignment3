# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# Clean any problematic repos (defensive)
RUN rm -rf /etc/apt/sources.list.d/*yarn* || true

# Install PostgreSQL client and R
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      postgresql-client \
      r-base \
      ca-certificates && \
    rm -rf /var/lib/apt/lists/*




