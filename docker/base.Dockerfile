FROM alpine:latest

RUN apk --update --no-cache add \
      ca-certificates \
      freetype-dev \
      g++ \
      gcc \
      pkgconfig \
      python \
      python-dev \
      py2-pip \
      openssl && \
    rm -vf /var/cache/apk/* && \
    update-ca-certificates

RUN pip install --no-cache-dir --upgrade pip && \
    find / -name '*.pyc' -or -name '*.pyo' -delete

RUN pip install --no-cache-dir --upgrade Django && \
    find / -name '*.pyc' -or -name '*.pyo' -delete

RUN pip install --no-cache-dir --upgrade djangorestframework && \
    find / -name '*.pyc' -or -name '*.pyo' -delete

ENTRYPOINT ["/srv/bootloader/manage.py", "runserver", "0.0.0.0:8000"]
