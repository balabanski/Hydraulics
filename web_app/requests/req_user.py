import json
import urllib
from urllib import request
import requests
import subprocess

from backend.src.core.config import settings


def sign_up(data_: dict):
    data = json.dumps(data_).encode('UTF-8')
    url = f'http://{settings.DOMAIN}:80{settings.API_V1_STR}/users/create-user-open'

    req = urllib.request.Request(url, data) #
    req.add_header('accept', 'application/json')
    req.add_header('Content-Type', 'application/json')

    try:
        res = urllib.request.urlopen(req)
        data_res_str = res.read().decode('UTF-8')
        data_res_dict = json.loads(data_res_str)
        return data_res_dict

    except Exception as e:
        for item in e.fp:
            print(item, '\n', type(item), '\n', "urllib sign_up хренушки".center(50, '*'))
        try:
            return json.loads(item.decode('utf-8'))
        except:
            pass

def req_access_token(email_, password_):

    data = urllib.parse.urlencode({
                       "username": f'{email_}',
                       "password": f'{password_}',
                       }).encode('UTF-8')
    print('data=json.dumps(data)______________', data)

    url = f'http://{settings.DOMAIN}:80{settings.API_V1_STR}/login/access-token'

    req = request.Request(url, data=data)
    req.add_header('accept', 'application/json')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')

    res = request.urlopen(req)
    response = res.read()

    return json.loads(response)['access_token']


def read_user_me(token_):
    url = f'http://{settings.DOMAIN}:80{settings.API_V1_STR}/users/me'
    req = request.Request(url, data=None)
    req.add_header('accept', 'application/json')
    req.add_header('Authorization', f'Bearer {token_}')
    res = request.urlopen(req)


def update_user_me(token_, data_: dict = None):
    url = f'http://{settings.DOMAIN}:80{settings.API_V1_STR}/users/update-me'
    try:
        # пробую urllib
        data = json.dumps(data_).encode("UTF-8")
        # data = urllib.parse.urlencode(data_).encode('UTF-8')
        # print('data_________', data, '\n', type(data))

        req = urllib.request.Request(url, data=data)
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36')
        req.add_header('accept', 'application/json')
        req.add_header('Authorization', f'Bearer {token_}')
        req.add_header('Content-Type', 'application/json')
        res_ = request.urlopen(req)
        # res_ = json.loads(res_)

    except Exception as e:
        for item in e.fp:
            print(item, '\n',type(item), '\n', "urllib хренушки".center(50, '*'))

        # пробую requests
        headers = {
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'accept': 'application/json',
            'Authorization': f'Bearer {token_}',
            'Content-Type': 'application/json',
        }
        response = requests.post(url, headers=headers, json=data_, allow_redirects=True)
        res_ = json.loads(response.text)
        # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

        if response.text == '{"detail":"Method Not Allowed"}':
            print("requests хренушки".center(50, '*'))

            #  # пробую os
            json_data_str = json.dumps(data_)  # str
            # req_str = """curl -X 'PUT'  {} \
            #   -H 'accept: application/json' \
            #   -H 'Authorization: Bearer {}' \
            #   -H 'Content-Type: application/json' \
            #   -d '{}'""".format(url, token_, json_data_str)
            # # os.system(req_str)
            res_ = subprocess.check_output(['curl', '-X', 'PUT', f'{url}', '-H', 'accept: application/json', '-H',
                                            'Authorization: Bearer {}'.format(token_),
                                            '-H', 'Content-Type: application/json', '-H',
                                            'Content-Type: application/json',
                                            '-d', json_data_str])
            res_ = json.loads(res_.decode('utf-8'))

    if res_.get("id"):
        print(res_.get("id"))
        return res_.get("id")




