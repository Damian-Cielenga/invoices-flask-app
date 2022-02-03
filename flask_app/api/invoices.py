from xeroApi import xero_api
import xml.etree.ElementTree as ET

def get_invoices(id):
    """
    Gets job data for a specific job id from Workflowmax
    :param job_id :type str
    :return job data :type Any
    """
    data = xero_api(f"invoice.api/get/{id}/")
    
    # save current invoices
    with open(f"xml/{id}.xml", "w", encoding="utf-8") as file:
        file.write(str(data))

