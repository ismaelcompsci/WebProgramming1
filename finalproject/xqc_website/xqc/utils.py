import requests
import json

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
    my_params = {"user_login" : username }
    response = requests.get(endpoint, headers=headers, params=my_params)
    data = response.json()
    return data



def get_user_chat_logs(chat_user):
    endpoint = f'https://logs.ivr.fi/channel/xqc/user/{chat_user}'
    headers = {"Content-Type": "application/json", "accept": "application/json" }

    response = requests.get(endpoint, headers=headers)
    data = response.text
    return data