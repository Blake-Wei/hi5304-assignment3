# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Defensive: remove any problematic yarn repo files (if present)
RUN rm -rf /etc/apt/sources.list.d/*yarn* || true

# System deps for Postgres client + R + compiling common R packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      postgresql-client \
      r-base \
      ca-certificates \
      build-essential \
      gfortran \
      libcurl4-openssl-dev \
      libssl-dev \
      libxml2-dev \
      pandoc \
    && rm -rf /var/lib/apt/lists/*

# Python deps (so VS Code/Jupyter uses container Python)
COPY .devcontainer/requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r /tmp/requirements.txt

# Install R packages system-wide (no student installs)
RUN R -q -e 'options(repos=c(CRAN="https://cloud.r-project.org")); \
            install.packages(c("tidyverse","janitor","skimr","IRkernel"), \
                             Ncpus=max(1, parallel::detectCores()-1))'

# Register R kernel system-wide so it always appears
RUN R -q -e 'IRkernel::installspec(user=FALSE, name="ir42", displayname="R (4.2.2)")'






