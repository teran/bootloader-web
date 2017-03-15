FROM python-base

RUN apk --update --no-cache add bash && \
    rm -vf /var/cache/apk/*

RUN pip install --no-cache-dir --upgrade \
      django \
      ipython && \
    find / -name '*.pyc' -or -name '*.pyo' -delete

ENTRYPOINT ["/usr/bin/ipython"]
