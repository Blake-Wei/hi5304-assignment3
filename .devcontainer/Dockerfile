# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Defensive: remove any problematic yarn repo files (if present)
RUN rm -rf /etc/apt/sources.list.d/*yarn* || true

# ---- System dependencies (Debian) ----
# - postgresql-client -> psql
# - r-base -> R
# - build libs -> compile common R packages (tidyverse, etc.)
# - pandoc -> helpful for RMarkdown/Quarto style workflows
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

# ---- Python packages (system-wide) ----
# Ensures VS Code + Jupyter use the same Jupyter install (not user-level)
COPY .devcontainer/requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r /tmp/requirements.txt && \
    python -m pip install --no-cache-dir jupyter ipykernel

# ---- R packages (system-wide) ----
# Preinstall course packages + IRkernel so students don't install anything in class
RUN R -q -e 'options(repos=c(CRAN="https://cloud.r-project.org")); \
            install.packages(c("tidyverse","janitor","skimr","IRkernel"), \
                             Ncpus=max(1, parallel::detectCores()-1))'

# Register the R kernel spec system-wide so it appears in VS Code/Jupyter
RUN R -q -e 'IRkernel::installspec(user=FALSE, name="ir42", displayname="R (4.2.2)")'

# Optional: show kernels at build time in logs (nice sanity check)
RUN jupyter kernelspec list





