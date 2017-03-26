#!/usr/bin/env python

import copy
import json
import re
import requests
import socket

import netifaces

hostname = socket.gethostname()
authToken = "76f2ca243a219f0bcb51810d5809609e8f5771cd"
bootloaderUrl = "http://bootloader:8000/api/"
location = "Moscow"

headers = {
    'User-Agent': 'Bootloader-Agent/0.1',
    'Authorization': 'Token '+authToken,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

interfaceRegex = re.compile(r'eth([0-9]{,2})')

# os.path.join(bootloaderUrl, 'servers/'),
serversUrl = 'http://bootloader:8000/api/servers/'
interfacesURL = 'http://bootloader:8000/api/interfaces/'

r = requests.get(
    serversUrl,
    params={'fqdn': hostname},
    headers=headers)

if len(r.json()) > 0:
    print "Server is already registered, checking interfaces"
else:
    print "Server is not registered. Registering"
    r = requests.post(
        serversUrl,
        data=json.dumps({'fqdn': hostname, 'location': location}),
        headers=headers)

    print r.json()

r = requests.get(
    interfacesURL,
    params={'server': hostname},
    headers=headers)

api_interfaces = r.json()
interfaces = []
for interface in netifaces.interfaces():
    if interfaceRegex.match(interface):
        hwaddr = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
        interfaces.append({
            'name': interface, 'mac': hwaddr, 'server': hostname})

if len(api_interfaces) > 0:
    print "More than 1 interface, not bad."
    api_interfaces = sorted(api_interfaces, key=lambda k: k['name'])
    interfaces = sorted(interfaces, key=lambda k: k['name'])
    check_interfaces = copy.deepcopy(api_interfaces)

    for interface in check_interfaces:
        del(interface['pk'])
    if check_interfaces == interfaces:
        print 'Interfaces: No changes requred'
    else:
        for interface in api_interfaces:
            requests.delete(
                interfacesURL+str(interface['pk'])+'/', headers=headers)
        for interface in interfaces:
                r = requests.post(
                    interfacesURL,
                    data=json.dumps(interface),
                    headers=headers)
                print r.json()
else:
    print "0 Interfaces. Registering"
    for interface in interfaces:
            r = requests.post(
                interfacesURL,
                data=json.dumps(interface),
                headers=headers)
            print r.json()
