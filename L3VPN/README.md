# Generate config in preparation for deploy of L3VPN
These playbooks will generate relevant config (interface, routing and vrf) for running L3VPN over Cisco IOS-XE devices.

## Overview
The variable files and ansible playbooks used for provisioning of L3VPN:

### Vars
* **fabric.yml** - contains a data model that describes how all devices is connected and how the infrastructure should be configured.
* **services.yml** - describes how the services (in this case L3VPN) should be configured.
* **ip_addresses.yml** - contains all the subnets that is available for generating linknets.

### Playbooks
* **assign_ip_addresses.yml** - generates *fabric_linknets* from the *available_subnets*. The number of linknets generated is based on the number of links from *fabric*. 
If there is already some linknets in *fabric linknets*, it will add or subtract linknets to get the number of linknets correct. Unneeded linknets is put back into *available_subnets* (and merged if possible).
* **generate_nodes_datamodel** - transform all the _**Vars**_ into node-specific data models in **nodes.yml**.
* **generate_node_config** - generates all the node specific config into **output/nodes.cfg**.

## Details

### Fabric
* **fabric** - describes how all the nodes are connected. A list of dictionaries, containing hostname and port for *right* and *left* node.
* **mpbgp** - multiprotocol bgp is used to exchange routes between PE nodes. A list of dictionaries, containing hostname, asn and ip for *right* and *left* node. 
* **services** - lists all available services. So far *VPNV4* is the only working choice.
* **ips_nodes** - lists all the provider nodes.
* **nodes** - lists all the nodes in the network. Each node is a dictionary, containing hostname, management IP address and loopback IP address.

### Services
* **VPNV4** - lists all the VPNs that should be configured. Each VPN contains the following:
    * **name** - name assigned to VPN
    * **rd** - route destinguisher
    * **ospfid** - OSPF router id used for devices in this VPN
    * **nodes** - all the nodes in the VPN. A dictionary, where the key is always the customer node, the values is always the provider nodes.

### Node specific
To simplify config generation, the *fabric* datamodel is transformed into *node*-specific datamodel. Some points in relation to that:
* All linknets are dynamically assigned. The *left* port gets the first available IP address in the assigned linknet subnet, the *right* the second.
* ASN and BGP information is only populated if you need it, ie PE nodes only.

### Config generation
All the node specific config snippets is written to one file, next step is to switch this out with creation of individual node config files in preparation for node provisioning.