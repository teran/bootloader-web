FROM alpine:latest

RUN apk --update --no-cache add \
      ca-certificates \
      freetype-dev \
      g++ \
      gcc \
      linux-headers \
      pkgconfig \
      python \
      python-dev \
      py2-pip \
      openssl && \
    rm -vf /var/cache/apk/* && \
    update-ca-certificates

RUN pip install --no-cache-dir --upgrade pip && \
    find / -name '*.pyc' -or -name '*.pyo' -delete

COPY bootloader-agent.py /srv/
COPY requirements.txt /srv/

RUN pip install --no-cache-dir --upgrade -r /srv/requirements.txt && \
    find / -name '*.pyc' -or -name '*.pyo' -delete
