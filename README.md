Bootloader
==========

![Layers size](https://images.microbadger.com/badges/image/teran/bootloader-web.svg)
[![Docker Automated build](https://img.shields.io/docker/automated/teran/bootloader-web.svg)](https://hub.docker.com/r/teran/bootloader-web/)
![License](https://img.shields.io/github/license/teran/bootloader-web.svg)

Servers inventory & deployment solution

Currently deep-deep alpha state.

Application arhitecture
=======================

![](https://raw.githubusercontent.com/teran/bootloader-web/master/docs/static/images/architecture.png)

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

bootloader is licenced under GPLv2 licence.

However some parts of the software uses third-part code, here's the list of JS
libraries used in bootloader-web and their licenses:

 * [Bootstrap](http://getbootstrap.com) - Licensed under the MIT license
 * [html5shiv](https://github.com/aFarkas/html5shiv) - MIT/GPL2 Licensed
 * [jQuery](https://jquery.com) - http://jquery.org/license
 * [respond](https://github.com/scottjehl/Respond) - Licensed under the MIT license

TODO
====
- [X] Custom authentication for API handlers used in deployment(short-life tokens linked to installation)
- [ ] Client part to run some configuration gathering just after install
- [X] WebUI to add servers
- [ ] WebUI to edit servers
- [X] Create a way to get queue name from location UI
- [ ] Update deployments to be able to set parameters to profiles
- [ ] Add working Kubernetes specs
