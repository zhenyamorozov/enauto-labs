from ncclient import manager

m = manager.connect(
    host="10.10.20.48",
    port=830,
    username="developer",
    password="C1sco12345",
    hostkey_verify=False,
    timeout=None
)
print(m)

# print all capabilities
for capability in m.server_capabilities:
    print(capability)

# find and print the specific capability
print()
print(next(capability for capability in m.server_capabilities if "urn:ietf:params:xml:ns:yang:ietf-interfaces" in capability))

# capability is an object
capa = m.server_capabilities[capability]
print()
print(capa.namespace_uri)
print(capa.get_abbreviations())

m.close_session()
pass