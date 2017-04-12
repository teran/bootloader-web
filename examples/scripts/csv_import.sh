#!/bin/bash

CSV_FILE="${1}"
LOCATION="${2}"
BOOTLOADER_URL="${3}"
API_TOKEN="${4}"

# csv format: <hostname>;<ipmi_host>;whatever;whatever;whatever;whatever;<mac_address>
awk -F ';' 'NR>1 {print $1,$2,$7}' "${CSV_FILE}" | while read f ; do
  HOSTNAME=$(echo $f | awk '{print $1}')
  IPMI_HOSTNAME=$(echo $f | awk '{print $2}')
  MAC=$(echo $f | awk '{print $3}')

  SERVER_PAYLOAD="{\"fqdn\":\"${HOSTNAME}\",\"location\":\"${LOCATION}\",\"ipmi_host\":\"${IPMI_HOSTNAME}\"}"
  INTERFACE_PAYLOAD="{\"name\": \"eth0\", \"server\": \"${HOSTNAME}\", \"mac\": \"${MAC}\"}"

  curl -X POST \
    -H "Authorization: Token ${API_TOKEN}" \
    -H 'Content-Type: application/json' \
    -H 'Accepts: application/json' \
    -d "${SERVER_PAYLOAD}" \
    "${BOOTLOADER_URL}/api/servers/"

  curl -X POST \
    -H "Authorization: Token ${API_TOKEN}" \
    -H 'Content-Type: application/json' \
    -H 'Accepts: application/json' \
    -d "${INTERFACE_PAYLOAD}" \
    "${BOOTLOADER_URL}/api/interfaces/"
done
