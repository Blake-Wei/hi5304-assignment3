# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# Defensive: remove any problematic yarn repo files (if present)
RUN rm -rf /etc/apt/sources.list.d/*yarn* || true

# Avoid interactive prompts during apt installs
ENV DEBIAN_FRONTEND=noninteractive

# 1) OS packages:
# - postgresql-client: psql
# - r-base: R
# - build + headers needed for common R packages (tidyverse, etc.)
# - pandoc: nice-to-have for RMarkdown (optional but useful in teaching)
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

# 2) Preinstall R packages system-wide (so students don't install in class)
# Set CRAN repo explicitly.
RUN R -q -e 'options(repos = c(CRAN="https://cloud.r-project.org")); install.packages(c("tidyverse","janitor","skimr","readr","ggplot2"), Ncpus=max(1, parallel::detectCores()-1))'

# Optional (recommended if you plan to connect R to Postgres later)
# Uncomment if/when you teach DB connections in R:
# RUN R -q -e 'options(repos = c(CRAN="https://cloud.r-project.org")); install.packages(c("DBI","RPostgres"), Ncpus=max(1, parallel::detectCores()-1))'




