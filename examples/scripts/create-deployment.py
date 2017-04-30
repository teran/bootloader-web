#!/usr/bin/env python

import os
import requests
import sys

try:
    API_TOKEN = os.environ['API_TOKEN']
    BOOTLOADER_URL = os.environ['BOOTLOADER_URL']
    SERVER_NAME = os.environ['SERVER_NAME']
    PROFILE = os.environ['PROFILE'].split('==')
except KeyError as e:
    print("""
    API_TOKEN and BOOTLOADER_URL must be passed as environment variables

    SERVER_NAME and PROFILE_ID are used as a payload for API

    Example:
    export API_TOKEN=<token>
    export BOOTLOADER_URL=<bootloaderurl>
    export SERVER_NAME=<hostname>
    export PROFILE=<name>==<version>
    %s
    """ % __file__)
    sys.exit(1)

headers = {
    'User-Agent': 'Bootloader Create Deployment example script/0.1',
    'Authorization': 'Token %s' % (API_TOKEN,),
}

r = requests.get(
    '%s/api/v1alpha1/profiles/?name=%s&version=%s' % (
        BOOTLOADER_URL, PROFILE[0], PROFILE[1],),
    headers=headers,
).json()[0]

r = requests.post(
    '%s/api/v1alpha1/deployments/' % (BOOTLOADER_URL,),
    headers=headers,
    data={
        'server': SERVER_NAME,
        'profile': r['id'],
    })

print(r.content)
