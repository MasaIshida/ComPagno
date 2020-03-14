import requests
from . import property
import json

def main(text, source, target):
    """
    翻訳機能実装メゾット
     グーグル翻訳へリクエストを送りその結果を元に
     翻訳機能を提供する

    :param text: 翻訳対象
    :param source: 記述語
    :param target: 翻訳語
    :return: 翻訳した内容
    """

    # リクエストパラメーターをセット
    payload = {'text': text, 'source': source, 'target': target}

    # 翻訳リクエストを実行
    response = requests.get(property.url, params=payload)

    # リクエストに成功した場合
    if response.status_code == 200:
        data = response.text.replace('{"code":200,"text":"', "").replace('"}', "")
        return data

    return None
