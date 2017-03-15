FROM python-base

RUN apk --update --no-cache add \
      nginx \
      uwsgi \
      uwsgi-python && \
    rm -vf /var/cache/apk/*
