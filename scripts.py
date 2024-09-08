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
    if status == "200":
        return True
    elif status == "400":
        return "(400) Query String Error"
    elif status == "403":
        return "(403) Permission Denied"
    elif status == "404":
        return "(404) Not Found"
    elif status == "500":
        return "(500) Internal Server Error"
    else:
        return "(Unknown) Error"


def function_getOverview():
    data = requests.get(ADDRESS + "/api/overview?apikey=" + API_KEY, headers=headers).json()
    status = function_statusCheck(data)
    if status is True:
        # Data
        return
    else:
        return status
