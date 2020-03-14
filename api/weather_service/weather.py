import requests
import ast
from . import property


def main(nation):

    # リクエストパラメーターをセット
    payload = {'appid': property.api_key, 'id': nation}

    response = requests.get(property.url, params=payload)

    dic = ast.literal_eval(response.text)

    return dic

