import json
import requests

from bootloader.settings import SLACK_HOOK_URL, SLACK_CHANNEL
from tools.notifications import ThirdPartyAPIException


class Message():
    def __init__(self, message):
        if SLACK_HOOK_URL and SLACK_CHANNEL:
            r = requests.post(
                SLACK_HOOK_URL,
                data={
                    'payload': json.dumps({
                        'channel': SLACK_CHANNEL,
                        'username': 'bootloader',
                        'text': message,
                        'icon_emoji': ':rocket:'
                    })
                })
            if r.status_code != 200:
                raise ThirdPartyAPIException(
                    "Slack API got back not 200-status: %s" % (r.status_code,))
        else:
            print('Slack notification requested but slack is not configured')
