import xmltodict
import json

from typing import Any, Tuple, Union
from datetime import datetime, timedelta
from custom_logger import logger

def xml_to_json(xml: bytes) -> Any:
    """
    Converts xml data to JSON
    :param xml :type bytes
    :return json object :type Any
    """
    try:
        obj = xmltodict.parse(xml)
        json_obj = json.loads(json.dumps(obj))
        return json_obj
    except Exception as e:
        logger.error("Could not parse XML to JSON!")
        raise e


def get_time_range(days_ago: int = 7)  -> Tuple[str, str]: 
    """
    gets the time range in string time format 
    :param starting_date :type datetime
    :param end_date :type datetime
    :return start :type str
    :return end :type str
    """
    starting_date: datetime = datetime.today()
    end_date: datetime = starting_date - timedelta(days=days_ago)

    start: str = end_date.strftime("%Y%m%d")
    end: str = starting_date.strftime("%Y%m%d")
    return start, end 


def minutes_to_hours(minutes: Union[str, int]):
    """
    converts the minutes into hours
    :param mins :type int
    :return hours :type str
    """
    mins: int = int(minutes)
    hours: str = str(timedelta(minutes=mins))[:-3]
    return hours

def format_date(date: str) -> str:
    """
    formatted date into str
    :param date :type datetime
    :return formatted date :type str
    """ 
    date_time_obj: datetime = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    formatted_date = date_time_obj.strftime('%d-%b.-%Y')
    return formatted_date

def convert_boolean_to_yes_or_no(value: str) -> str:
    """
    Converts a given (boolean) value to 'Yes' or 'No'
    :param value :type str
    :return converted value :type str
    """
    converted_value: str = "Yes" if value == "true" else "No"
    return converted_value
