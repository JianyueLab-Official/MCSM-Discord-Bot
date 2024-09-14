import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')
ADDRESS = os.getenv('MCSMANAGER_ADDRESS')
API_KEY = os.getenv('MCSMANAGER_API_KEY')

headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json; charset=UTF-8",
}


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


def function_getOverview():
    response = requests.get(ADDRESS + "/api/overview?apikey=" + API_KEY, headers=headers).json()
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


def function_searchUser():
    return


def function_createUser(username: str, password: str, role: int):
    request_body = {"username": username, "password": password, "permission": role}
    response = requests.post(ADDRESS + "/api/auth?apikey=" + API_KEY, headers=headers, json=request_body).json()
    status = function_statusCheck(response)
    if status is True:
        data_set = {
            "status": response["status"],
            "user_uuid": response["data"]["uuid"],
        }
        return data_set
    else:
        return status


def function_updateUser():
    return


def function_deleteUser(user_uuid):
    request_body = [user_uuid]
    data = requests.delete(ADDRESS + "/api/auth?apikey=" + API_KEY, headers=headers, json=request_body).json()
    status = function_statusCheck(response)
    if status is True:
        if data["status"] is True:
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
        return data


def function_instanceList():
    return


def function_instanceDetail():
    return


def function_createInstance():
    return


def function_updateInstance():
    return


def function_deleteInstance():
    return


def function_startInstance():
    return


def function_stopInstance():
    return


def function_restartInstance():
    return


def function_killInstance():
    return


def function_sendCommand():
    return


def function_getOutput():
    return


def function_reinstallInstance():
    return


def function_addNode():
    return


def function_deleteNode():
    return


def function_tryNode():
    return


def function_updateNode():
    return