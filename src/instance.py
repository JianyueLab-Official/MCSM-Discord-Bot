import os
import requests
from shared import *


def function_instanceDetail(uuid, daemon_id):
    response = requests.get(
        ADDRESS
        + "/api/instance?apikey="
        + API_KEY
        + "&uuid="
        + uuid
        + "&daemonId="
        + daemon_id,
        headers=headers,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "uuid": response["data"]["instanceUuid"],
            "instance_status": function_instanceStatusCheck(response["data"]["status"]),
            "nickname": response["data"]["config"]["nickname"],
            "autoStart": function_trueFalseJudge(
                response["data"]["config"]["eventTask"]["autoStart"]
            ),
            "autoRestart": function_trueFalseJudge(
                response["data"]["config"]["eventTask"]["autoRestart"]
            ),
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
        json=request_body,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            # data process
        }
        return data_set
    else:
        return status


def function_deleteInstance(uuid, daemon_id, delete_file):
    # only delete once at time
    request_body = {"uuids": [uuid], "deleteFile": delete_file}

    response = requests.delete(
        ADDRESS + "/api/instance?&apikey=" + API_KEY + "&daemonId=" + daemon_id,
        headers=headers,
        json=request_body,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        if response["data"] is True:
            data_set = {
                "status": response["status"],
                "uuid": uuid,
                "time": response["time"],
                "message": "Instance has been deleted.",
            }

        else:
            data_set = {
                "status": response["status"],
                "uuid": uuid,
                "time": response["time"],
                "message": "Instance has NOT been deleted.",
            }

        return data_set

    else:
        return status


def function_startInstance(uuid, daemon_id):
    response = requests.get(
        ADDRESS
        + "/api/protected_instance/open?apikey="
        + API_KEY
        + "&daemonId="
        + daemon_id
        + "&uuid="
        + uuid,
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
        ADDRESS
        + "/api/protected_instance/stop?apikey="
        + API_KEY
        + "&daemonId="
        + daemon_id
        + "&uuid="
        + uuid,
        headers=headers,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "uuid": uuid,
            "time": response["time"],
            "message": "Instance has been stopped.",
        }
        return data_set
    else:
        return status


def function_restartInstance(uuid, daemon_id):
    response = requests.get(
        ADDRESS
        + "/api/protected_instance/restart?apikey="
        + API_KEY
        + "&uuid="
        + uuid
        + "&daemonId="
        + daemon_id,
        headers=headers,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "uuid": uuid,
            "time": response["time"],
            "message": "Instance has been restarted.",
        }
        return data_set
    else:
        return status


def function_killInstance(uuid, daemon_id):
    response = requests.get(
        ADDRESS
        + "/api/protect_instance/kill?apikey="
        + API_KEY
        + "&uuid="
        + uuid
        + "&daemonId="
        + daemon_id,
        headers=headers,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "uuid": uuid,
            "time": response["time"],
            "message": "Instance has been killed.",
        }
        return data_set
    else:
        return status


def function_sendCommand(uuid, daemon_id, command):
    response = requests.get(
        ADDRESS
        + "/api/protected_instance/command?apikey="
        + API_KEY
        + "&uuid="
        + uuid
        + "&daemonId="
        + daemon_id
        + "&command="
        + command,
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
        ADDRESS
        + "/api/protected_instance/outputlog?apikey="
        + API_KEY
        + "&uuid="
        + uuid
        + "&daemonId="
        + daemon_id
        + "&size="
        + OUTPUT_SIZE,
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
