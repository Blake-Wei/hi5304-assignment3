# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

# Remove any Yarn apt repo entries (prevents EXPKEYSIG issues if present)
RUN set -eux; \
    for f in $(grep -RIl "dl.yarnpkg.com" /etc/apt/sources.list /etc/apt/sources.list.d 2>/dev/null || true); do \
      echo "Removing Yarn apt source: $f"; \
      rm -f "$f"; \
    done; \
    rm -f /etc/apt/trusted.gpg.d/yarn.gpg /usr/share/keyrings/yarn.gpg /usr/share/keyrings/yarnkey.gpg 2>/dev/null || true

# Base tools + Postgres client + R
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      postgresql-client \
      r-base \
      gdebi-core \
      wget \
      ca-certificates \
      gnupg \
      curl; \
    rm -rf /var/lib/apt/lists/*

# ---- RStudio Server ----
# Use an explicit URL but make failures visible (no -q), and follow redirects.
# If this URL changes later, the error message will clearly show why.
ARG RSTUDIO_DEB_URL="https://download2.rstudio.org/server/jammy/amd64/rstudio-server-2026.01.0-392-amd64.deb"

RUN set -eux; \
    echo "Downloading RStudio Server from: ${RSTUDIO_DEB_URL}"; \
    wget --server-response --progress=dot:giga -O /tmp/rstudio-server.deb "${RSTUDIO_DEB_URL}"; \
    dpkg -I /tmp/rstudio-server.deb | head -n 50; \
    gdebi -n /tmp/rstudio-server.deb; \
    rm -f /tmp/rstudio-server.deb



