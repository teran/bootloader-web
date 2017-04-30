#!/usr/bin/env python

import os
import requests
import sys

try:
    API_TOKEN = os.environ['API_TOKEN']
    BOOTLOADER_URL = os.environ['BOOTLOADER_URL']
except KeyError as e:
    print("""
    API_TOKEN and BOOTLOADER_URL must be passed as environment variables

    Example:
    export API_TOKEN=<token>
    export BOOTLOADER_URL=<bootloaderurl>
    %s
    """ % __file__)
    sys.exit(1)


headers = {
    'User-Agent': 'Bootloader Delete Deployment example script/0.1',
    'Authorization': 'Token %s' % (API_TOKEN,),
}

r = requests.get(
    '%s/api/v1alpha1/deployments/' % BOOTLOADER_URL,
    headers=headers).json()

for deployment in r:
    requests.delete(
        '%s/api/v1alpha1/deployments/%s/' % (
            BOOTLOADER_URL, deployment['id'],),
        headers=headers)
