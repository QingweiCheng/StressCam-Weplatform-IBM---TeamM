from sys import path
path.insert(0,'/home/pi')
path.insert(0,'/usr/local/lib/python3.7/dist-packages/cloudant')
from cloudant.client import Cloudant
from cloudant.query import Query
from change_device_info import read_key_info
import subprocess, re
import authenticate

def ibm_auth():
	key = read_key_info()
	api_info = authenticate.api_key_request(key["namespace"],key["passpharse"])
	username = api_info["user_name"]
	api_key =  api_info["api_key"]
	return Cloudant.iam(username, api_key, connect=True)

def query_wiotp_info():
	client = ibm_auth()
	serial_info  =subprocess.check_output(['cat /proc/cpuinfo'],shell = True, encoding="UTF-8")
	serial_info = re.search("([0-9]*[a-z][a-z]9)", serial_info)
	selector= {
	      "_id": ""
	}
	doc_id = f"camera_wiotp_info:{serial_info[0]}"
	selector['_id'] = doc_id
	db=client['wiot_platform_camera_credential']
	query = Query(db, partition_key='camera_wiotp_info', selector=selector, skip = 0, limit=1)
	wiotp_login_info= query()['docs'][0]['wiotp_info']
	return wiotp_login_info


