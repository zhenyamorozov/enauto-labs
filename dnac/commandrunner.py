"""

This script uses the always-on DNA Center DevNet sandbox: Catalyst Center Always-On v2.3.3.6

"""

import requests
import json

system_url = "https://sandboxdnac.cisco.com/dna/system/api/v1"
intent_url = "https://sandboxdnac.cisco.com/dna/intent/api/v1"
username = "devnetuser"
password = "Cisco123!"

# 1. Authenticate
resp = requests.post(
    system_url + "/auth/token",
    auth=requests.auth.HTTPBasicAuth(username, password),
    verify = False
)

auth_token = resp.json()['Token']

# 2. Get the list of devices
resp = requests.get(
    intent_url + "/network-device",
    headers={'X-Auth-Token': auth_token, 'Content-Type': 'application/json'},
    verify=False
)

devices = resp.json()['response']

# 3. Request commands to run with CommandRunner
resp = requests.post(
    intent_url + "/network-device-poller/cli/read-request",
    headers={'X-Auth-Token': auth_token, 'Content-Type': 'application/json'},
    json={
        'deviceUuids': [device['id'] for device in devices],
        'commands': ["show version", "show ip interface brief", "show ip route"]
    },
    verify=False
)

taskId = resp.json()['response']['taskId']

# 4. Wait for task to complete
while True:
    resp = requests.get(
        intent_url + "/task/{taskId}".format(taskId=taskId),
        headers={'X-Auth-Token': auth_token, 'Content-Type': 'application/json'},
        verify=False
    )
    if 'endTime' in resp.json()['response']:
        break
    # perhaps needs a delay, but works on the 1st iteration
fileId = json.loads(resp.json()['response']['progress'])['fileId']

# 5. Retrieve the file 
resp = requests.get(
    intent_url + "/file/{fileId}".format(fileId=fileId),
    headers={'X-Auth-Token': auth_token, 'Content-Type': 'application/json'},
    verify=False
)
outputs = resp.json()

for device in outputs:
    print(f"****** DEVICE ID: {device['deviceUuid']} ******")
    for command in device['commandResponses']['SUCCESS']:
        print(f"------ COMMAND: {command} ------")
        print(device['commandResponses']['SUCCESS'][command])

    print()



