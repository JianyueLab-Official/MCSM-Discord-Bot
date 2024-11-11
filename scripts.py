import os

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
ADDRESS = os.getenv('MCSMANAGER_ADDRESS')
API_KEY = os.getenv('MCSMANAGER_API_KEY')
OUTPUT_SIZE = os.getenv('OUT_PUT_SIZE')
PAGE_SIZE = os.getenv('PAGE_SIZE')
PAGE = os.getenv('PAGE')

headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json; charset=UTF-8",
}

PAGE_SIZE_PAGE = f"&page_size={PAGE_SIZE}&page={PAGE}"

instanceData = {}
daemonData = {}
userData = {}


def function_trueFalseJudge(data):
    if data is True:
        return '✅'
    elif data is False:
        return '❌'
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


def function_fetchDaemonData():
    data = requests.get(
        ADDRESS + f"/api/overview?apikey={API_KEY}"
    ).json()

    daemons = data["data"]["remote"]

    for daemon in daemons:
        daemon_uuid = daemon["uuid"]
        remarks = daemon["remarks"]
        daemonData[remarks] = daemon_uuid

    daemon_ids = daemonData.values()

    for daemon_id in daemon_ids:
        data = requests.get(
            ADDRESS + f"/api/service/remote_service_instances?daemonId={daemon_id}{PAGE_SIZE_PAGE}&status=&instance_name=&apikey={API_KEY}",
            headers=headers,
        ).json()

        instances = data["data"]["data"]

        for instance in instances:
            instance_id = instance["instanceUuid"]
            nickname = instance["config"]["nickname"]
            instanceData[nickname] = {}
            instanceData[nickname]["uuid"] = instance_id
            instanceData[nickname]["daemonId"] = daemon_id

    return


def function_fetchUserData():
    response = requests.get(
        ADDRESS + "/api/auth/search?apikey=" + API_KEY + "&userName=&role=&" + PAGE_SIZE_PAGE,
        headers=headers
    ).json()

    users = response["data"]["data"]

    for user in users:
        userName = user["userName"]
        userId = user["uuid"]
        userData[userName] = userId

    return


def function_getOverview():
    response = requests.get(
        ADDRESS + "/api/overview?apikey=" + API_KEY,
        headers=headers
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


def function_searchUser(username):
    response = requests.get(
        ADDRESS + "/api/auth/search&apikey=" + API_KEY + "&username=" + username + PAGE_SIZE_PAGE,
        headers=headers
    ).json()

    status = function_statusCheck(response)

    if status is True:
        if response["data"]["data"]["uuid"] is not None:
            data_set = {
                "status": response["status"],
                "uuid": response["data"]["data"]["uuid"],
                "username": response["data"]["data"]["username"],
                "permission": function_permissionCheck(response["data"]["data"]["permission"]),
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
    request_body = {
        "username": username,
        "password": password,
        "permission": role
    }

    response = requests.post(
        ADDRESS + "/api/auth?apikey=" + API_KEY,
        headers=headers,
        json=request_body
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
        ADDRESS + "/api/auth?apikey=" + API_KEY,
        headers=headers,
        json=request_body
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


def function_instanceDetail(uuid, daemon_id):
    response = requests.get(
        ADDRESS + "/api/instance?apikey=" + API_KEY + "&uuid=" + uuid + "&daemonId=" + daemon_id,
        headers=headers
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "uuid": response["data"]["instanceUuid"],
            "instance_status": function_instanceStatusCheck(response["data"]["status"]),
            "nickname": response["data"]["config"]["nickname"],
            "autoStart": function_trueFalseJudge(response["data"]["config"]["eventTask"]["autoStart"]),
            "autoRestart": function_trueFalseJudge(response["data"]["config"]["eventTask"]["autoRestart"]),
        }
        return data_set
    else:
        return status


def function_createInstance(daemon_id):
    request_body = {
        # missing request body
    }

    response = requests.post(
        ADDRESS + "/api/instance?apikey=" + API_KEY + "&daemonId=" + daemon_id,
        headers=headers,
        json=request_body
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            # data process
        }
        return data_set
    else:
        return status


def function_updateConfig(uuid, daemon_id):
    request_body = {
        # missing request body
    }

    response = requests.put(
        ADDRESS + "/api/instance?&apikey=" + API_KEY + "&daemonId=" + daemon_id + "&uuid=" + uuid,
        headers=headers,
        json=request_body
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            # missing data process
        }
        return data_set
    else:
        return status


def function_deleteInstance(uuid, daemon_id, delete_file):
    # only delete once at time
    request_body = {
        "uuids": [
            uuid
        ],
        "deleteFile": delete_file
    }

    response = requests.delete(
        ADDRESS + "/api/instance?&apikey=" + API_KEY + "&daemonId=" + daemon_id,
        headers=headers,
        json=request_body
    ).json()

    status = function_statusCheck(response)

    if status is True:
        if response["data"] is True:
            data_set = {
                "status": response["status"],
                "uuid": uuid,
                "time": response["time"],
                "message": "Instance has been deleted."
            }

        else:
            data_set = {
                "status": response["status"],
                "uuid": uuid,
                "time": response["time"],
                "message": "Instance has NOT been deleted."
            }

        return data_set

    else:
        return status


def function_startInstance(uuid, daemon_id):
    response = requests.get(
        ADDRESS + "/api/protected_instance/open?apikey=" + API_KEY + "&daemonId=" + daemon_id + "&uuid=" + uuid,
        headers=headers,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "uuid": uuid,
            "time": response["time"],
        }
        return data_set
    else:
        return status


def function_stopInstance(uuid: str, daemon_id: str):
    response = requests.get(
        ADDRESS + "/api/protected_instance/stop?apikey=" + API_KEY + "&daemonId=" + daemon_id + "&uuid=" + uuid,
        headers=headers,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "uuid": uuid,
            "time": response["time"],
            "message": "Instance has been stopped."
        }
        return data_set
    else:
        return status


def function_restartInstance(uuid, daemon_id):
    response = requests.get(
        ADDRESS + "/api/protected_instance/restart?apikey=" + API_KEY + "&uuid=" + uuid + "&daemonId=" + daemon_id,
        headers=headers,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "uuid": uuid,
            "time": response["time"],
            "message": "Instance has been restarted."
        }
        return data_set
    else:
        return status


def function_killInstance(uuid, daemon_id):
    response = requests.get(
        ADDRESS + "/api/protect_instance/kill?apikey=" + API_KEY + "&uuid=" + uuid + "&daemonId=" + daemon_id,
        headers=headers,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "uuid": uuid,
            "time": response["time"],
            "message": "Instance has been killed."
        }
        return data_set
    else:
        return status


def function_sendCommand(uuid, daemon_id, command):
    response = requests.get(
        ADDRESS + "/api/protected_instance/command?apikey=" + API_KEY + "&uuid=" + uuid + "&daemonId=" + daemon_id + "&command=" + command,
        headers=headers,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "uuid": uuid,
        }
        return data_set
    else:
        return status


def function_getOutput(uuid, daemon_id):
    response = requests.get(
        ADDRESS + "/api/protected_instance/outputlog?apikey=" + API_KEY + "&uuid=" + uuid + "&daemonId=" + daemon_id + "&size=" + OUTPUT_SIZE,
        headers=headers,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "data": response["data"],
        }
        return data_set
    else:
        return status


def function_addNode(ip, port, remarks, daemon_apikey):
    request_body = {
        "ip": ip,
        "port": port,
        "remarks": remarks,
        "apikey": daemon_apikey,
    }

    response = requests.post(
        ADDRESS + "/api/service/remote_service?apikey=" + API_KEY,
        json=request_body,
        headers=headers
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "data": response["data"],
            "message": "Node(Daemon) has been added."
        }
        return data_set
    else:
        return status


def function_deleteNode(daemon_id):
    response = requests.delete(
        ADDRESS + "/api/service/remote_service?apikey=" + API_KEY + "&uuid=" + daemon_id,
        headers=headers,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "data": response["data"],
            "message": "Node(Daemon) has been deleted."
        }
        return data_set
    else:
        return status


def function_tryNode(daemon_id):
    response = requests.get(
        ADDRESS + "/api/service/link_remote_service?apikey=" + API_KEY + "&uuid=" + daemon_id,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "data": response["data"],
            "message": "Node(Daemon) has been tried."
        }
        return data_set
    else:
        return status


def function_updateDaemon(daemon_id, ip, port, remarks, daemon_apikey):
    request_body = {
        "uuid": daemon_id,
        "ip": ip,
        "port": port,
        "prefix": "",
        "available": false,
        "remarks": remarks,
        "apiKey": daemon_apikey
    }

    response = requests.put(
        ADDRESS + "/api/service/remote_service?apikey=" + API_KEY,
        json=request_body,
        headers=headers
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "data": response["data"],
            "time": response["time"],
        }

        return data_set
    else:
        return status