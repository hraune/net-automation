# L3VPN on Cisco IOS-XE
These playbooks will generate relevant config (interface, routing and vrf) for running L3VPN over Cisco IOS-XE devices.

## Overview
The variable files and ansible playbooks used for provisioning of L3VPN:

### Vars
* **fabric.yml** - contains a data model that describes how all devices is connected and how the infrastructure should be configured.
* **services.yml** - describes how the services (in this case L3VPN) should be configured.
* **ip_addresses.yml** - contains all the subnets that is available for generating linknets.

### Playbooks
* **assign_ip_addresses.yml** - generates *fabric_linknets* from the *available_subnets*. The number of linknets generated is based on the number of links from *fabric*. 
Depending on the number of linknets in *fabric linknets*, it will add or subtract linknets to get the correct number of linknets. Unneeded linknets is put back into *available_subnets* (and merged into the existing subnets if possible).
* **generate_nodes_datamodel.yml** - transform all the _**Vars**_ into node-specific data models in **nodes.yml**. Will also populate the **hosts** file for future playbooks; current playbooks is localhost only.
* **pre_validate.yml** - checks all devices for any existing VPN configurations, outputs results into **existing_vrf.yml**.
* **generate_config.yml** - generates network and service config into **configs/<hostname>/**. Validation file for napalm_validate is also created for each node.
* **deploy_config.yml** - deploys network and service config and validates deployment.

## Details

### Fabric
* **fabric** - describes how all the nodes are connected. A list of dictionaries, containing hostname and port for *right* and *left* node.
* **mpbgp** - multiprotocol bgp is used to exchange routes between PE nodes. A list of dictionaries, containing hostname, asn and ip for *right* and *left* node. 
* **services** - lists all available services. So far *VPNV4* is the only working choice.
* **isp_nodes** - lists all the provider nodes.
* **nodes** - lists all the nodes in the network. Each node is a dictionary, containing hostname, management IP address and loopback IP address.

### Services
* **VPNV4** - lists all the VPNs that should be configured. Each VPN is a dictionary containing:
    * **name** - name assigned to VPN.
    * **rd** - route distinguisher.
    * **ospfid** - OSPF router id used for devices within this VPN
    * **nodes** - all the nodes in the VPN. A dictionary, where the key is always the customer node, the values is always the provider node it is connected to.
    * **state** - If set to 'absent', VPN will be removed on next run.

### Node specific
To simplify config generation, the *fabric* datamodel is transformed into *node*-specific datamodel.
* All linknets are dynamically assigned. The *left* port gets the first available IP address in the assigned linknet subnet, the *right* the second.
* ASN and BGP information is only populated if you need it, ie PE nodes only.
* Will use route distinguisher for route target export/import.

### Pre-validation
Before any config is generated, the network is checked for any current VPNs already configured. Any unknown VPNs is tagged as such.

### Config generation
Each node gets a directory under **output** which config is generated into. In all there is up to three configs generated (dependent on role of device):
  * basic.cfg - barebone config with only management
  * running.cfg - network config (linknets, routing etc).
  * service.cfg - service specific config.

If the **ignore_surprise** option is set to false, any unknown VPNs will be removed. 
If there is any existing VPNs configured that are similar to those in services.yml, the **overwrite_existing** will if set to true generate config that overwrites, or if set to false skip that VPN.

### Config deployment
The network config is deployed with the **ios_config** module in Ansible, service config is deployed with **napalm_install_config**.

### Config validation
During config generation, a validation file for **napalm_validate** is also generated. It checks that all interfaces is configured with the correct IP, that BGP is running correctly, and that all devices in a VPN can ping each other.