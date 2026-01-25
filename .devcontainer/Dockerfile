# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Defensive: remove any problematic yarn repo files (if present)
RUN rm -rf /etc/apt/sources.list.d/*yarn* || true

# System deps:
# - psql client
# - R
# - build + common libs required to compile tidyverse dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      postgresql-client \
      r-base \
      r-base-dev \
      ca-certificates \
      build-essential \
      gfortran \
      libcurl4-openssl-dev \
      libssl-dev \
      libxml2-dev \
      libfontconfig1-dev \
      libfreetype6-dev \
      libharfbuzz-dev \
      libfribidi-dev \
      libpng-dev \
      libtiff5-dev \
      libjpeg-dev \
      pandoc \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY .devcontainer/requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r /tmp/requirements.txt

# R packages (system-wide) + IRkernel
RUN R -q -e 'options(repos=c(CRAN="https://cloud.r-project.org")); \
            install.packages(c("tidyverse","janitor","skimr","IRkernel"), \
                             Ncpus=max(1, parallel::detectCores()-1))'

# Register R kernel system-wide so VS Code always sees it
RUN R -q -e 'IRkernel::installspec(user=FALSE, name="ir42", displayname="R (4.2.2)")'







