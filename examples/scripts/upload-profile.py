#!/usr/bin/env python

import json
import os
import requests
import sys
import yaml

try:
    API_TOKEN = os.environ['API_TOKEN']
    BOOTLOADER_URL = os.environ['BOOTLOADER_URL']
except KeyError as e:
    print("""
    API_TOKEN and BOOTLOADER_URL must be passed as environment variables

    Example:
    export API_TOKEN=<token>
    export BOOTLOADER_URL=<bootloaderurl>
    %s profile.yaml
    """ % __file__)
    sys.exit(1)


headers = {
    'User-Agent': 'Bootloader Upload profile example script/0.1',
    'Authorization': 'Token %s' % (API_TOKEN,),
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

with open(sys.argv[1], 'r') as fp:
    profile = yaml.load(fp)
    payload = json.dumps({'profile': json.dumps(profile)})
    r = requests.post(
        '%s/api/v1alpha2/profiles/' % (BOOTLOADER_URL,),
        data=payload,
        headers=headers)

if r.status_code == 201:
    print('Profile %s uploaded successfully: status code %s returned' % (
        sys.argv[1], r.status_code,))
else:
    print("Error uploading profile:\nstatus code: %s\n%s" % (
        r.status_code, r.content,))
