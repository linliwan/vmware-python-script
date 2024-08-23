# Do not produce pycache
import sys
sys.dont_write_bytecode = True

import requests
import urllib3
from vmware.vapi.vsphere.client import create_vsphere_client
from com.vmware.vcenter_client import VM

from credential import credential
from pprint import pprint

# Disable cert verification & secure connection warning for demo purpose. 
session = requests.session()
session.verify = False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Connect to a vCenter Server using username and password
vsphere_client = create_vsphere_client(server=credential['server'], username=credential['username'], password=credential['password'], session=session)

vm_name = 'MGMT-remotedesk53'
vm_list = vsphere_client.vcenter.VM.list(VM.FilterSpec(names=set([vm_name])))

if vm_list:
    vm_id = vm_list[0].vm
    print(f"VM '{vm_name}' ID is: {vm_id}")
else:
    print(f"Can not find '{vm_name}'.")

for i in range(1, 3):
    clone_name = f"MyClonedVM_{i}"
    clone_spec = VM.CloneSpec(name=clone_name, source=vm_id)
    cloned_vm_id = vsphere_client.vcenter.VM.clone(clone_spec)
    print(f"Clone Success: {clone_name} -> ID: {cloned_vm_id}")
