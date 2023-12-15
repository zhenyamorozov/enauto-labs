from ncclient import manager
from xml.dom.minidom import parseString

## Remove a loopback interface

# XML template for interface to be removed, ietf-interfaces
netconf_interface_template = """
  <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
      <interface operation="delete">
        <name>{name}</name>
      </interface>
    </interfaces>
  </config>"""

# Ask user for the interface details
remove_if = {}
remove_if['name'] = "Loopback" + input("Loopback number to delete? ")

netconf_data = netconf_interface_template.format(**remove_if)    # unpack dict into args


with manager.connect(
    host="10.10.20.48",
    port=830,
    username="developer",
    password="C1sco12345",
    hostkey_verify=False,
    timeout=None
) as m:
    # <edit-config> updates part of configuration
    netconf_reply = m.edit_config(netconf_data, target="running")

    xml = parseString(netconf_reply.xml).toprettyxml()
    print(xml)
    if "<ok/>" in xml:
        print("Success!")

