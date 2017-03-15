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
    update-ca-certificates && \
    pip install --no-cache-dir --upgrade pip && \
    find / -name '*.pyc' -or -name '*.pyo' -delete

ENTRYPOINT ["/bin/sh"]
