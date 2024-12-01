import os
import requests
from shared import *

def function_trueFalseJudge(data):
    if data is True:
        return "✅"
    elif data is False:
        return "❌"
    else:
        return None


def function_statusCheck(data):
    status = data["status"]

    match status:
        case 200:
            return True
        case 400 | 403:
            data_set = {
                "status": 400,
                "message": "(400) Query String Error",
            }
        case 404:
            data_set = {
                "status": 400,
                "message": "(404) Permission Denied",
            }
        case 500:
            data_set = {
                "status": 500,
                "message": "(500) Internal Server Error",
            }
        case _:
            data_set = {
                "status": 500,
                "message": "(Bot) Internal Server Error",
            }

    return data_set


def function_permissionCheck(code):
    match code:
        case 10:
            return "Admin"
        case 1:
            return "User"
        case -1:
            return "Banned"
        case _:
            return "Unknown"


def function_instanceStatusCheck(data):
    match data:
        case 3:
            return "Running"
        case 2:
            return "Starting"
        case 1:
            return "Stopping"
        case 0:
            return "Stopped"
        case -1:
            return "Maintenance"
        case _:
            return "Unknown"


def function_daemonNameIdTrans(instance_name):
    uuid = instanceData[instance_name]["uuid"]
    daemon_id = instanceData[instance_name]["daemonId"]
    return uuid, daemon_id


def function_userNameIdTrans(user_name):
    uuid = userData[user_name]["uuid"]
    return uuid


def function_nodeNameIdTrans(node_name):
    daemonId = daemonData[node_name]
    return daemonId


def function_getOverview():
    response = requests.get(
        ADDRESS + "/api/overview?apikey=" + API_KEY, headers=headers
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "panel_version": response["data"]["version"],
            "specified_daemon_version": response["data"]["specifiedDaemonVersion"],
            "record_login": response["data"]["record"]["logined"],
            "record_illegal_access": response["data"]["record"]["illegalAccess"],
            "record_banned_ips": response["data"]["record"]["banips"],
            "record_login_failed": response["data"]["record"]["loginFailed"],
            "remote_available": response["data"]["remoteCount"]["available"],
            "remote_total": response["data"]["remoteCount"]["total"],
        }
        return data_set
    else:
        return status
