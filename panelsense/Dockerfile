ARG BUILD_FROM
FROM $BUILD_FROM
# FROM ghcr.io/home-assistant/amd64-base:3.15
WORKDIR /usr/src/app

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Copy in the root filesystem for s6-overlay
COPY rootfs /
RUN chmod a+x /etc

# Install dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip

RUN apk add nginx

COPY senseapp /usr/src/app/senseapp
COPY requirements.txt /tmp/requirements.txt
COPY config.yaml /

ENV SENSE_APP=/usr/src/app/senseapp/sense.py
ENV HASS_WS_ADDRESS="ws://supervisor/core/websocket"
ENV PANEL_SENSE_DATABASE="/config/panelsense/sense_database.db"
ENV STORAGE_DATABASE="/config/panelsense/storage_database.db"
# for debug only
RUN apk add git nano curl zsh vim
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Install python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

LABEL \
  io.hass.version="VERSION" \
  io.hass.type="addon" \
  io.hass.arch="armhf|aarch64|i386|amd64"