# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# --- Critical fix for Codespaces builds ---
# The base/devcontainer features layer may add Yarn's APT repo, whose signing key can expire.
# This removes the Yarn repo/key so `apt-get update` doesn't fail with EXPKEYSIG.
RUN rm -f /etc/apt/sources.list.d/yarn.list || true \
 && rm -f /etc/apt/trusted.gpg.d/yarn.gpg || true \
 && rm -f /usr/share/keyrings/yarnkey.gpg || true

# --- Install Postgres client + R + helpers ---
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      postgresql-client \
      r-base \
      gdebi-core \
      wget \
      ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# --- Install RStudio Server ---
# If this URL/version ever changes upstream, the build will fail here.
RUN wget -q -O /tmp/rstudio-server.deb \
      https://download2.rstudio.org/server/jammy/amd64/rstudio-server-2026.01.0-392-amd64.deb && \
    gdebi -n /tmp/rstudio-server.deb && \
    rm -f /tmp/rstudio-server.deb


