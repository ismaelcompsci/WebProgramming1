import requests
from datetime import datetime
import dateutil.relativedelta
import json
from .models import *

clinetId = "s1x7dpfczuw7ubjealt06jct315ei1"
clinetSecret = "l53spssusq84z1choiptuz30dt028l"
OAUTH_TOKEN = "oauth:c7bpaonlt6mmrhzwoakipdaso0b42d"
username = "authtoken1"


def getAuth():
    url = f"https://id.twitch.tv/oauth2/token?client_id={clinetId}&client_secret={clinetSecret}&grant_type=client_credentials"

    response = requests.post(url)
    data = response.json()

    access_token = data["access_token"]

    authorization = f"Bearer {access_token}"

    headers = {"Authorization": authorization, "Client-Id": clinetId}
    return headers


def is_live(channel):

    endpoint = f"https://api.twitch.tv/helix/streams?user_login={channel}"

    headers = getAuth()
    my_params = {"user_login": username}
    response = requests.get(endpoint, headers=headers, params=my_params)
    data = response.json()
    return data


def get_user_chat_logs(chat_user):
    endpoint = f"https://logs.ivr.fi/channel/xqc/user/{chat_user}"
    headers = {"Content-Type": "application/json", "accept": "application/json"}

    response = requests.get(endpoint, headers=headers)
    data = response.text
    return data


def get_chat_month_year_log(username, month, year):
    endpoint = f"https://logs.ivr.fi/channel/xqc/user/{username}/{year}/{month}"
    headers = {"Content-Type": "application/json", "accept": "application/json"}

    response = requests.get(endpoint, headers=headers)

    data = response.json()
    return data


def api_iter(username):

    start_time = datetime.now()
    while True:
        if start_time.year == 2017:
            break
        data = get_chat_month_year_log(username, start_time.month, start_time.year)[
            "messages"
        ]
        start_time = start_time - dateutil.relativedelta.relativedelta(months=1)
        """ "id": self.id,
            "channel" : self.channel,
            "displayName": self.displayName,
            "raw": self.raw,
            "text": self.text,
            "timestamp": self.timestamp,
            "username": self.username"""
        break

        for item in data:
            obj, created = Chatter.objects.get_or_create(
                channel=item["channel"],
                displayName=item["displayName"],
                raw=item["raw"],
                text=item["text"],
            )
