ARG BUILD_FROM
FROM $BUILD_FROM
# FROM ghcr.io/home-assistant/amd64-base:3.15
WORKDIR /usr/src/app

# Copy in the root filesystem for s6-overlay
COPY rootfs /
RUN chmod a+x /etc/services.d/PanelSense/run
RUN chmod a+x /etc/services.d/PanelSense/finish
RUN chmod a+x /etc/nginx/http.d/ingress.conf
RUN chmod a+x /etc/cont-init.d/nginx.sh

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

# for debug only
RUN apk add git nano curl zsh
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Install python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# CMD [ "nginx","-g","daemon off;error_log /dev/stdout debug;" ]