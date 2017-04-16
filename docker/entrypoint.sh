#!/bin/sh

set -e

if [[ -n "${SSL_CERTIFICATE_CONTENTS}" ]] ; then
  echo "${SSL_CERTIFICATE_CONTENTS}" > /etc/bootloader/certificate.pem
  chown root:root /etc/bootloader/certificate.pem
  chmod 0400 /etc/bootloader/certificate.pem
fi

if [[ -n "${SSL_KEY_CONTENTS}" ]] ; then
  echo "${SSL_KEY_CONTENTS}" > /etc/bootloader/key.pem
  chown root:root /etc/bootloader/key.pem
  chmod 0400 /etc/bootloader/key.pem
fi

if [[ "${SSL_ENABLE}" == "true" ]] ; then
  cp /etc/bootloader/nginx-ssl.conf /etc/nginx/conf.d/nginx-ssl.conf
  if [[ "${SSL_SET_REDIRECT}" == "true" ]] ; then
    cp /etc/bootloader/nginx-http-redirect.conf /etc/nginx/conf.d/nginx-redirect.conf
  fi
else
  cp /etc/bootloader/nginx-http.conf /etc/nginx/conf.d/nginx-http.conf
fi

touch /var/log/uwsgi.log
chown nobody:nogroup /var/log/uwsgi.log
chmod 0600 /var/log/uwsgi.log

uwsgi \
  -y /etc/bootloader/uwsgi.yaml \
  --daemonize2 /var/log/uwsgi.log

mkdir -p /run/nginx
nginx -t && nginx

touch /var/log/celery.log
chown bootloader:nobody /var/log/celery.log
chmod 0600 /var/log/celery.log
mkdir -p /run/celery
chown bootloader:nobody /run/celery

/usr/bin/celery worker \
  -A deployments.tasks \
  --queues bootloader_tasks \
  --logfile /var/log/celery.log \
  --pidfile=/run/celery/celery.pid \
  --uid 100 \
  --gid 65533 \
  --detach

tail -f /var/log/uwsgi.log /var/log/nginx/* /var/log/celery.log
