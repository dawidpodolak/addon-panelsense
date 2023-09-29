ARG BUILD_FROM
FROM $BUILD_FROM

WORKDIR /usr/src/app

# Add Bashio
ARG BASHIO_VERSION="0.13.1"
RUN curl -L -s -o /usr/lib/bashio.tar.gz \
    "https://github.com/hassio-addons/bashio/archive/v${BASHIO_VERSION}.tar.gz" \
    && tar xzf /usr/lib/bashio.tar.gz -C /usr/lib \
    && rm /usr/lib/bashio.tar.gz

LABEL \
  io.hass.version="VERSION" \
  io.hass.type="addon" \
  io.hass.arch="armhf|aarch64|i386|amd64"

COPY senseapp /usr/src/app/senseapp
COPY requirements.txt /tmp/requirements.txt
COPY config.yaml /

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

RUN pip install --no-cache-dir -r /tmp/requirements.txt

CMD ["/run.sh"]
