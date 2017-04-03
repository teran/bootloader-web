Bootloader
==========

[![Docker Automated build](https://img.shields.io/docker/automated/teran/bootloader-web.svg)](https://hub.docker.com/r/teran/bootloader-web/)
[![License](https://img.shields.io/github/license/teran/bootloader-web.svg)]()

Servers inventory & deployment solution

Currently deep-deep alpha state.

Configuration
=============

Currently there's the way to configure the agent via environment variables:

 * `BOOTLOADER_URL` - URL of bootloader-web instance, default is `'http://bootloader:8000/'`
 * `BROKER_URL` - URL of broker for celery, default is `'amqp://guest:guest@rabbitmq:5672//'`
 * `DB_HOST` - Hostname of PostgreSQL database to use for the app, default is `'postgresql'`
 * `DB_NAME` - Database name, default is `'postgres'`
 * `DB_PASSWORD` - Password to access the database, default is `None`
 * `DB_USER` - Username to access the database, default is `'postgres'`

Licence
=======

The code is licenced under GPLv2 licence.

TODO
====
- [X] Custom authentication for API handlers used in deployment(short-life tokens linked to installation)
- [ ] Client part to run some configuration gathering just after install
- [ ] WebUI to add servers
- [ ] WebUI to edit servers
