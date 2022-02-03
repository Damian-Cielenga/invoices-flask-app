from datetime import datetime
from typing import Any, Dict, Union
from dotenv import load_dotenv
from enum import Enum, unique
from requests_oauthlib import OAuth2Session
from requests.models import Response
from xml.etree import ElementTree
from time import sleep
from utils import xml_to_json
from custom_logger import logger
import os
import json

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")
WORKFLOWMAX_BASE_URL = "https://api.xero.com/workflowmax/3.0"

TOKEN_PATH = "./token.json"


@unique
class CallMethods(Enum):
    get = "GET"
    post = "POST"

   
def get_token_from_file():
    """
    Retrieves the token from the configures json-file, for the token
    :return token :type Any|None
    """
    data = None
    with open(TOKEN_PATH, encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


def save_token_to_file(token: Any):
    """
    saves auth_token to file
    :param token :type any 
    """
    json_string = json.dumps(token, indent=2)
    with open(TOKEN_PATH, "w") as json_file:
        json_file.write(json_string)


def update_expire_time():
    """
    Updates the expiry time by calculating the passed time 
    """
    token = get_token_from_file() 
    expires_at: int = token["expires_at"]

    token["expires_in"] = int((
        datetime.fromtimestamp(expires_at) - datetime.now()
    ).total_seconds())

    save_token_to_file(token)

CLIENT = OAuth2Session(
    CLIENT_ID,
    token=get_token_from_file(),
    auto_refresh_url="https://identity.xero.com/connect/token",
    auto_refresh_kwargs={
        "client_id": CLIENT_ID,
        "client_secret": os.getenv("CLIENT_SECRET"),
    },
    token_updater=save_token_to_file
)


def request(
    url: str,
    method: CallMethods,
    headers: "Dict[str, str] | None" = None,
    data: "Dict[str, Any] | None" = None
) -> "None|Response":
    """
    :param url :type str
    :param methode :type CallMethods
    :return :type None|Reponse
    """
    response: "None|Response" = None

    logger.info(f"Request: {url}")
    if method.value == 'GET':
        response = CLIENT.get(url, headers=headers)
    elif method.value == 'POST':
        response = CLIENT.post(url, headers=headers, data=data)

    if response.status_code != 200:
        logger.error("Request - ERROR:")
        logger.error(response.reason)
    else:
        logger.info("Request - OK")
    return response


def xero_api(endpoint: str) -> Union[Any, bytes]: 
    """
    Calls the XeroAPI with the given endpoint
    :param endpoint :type str
    :param convert_xml_to_json type: bool :default False
    :return response :type Response
    """
    url: str = f"{WORKFLOWMAX_BASE_URL}/{endpoint}"
    headers: "Dict[str, str]" = {
        "xero-tenant-id": TENANT_ID
    }
    update_expire_time()

    response: Response = request(url, CallMethods.get, headers)
    data: "Union[Any, bytes]" = response.content

    if response.headers.get("X-MinLimit-Remaining", None) == "1":
        logger.info("Reached API Call Limit, sleep for 60 seconds")
        sleep(60)   

    tree = ElementTree.fromstring(data)
    if tree.find("Status").text == "ERROR":
        error_description: str = tree.find("Status/ErrorDescription").text
        logger.error("API Call failed!")
        logger.error(error_description)
        data = {}

    return data