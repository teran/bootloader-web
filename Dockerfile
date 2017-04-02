FROM alpine:latest

RUN apk --update --no-cache add \
      ca-certificates \
      freetype-dev \
      g++ \
      gcc \
      linux-headers \
      mailcap \
      pkgconfig \
      postgresql-dev \
      python \
      python-dev \
      py2-pip \
      openssl && \
    rm -vf /var/cache/apk/* && \
    update-ca-certificates

RUN pip install --no-cache-dir --upgrade pip uwsgi && \
    find / -name '*.pyc' -or -name '*.pyo' -delete

ADD uwsgi.yaml /etc/bootloader/uwsgi.yaml

ADD bootloader /srv/bootloader

RUN pip install --no-cache-dir --upgrade -r /srv/bootloader/requirements.txt && \
    find / -name '*.pyc' -or -name '*.pyo' -delete

WORKDIR "/srv/bootloader"

EXPOSE 8000

ENTRYPOINT ["uwsgi", "-y", "/etc/bootloader/uwsgi.yaml"]
