from operator import inv
from xeroApi import xero_api
import xml.etree.ElementTree as ET
from custom_logger import logger
import jinja2

invoice_id = "I20200422"

# parse xml file
tree = ET.parse(f"xml/{invoice_id}.xml")
root = tree.getroot()


# XPath
ID = root.findall("./ID")[0].text 
DATE = root.findall("./Date")[0].text.split("T")[0]
DUE_DATE = root.findall("./DueDate")[0].text.split("T")[0]
CLIENT = root.findall("./Client/Name")[0].text
CONTACT = root.findall("./Contact/Name")[0].text
TASK_NAME = [x.text for x in root.findall("./Jobs/Job/Tasks/Task/Name")]
TASK_AMOUNT = [float(x.text) for x in root.findall("./Jobs/Job/Tasks/Task/AmountIncludingTax")]
SUM = sum(TASK_AMOUNT)
TASK = zip(TASK_NAME,TASK_AMOUNT)

# json for template
content = {
  "id": ID,
  "date": DATE,
  "due_date": DUE_DATE,
  "client": CLIENT,
  "contact": CONTACT,
  "task": TASK,
  "sum": SUM
}

# set layout
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('template'))
template = jinja_env.get_template('invoice.html')

with open(f"template/{invoice_id}.html", "w", encoding='utf-8') as file:
    file.write(template.render(content))