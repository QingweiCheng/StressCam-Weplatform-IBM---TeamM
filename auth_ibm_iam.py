from cloudant.client import Cloudant
from cloudant.query import Query
from getmac import get_mac_address
from change_device_info import read_ibm_info
import subprocess, re
def ibm_auth():
	username = read_ibm_info()['username']
	api_key = read_ibm_info()['api_key']
	return Cloudant.iam(username, api_key, connect=True)

def query_wiotp_info():
	client = ibm_auth()
	serial_info  =str(subprocess.Popen(['cat','/proc/cpuinfo'], stdout=subprocess.PIPE).communicate())
	serial_info = re.search("0000000031644ee9", serial_info)
	selector= {
	      "_id": ""
	}
	doc_id = f"camera_wiotp_info:{serial_info[0]}"
	selector['_id'] = doc_id
	db=client['wiot_platform_camera_credential']
	query = Query(db, partition_key='camera_wiotp_info', selector=selector, skip = 0, limit=1)
	wiotp_login_info= query()['docs'][0]['wiotp_info']
	return wiotp_login_info


