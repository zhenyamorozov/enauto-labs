from ncclient import manager
from xml.dom.minidom import parseString

## Add a loopback interface

# XML template for interface configuration ietf-interfaces
netconf_interface_template = """
  <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
      <interface>
        <name>{name}</name>
        <description>{desc}</description>
        <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
          {type}
        </type>
        <enabled>{status}</enabled>
        <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
          <address>
            <ip>{ip_address}</ip>
            <netmask>{mask}</netmask>
          </address>
        </ipv4>
      </interface>
    </interfaces>
  </config>"""

# Ask user for the interface details
new_if = {}
new_if['name'] = "Loopback" + input("Loopback number to add? ")
new_if['desc'] = input("Description of the interface? ")
new_if['type'] = "ianaift:softwareLoopback"
new_if['status'] = "true"
new_if['ip_address'] = input("Interface IP address? ")
new_if['mask'] = input("Interface IP network mask? ")

netconf_data = netconf_interface_template.format(**new_if)    # unpack dict into args


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

