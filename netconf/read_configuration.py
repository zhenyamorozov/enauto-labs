from ncclient import manager
from xml.dom.minidom import parseString
import xmltodict
import difflib

## Retrieve interfaces info using the ietf-interfaces model

# XML filter for targeted NETCONF queries
netconf_filter = """
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface></interface>
  </interfaces>
</filter>"""

with manager.connect(
    host="10.10.20.48",
    port=830,
    username="developer",
    password="C1sco12345",
    hostkey_verify=False,
    timeout=None
) as m:
    print(m)

    # <get-config> retrives from the specified datastore
    netconf_reply1 = m.get_config(source="running", filter=netconf_filter)
    # <get> retrieves fron 'running' datastore, can also retrieve state data
    netconf_reply2 = m.get(filter=netconf_filter)

    xml1 = parseString(netconf_reply1.xml).toprettyxml()
    xml2 = parseString(netconf_reply2.xml).toprettyxml()

    print(xml1)
    print()
    print(xml2)
    print(xml1 == xml2) # =False, strings are not the same

    for diff in difflib.unified_diff(xml1.split("\n"), xml2.split("\n")):
        print(diff)

        # Show only message ID is different. So, results of <get> and <get-config> are identical.
        # @@ -1,5 +1,5 @@
        #  <?xml version="1.0" ?>
        # -<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:827b41ff-4a69-42bc-96ef-7ad5fcd43ebb">
        # +<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:c3bcc8a4-6c53-4c14-b0d8-09d4bb38b101">    

    interfaces = xmltodict.parse(xml1)['rpc-reply']['data']['interfaces']['interface']
    for interface in interfaces:
        print(
            interface['name'], 
            # interface['description'], 
            interface['enabled'], 
            # interface['ipv4']['address']['ip'], 
            # interface['ipv4']['address']['netmask']
        )