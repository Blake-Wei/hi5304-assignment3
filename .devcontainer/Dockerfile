FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# Install Postgres client + R + helpers
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      postgresql-client \
      r-base \
      gdebi-core \
      wget \
      ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install RStudio Server
RUN wget -q https://download2.rstudio.org/server/jammy/amd64/rstudio-server-2026.01.0-392-amd64.deb && \
    gdebi -n rstudio-server-2026.01.0-392-amd64.deb && \
    rm -f rstudio-server-2026.01.0-392-amd64.deb

