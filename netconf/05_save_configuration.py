from ncclient import manager, xml_
from xml.dom.minidom import parseString

## Save configuration from running to strtup

# Explicitly calling the RPC from a model
netconf_body = """
<cisco-ia:save-config xmlns:cisco-ia="http://cisco.com/yang/cisco-ia"/>
"""

with manager.connect(
    host="10.10.20.48",
    port=830,
    username="developer",
    password="C1sco12345",
    hostkey_verify=False,
    timeout=None
) as m:
    # dispatch method send a custom RPC operation
    netconf_reply = m.dispatch(xml_.to_ele(netconf_body))

    xml = parseString(netconf_reply.xml).toprettyxml()
    print(xml)
    if "Save running-config successful" in xml:
        print("Success!")

