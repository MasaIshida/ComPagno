import requests
from . import property

def main(message, token):

    # url https://notify-bot.line.me/ja/
    headers = {'Authorization': 'Bearer ' + token}

    payload = {'message': message}

    response = requests.post(property.url, headers=headers, params=payload)