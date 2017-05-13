# Profiles
## API Version

All the content is applied to Profile API `v1alpha1`.
In future versions API could be changed.

## Introduction

Bootloader uses profiles to get proper understanding on actions needed to
perform. Theoretically it's mission-agnostic and could perform any actions
including but not limited to:

* Hardware RAID setup via MegaCLI or any other similar tool
* Flash BIOS and/or BMC
* Configure network ports

## Steps and Actions

Deployment is splited into steps named by status they're designed to bring to:

* new
* preparing
* installation
* configuring
* postconfiguring
* error
* complete

Last two of them are the final states, where you cant switch out.
This is implemented using FSM mechanism and ideologically there should not be
any way to switch to any other states.

In each step there could be a set of actions to perform particular activity.
API `v1alpha1` supports the following actions:

* delete_file -- not implemented yet, pending to 0.0.1-alpha2
* expect_callback
* ipmi_command
* serve_file

All of them are executed on Agent instance for particular location and designed
to control deployment object.

serve_file and delete_file are served to provide some additional resources, i.e.
provide PXE-booted node with kernel and initrd, pxelinux confgiuration, etc.

### delete_file

Not implemented as of 0.0.1-alpha1

### expect_callback

Served for bootloader and object node synchronization.

Example:

```
postconfiguring:
  - action: expect_callback
    name: postconfiguring_callback
```

On deployment object it's expected to call something like:

```
wget -O /dev/null '{{ callback_base }}postconfiguring_callback'
```

In fact it would register callback name on local agent node and wait unitil
callback is called.

#### expect_callback signature

`name`(string) - callback name


### ipmi_command

Runs specified command on deployment objects BMC.
Data like IPMI hostname or IP address are taken from object's `ipmi_host` field,
credentials - from related credentials objects named `ipmi_username` and
`ipmi_password` accordingly.

Example:

```
- action: ipmi_command
  command: bootdev
  parameters: pxe
```

It executes IPMI command to BMC device one time and fails the deployment on
command failure.

#### ipmi_command signature

`command`(string) - command to execute. Possbile values are(supported by
  pyghmi):

* power
* bootdev
* sensors
* health
* inventory
* leds
* graphical
* net
* raw

`parameters`(string) - parameters to the command, specific for each particular
command. Some possible values are:

bootdev command:

* net
* network
* pxe
* hd
* safe
* cd
* cdrom
* optical
* dvd
* floppy
* default
* setup
* bios
* f1

power command:

* off
* on
* reset
* diag
* softoff
* shutdown

*NOTE:* IPMI behaviour could differ by vendors, provided examples(in
  `examples/` dir) are tested against Supermicro devices, it could not work for
other vendors at all or work different way.

*NOTE:* For IPMI functions implementation there's
[pyghmy](https://github.com/openstack/pyghmi) in use.

### serve_file

Downloads and serves by Agent the file, file could be provided URL or template.

Example:

```
- action: serve_file
  via: http
  filename: 'images/ubuntu/16.04/initrd.gz'
  source:
    type: url
    url: 'http://archive.ubuntu.com/ubuntu/dists/xenial-updates/main/installer-amd64/current/images/netboot/ubuntu-installer/amd64/initrd.gz'
```

#### serve_file signature

`via`(string) - method to serve file by, possbile values:

* http
* tftp

Please note, serving file by these methods requires enabled HTTP or TFTP server
on agent side.

`filename`(string) - relative target filename to store file at.
Templates are allowed to use with this field.

`source`(dict) - dict specific file source.

`source.type`(string) - File download method, could be `url` or `template`

`source.url`(string) - URL for file to download. Required by `type: url`

`source.name`(string) - Template name(from the same profile) to render served
file. Required by `type: template`

## Templates

Bootloader Profiles provide a pretty generic way to create configuration files,
preseeds any any other templated content required for deployment.

Templates are specified using `template` Profile section with template name as
a key. Example:

```
templates:
  pxelinux.cfg:
    type: template
    contents: |
      DEFAULT ubuntu1604
      LABEL ubuntu1604
        MENU LABEL ^Ubuntu 16.04
        MENU default
        KERNEL {{ agent_url }}/images/ubuntu/16.04/kernel
        INITRD {{ agent_url }}/images/ubuntu/16.04/initrd.gz
        APPEND auto=true priority=critical keymap=us debian-installer/keymap=us netcfg/choose_interface=auto preseed/url={{ agent_url }}/preseeds/{{ fqdn }}.cfg hostname={{ hostname }} domain={{ domain }} netcfg/disable_dhcp=true netcfg/get_ipaddress={{ ipaddress }} netcfg/get_netmask={{ netmask }} netcfg/get_gateway={{ gateway }} netcfg/get_nameservers={{ nameserver }}
```

### Template Signature

`template`(dict) - Top level-dict contains templates

`templates.$key`(string) - Template name

`templates.$key.type`(string) - Template type, `template` value only is
supported at the moment.

`templates.$key.contents`(string) - Template content

### Template context

To use complete configuration files Bootloader Profile API provides a context
with some predefined variables present in all the enteties `DeploymentContext`
used:

`agent_url`(string) - Agent URL, to be used to interact with Agent instance

`callback_base`(string) - Callback URL base

`domain`(string) - Deployment object FQDN's domain part of FQDN

`export_base`(string) - Web app URL base to export data, should not be used in confiuration files, because deployment objects should not interact with API or Web app directly.

`fqdn`(string) - Deployment object's FQDN

`gateway`(string) - Network gateway provided from Network data

`hostname`(string) - Deployment object's hostname part of FQDN

`ipaddress`(string) - Deployment object IP address, gathered by resolving FQDN in DNS

`ipmi_host`(string) - IPMI host field from Deployment object model

`nameserver`(string) - nameserver for the network Deployment object relates to

`netmask`(string) - network mask in IP notation for Deployment object network

`profile`(string) - Profile name deployment runs

*Note:* In some cases this list could be extended by particular feature.
