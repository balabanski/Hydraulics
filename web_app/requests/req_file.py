import json
import urllib
from urllib import request

from web_app.user import get_token

from backend.src.core.config import settings


token = get_token()


async def get_list_files(token_):
    url = f"http://{settings.DOMAIN}:80{settings.API_V1_STR}/files/list%20files"
    req = request.Request(url)
    req.add_header("accept", "application/json")
    req.add_header("Authorization", f"Bearer {token_}")
    try:
        res = request.urlopen(req)
        json_str = res.read().decode("UTF-8")
        data = json.loads(json_str)
        return data
    except urllib.error.HTTPError:
        print("устаревший токен")
    except Exception as e:
        for item in e.fp:
            print(
                item,
                "\n",
                type(item),
                "\n",
                "urllib create_file хренушки".center(50, "*"),
            )


def create_file(name_):
    data = json.dumps({"name": f"{name_}"}).encode("UTF-8")
    print(data)
    url = f"http://{settings.DOMAIN}:80{settings.API_V1_STR}/files/create?name={name_}"

    req = urllib.request.Request(url, data=data)
    # req.add_header('Content-Type', 'application/json')
    req.add_header("accept", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    try:
        res = urllib.request.urlopen(req)
        print(res)
    except Exception as e:
        for item in e.fp:
            print(
                item,
                "\n",
                type(item),
                "\n",
                "urllib create_file хренушки".center(50, "*"),
            )


# token_='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDgxNjAwNTMsInN1YiI6IjMzIn0.xZihP7dzuNdjAp-DvpujRB-263L6ykKb-ncpLR4D298'
def delete_file(id_):
    data = json.dumps({"name": f"{id_}"}).encode("UTF-8")
    print(data)
    url = f"http://{settings.DOMAIN}:80{settings.API_V1_STR}/files/delete?file_id={id_}"
    req = urllib.request.Request(url, data=data)

    req.add_header("accept", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    try:
        request.urlopen(req)
    except Exception as e:
        for item in e.fp:
            print(item, "\n", type(item), "\n", "delete_file ERROR".center(50, "*"))


def update_file(id_, meta_data=None, name=None, directory_id=None):
    print("****************UPDATE*******************************")
    data = {"meta_data": meta_data, "name": name}
    if directory_id:
        data["directory_id"] = directory_id
    data = json.dumps(data).encode("UTF-8")

    url = f"http://{settings.DOMAIN}:80{settings.API_V1_STR}/files/update?file_id={id_}"
    req = request.Request(url, data)
    req.add_header("accept", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        res = request.urlopen(req)
        res_data = json.loads(res.read().decode("UTF-8"))
        print("res_update_data_______________________\n", res_data)
    except Exception as e:
        for item in e.fp:
            print(item, "\n", type(item), "\n", "update_file ERROR".center(50, "*"))


def get_metadata_from_file(id_):
    # data = json.dumps({"name": f'{id_}'}).encode('UTF-8')
    url = f"http://{settings.DOMAIN}:80{settings.API_V1_STR}/files/get%20metadata?file_id={id_}"
    # req = request.Request(url, data=data)
    req = request.Request(url)
    req.add_header("accept", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        res = request.urlopen(req)
        res_data = json.loads(res.read().decode("UTF-8"))
        return res_data
    except Exception as e:
        for item in e.fp:
            print(
                item,
                "\n",
                type(item),
                "\n",
                "urllib get_metadata хренушки".center(50, "*"),
            )
