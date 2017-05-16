# Bootloader

[![Build Status](https://travis-ci.org/teran/bootloader-web.svg?branch=master)](https://travis-ci.org/teran/bootloader-web)
[![Layers size](https://images.microbadger.com/badges/image/teran/bootloader-web.svg)](https://hub.docker.com/r/teran/bootloader-web/)
![Recent build commit](https://images.microbadger.com/badges/commit/teran/bootloader-web.svg)
[![Docker Automated build](https://img.shields.io/docker/automated/teran/bootloader-web.svg)](https://hub.docker.com/r/teran/bootloader-web/)
![License](https://img.shields.io/github/license/teran/bootloader-web.svg)

Servers inventory & deployment solution

Currently deep-deep alpha state.

# Application arhitecture

![](https://raw.githubusercontent.com/teran/bootloader-web/master/docs/static/images/architecture.png)

# Configuration

Currently there's the way to configure the agent via environment variables:

 * `BOOTLOADER_URL` - URL of bootloader-web instance, default is `'http://bootloader:8000/'`
 * `BROKER_URL` - URL of broker for celery, default is `'amqp://guest:guest@rabbitmq:5672//'`
 * `DB_HOST` - Hostname of PostgreSQL database to use for the app, default is `'postgresql'`
 * `DB_NAME` - Database name, default is `'postgres'`
 * `DB_PASSWORD` - Password to access the database, default is `None`
 * `DB_USER` - Username to access the database, default is `'postgres'`
 * `DEFAULT_THEME` - Theme name to use
 * `GRAVATAR_PROXY` - `<true|false>` - Enable or disable proxying gravatar requests
 * `SSL_CERTIFICATE_CONTENTS` - contents of SSL certificates to use for HTTPS
 * `SSL_ENABLE` - `<true|false>` Enable SSL support
 * `SSL_KEY_CONTENTS` - contents of SSL private key to use for HTTPS
 * `SSL_SET_REDIRECT` - `<true|false>` enables redirect from HTTP to HTTPS

# Installation

All the releases and development versions are represented as docker images
## The most stable release

```
docker pull teran/bootloader-web:0.0.1-alpha1
docker pull teran/bootloader-agent:0.0.1-alpha1
```

### The most recent build (dangerous, could be totally unstable)

```
docker pull teran/bootloader-web:latest
docker pull teran/bootloader-agent:latest
```

# Compatibility and guarantees

### Application status

Current project state: Alpha

Pending release number: 0.0.1-alpha2

All releases will be reflected as a git tag.

### Build status

Build for bootloader components would mean corresponding docker images.
The most recent build is always tagged with `latest` no matter what version is it,
so it's just time-related tag.
Each branch have it's own tag, for `master` git-branch it's `master` tag in docker hub.
Eeach release gonna be tagged accordingly.

The most proper way for development purposes is to use `:master` docker tag.
For testing and/or production - tag describes particular version.

Update procedure between versions is not designed at the moment.
But based on how application is developed it should work in proper way without any
issues.

### API status
The most stable current API version: `v1alpha1`
Any incompatible changes will be marked as dedicated API version.

#### API Alpha versions

Their main purpose is to be a trade off between stability and development speed.
All of incompatible changes will be reflected in new version.
Supported during current version lifecycle only.

#### API Beta versions

Served for stabilization, i.e. fixes only are accepted.
Supported during current application version lifecycle only.

#### API Stable versions

A kind of LTS for API.
Supported during two stable releases.

#### API versions lifecycle

Normally it should work the following way:
v1alpha1 - the first initial version shows what could we need from API.
It will become v1alpha2 as only it would have incompatible changes.

In addition the most recent version of Alpha API will be forked to v1beta1 on first
alpha-release, and the most recent beta-version to stable on stable application release.

Legacy API versions could stay for some time for some reasons, but they are not going to be
supported or verified for compatibility.

### Dependencies status
Python versions:
 * 2.7,
 * 3.6 (optional)

Django versions:
 * 1.6 (optional)
 * 1.7 (optional)
 * 1.8 (optional)
 * 1.9 (optional)
 * 1.10 (optional)
 * 1.11

Celery versions:
 * 4.0

PostgreSQL versions:
 * 9.6

RabbitMQ versions:
 * 3.6

This version list means bootloader-web tests against them but here are some "but":
 * optional versions could be skipped if they're support would require too much
   work

# Licences

bootloader is licenced under GPLv2 licence.

However some parts of the software uses third-part code, here's the list of JS
libraries used in bootloader-web and their licenses:

 * [Bootstrap](http://getbootstrap.com) - Licensed under the MIT license
 * [html5shiv](https://github.com/aFarkas/html5shiv) - MIT/GPL2 Licensed
 * [jQuery](https://jquery.com) - http://jquery.org/license
 * [respond](https://github.com/scottjehl/Respond) - Licensed under the MIT license
 * [BOOTSTRA.386](https://github.com/kristopolous/BOOTSTRA.386) - Licensed under Apache-2.0 licence
 * [Slate theme](https://github.com/thomaspark/bootswatch) - Lincenced under MIT licence
 * [Yeti theme](https://github.com/thomaspark/bootswatch) - Lincenced under MIT licence

# Pending releases
## Alpha2 release features and requirements

- [ ] Make deployment timeouts configurable from profiles
- [ ] Errors are come to UI
- [ ] Queue tests
- [ ] Input validation with UI error displaying
- [ ] Handle JS errors without alert()
- [ ] Update any object through WebUI
- [ ] Full REST API namespacing with properly namespaced tests

## Alpha3

- [ ] Slack and email notifications about deployments
- [ ] Profiles API namespacing

## Beta1 release features and requirements

- [ ] All key parts are covered with tests
- [ ] All the pipeline is manually tested
