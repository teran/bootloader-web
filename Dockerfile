FROM alpine:latest

RUN apk --update --no-cache add \
      ca-certificates \
      libpq \
      mailcap \
      python \
      py2-pip \
      openssl && \
    rm -vf /var/cache/apk/* && \
    update-ca-certificates

RUN pip install --no-cache-dir --upgrade pip && \
    find / -name '*.pyc' -or -name '*.pyo' -delete

ADD uwsgi.yaml /etc/bootloader/uwsgi.yaml

ADD bootloader /srv/bootloader

RUN apk add --update --no-cache \
      freetype-dev \
      g++ \
      gcc \
      linux-headers \
      pkgconfig \
      postgresql-dev \
      python-dev && \
    pip install --no-cache-dir --upgrade -r /srv/bootloader/requirements.txt && \
    pip install --no-cache-dir --upgrade uwsgi && \
    find / -name '*.pyc' -or -name '*.pyo' -delete && \
    apk del --update --purge --no-cache \
      freetype-dev \
      g++ \
      gcc \
      linux-headers \
      pkgconfig \
      postgresql-dev \
      python-dev

WORKDIR "/srv/bootloader"

EXPOSE 8000

ENTRYPOINT ["uwsgi", "-y", "/etc/bootloader/uwsgi.yaml"]
