#This script is used to authenticate between the device with IBM cloud function

#Uncomment the commented lines with change of some parameters will allow for IBM IAM authentication 
#process to work. Do this if the device architechure is supported by IBM Cloud Cli. :)
#follow instructions from following links will guide you through the difference. 
#IBM IAM example: "https://cloud.ibm.com/apidocs/functions?code=python#getactivationbyid"
#IBM web action: "https://cloud.ibm.com/docs/openwhisk?topic=openwhisk-actions_web#http_redirect"

from os import RTLD_DEEPBIND, replace, truncate
import re
import subprocess
from subprocess import check_output
import http.client
import json
def api_key_request(namespace,password):
    #secrect= check_output("ibmcloud iam oauth-tokens", shell = True, encoding='utf-8')
    #sec = secrect.split("IAM token:  ",1)[1]
    #sec = sec.split("\n",1)[0]
    action_name = 'Get%20request'
    #   print(key)
    headers = {
        'accept': "application/json",
        #'authorization': sec,
        'content-type': "application/json"
    }
    conn = http.client.HTTPSConnection("us-south.functions.appdomain.cloud")

    conn.request("POST", f"/api/v1/web/{namespace}/default/{action_name}.json",body=json.dumps(password).encode('utf-8'), headers=headers)

    res = conn.getresponse()
    data = res.read()
    #print(json.loads(data.decode("utf-8"))['ibm_info'])
    return json.loads(data.decode("utf-8"))['ibm_info']
