import os
import requests
from shared import *


def function_fetchDaemonData():
    data = requests.get(ADDRESS + f"/api/overview?apikey={API_KEY}").json()

    daemons = data["data"]["remote"]

    for daemon in daemons:
        daemon_uuid = daemon["uuid"]
        remarks = daemon["remarks"]
        daemonData[remarks] = daemon_uuid

    daemon_ids = daemonData.values()

    for daemon_id in daemon_ids:
        data = requests.get(
            ADDRESS
            + f"/api/service/remote_service_instances?daemonId={daemon_id}{PAGE_SIZE_PAGE}&status=&instance_name=&apikey={API_KEY}",
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
        headers=headers,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "data": response["data"],
            "message": "Node(Daemon) has been added.",
        }
        return data_set
    else:
        return status


def function_deleteNode(daemon_id):
    response = requests.delete(
        ADDRESS
        + "/api/service/remote_service?apikey="
        + API_KEY
        + "&uuid="
        + daemon_id,
        headers=headers,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "data": response["data"],
            "message": "Node(Daemon) has been deleted.",
        }
        return data_set
    else:
        return status


def function_tryNode(daemon_id):
    response = requests.get(
        ADDRESS
        + "/api/service/link_remote_service?apikey="
        + API_KEY
        + "&uuid="
        + daemon_id,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            "status": response["status"],
            "data": response["data"],
            "message": "Node(Daemon) has been tried.",
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
        "apiKey": daemon_apikey,
    }

    response = requests.put(
        ADDRESS + "/api/service/remote_service?apikey=" + API_KEY,
        json=request_body,
        headers=headers,
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


def function_updateConfig(uuid, daemon_id):
    request_body = {
        # missing request body
    }

    response = requests.put(
        ADDRESS
        + "/api/instance?&apikey="
        + API_KEY
        + "&daemonId="
        + daemon_id
        + "&uuid="
        + uuid,
        headers=headers,
        json=request_body,
    ).json()

    status = function_statusCheck(response)

    if status is True:
        data_set = {
            # missing data process
        }
        return data_set
    else:
        return status
