import os
import requests
from shared import *

def function_fetchUserData():
    response = requests.get(
        ADDRESS
        + "/api/auth/search?apikey="
        + API_KEY
        + "&userName=&role=&"
        + PAGE_SIZE_PAGE,
        headers=headers,
    ).json()

    users = response["data"]["data"]

    for user in users:
        userName = user["userName"]
        userId = user["uuid"]
        userData[userName] = userId

    return


def function_searchUser(username):
    response = requests.get(
        ADDRESS
        + "/api/auth/search&apikey="
        + API_KEY
        + "&username="
        + username
        + PAGE_SIZE_PAGE,
        headers=headers,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        if response["data"]["data"]["uuid"] is not None:
            data_set = {
                "status": response["status"],
                "uuid": response["data"]["data"]["uuid"],
                "username": response["data"]["data"]["username"],
                "permission": function_permissionCheck(
                    response["data"]["data"]["permission"]
                ),
                "registerTime": response["data"]["data"]["registerTime"],
                "loginTime": response["data"]["data"]["loginTime"],
                "2fa": function_trueFalseJudge(response["data"]["data"]["open2fa"]),
            }
        else:
            data_set = {
                "message": "User not found",
            }
        return data_set
    else:
        return status


def function_createUser(username: str, password: str, role: int):
    request_body = {"username": username, "password": password, "permission": role}

    response = requests.post(
        ADDRESS + "/api/auth?apikey=" + API_KEY, headers=headers, json=request_body
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "user_uuid": response["data"]["uuid"],
        }
        return data_set
    else:
        return status


def function_deleteUser(user_uuid):
    request_body = [user_uuid]

    response = requests.delete(
        ADDRESS + "/api/auth?apikey=" + API_KEY, headers=headers, json=request_body
    ).json()

    status = function_statusCheck(response)

    if status is True:
        if response["status"] is True:
            data_set = {
                "status": response["status"],
                "message": "User has been deleted",
            }
        else:
            data_set = {
                "status": response["status"],
                "message": "User has NOT been deleted",
            }
        return data_set
    else:
        return status
