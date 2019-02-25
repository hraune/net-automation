# L3VPN on Cisco IOS-XE
These playbooks will generate relevant config (interface, routing and vrf) for running L3VPN over Cisco IOS-XE devices, deploy config on devices and finally validate deployment.

## Overview
The variable files and ansible playbooks used for provisioning of L3VPN:

### Vars
* **fabric.yml** - contains a data model that describes how all devices is connected and how the infrastructure should be configured.
* **services.yml** - describes how the services (in this case L3VPN) should be configured.
* **ip_addresses.yml** - contains all the subnets that is available for generating linknets.

### Playbooks
* **assign_ip_addresses.yml** - generates *fabric_linknets* from the *available_subnets*. The number of linknets generated is based on the number of links from *fabric*. 
Depending on the number of linknets in *fabric linknets*, it will add or subtract linknets to get the correct number of linknets. Unneeded linknets is put back into *available_subnets* (and merged into the existing subnets if possible).
* **create_node_datamodel.yml** - transform all the _**Vars**_ into node-specific data models in **nodes.yml**. Will also populate the **hosts** file for future playbooks; current playbooks is localhost only.
* **validate_input.yml** - validates all the vars for completeness.
* **pre_validate.yml** - checks all devices for any existing VPN configurations, outputs results into **existing_vrf.yml**.
* **generate_config.yml** - generates network and service config into **configs/<hostname>/**. Validation file for napalm_validate is also created for each node.
* **deploy_config.yml** - deploys network and service config and validates deployment.

## Details

### Fabric
* **hardware** - describes the properties of the hardware used; number and names of ports as well as common management interface.
* **fabric** - describes how all the nodes are connected. A list of dictionaries, containing hostname and port for *right* and *left* node. Split into an infrastructure and a customer specific list.
* **mpbgp** - multiprotocol bgp is used to exchange routes between PE nodes. A list of dictionaries, containing ASN neighbor pairings. 
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
* All linknets are dynamically assigned. The *left* port gets the first available IP address in the assigned linknet subnet, the *right* port the second.
* Interface description is generated on the format "To < hostname on the other end >;< interface on the other end >".
* ASN and BGP information is only populated if you need it, ie PE nodes only.
* Will use route distinguisher for route target export/import.

### Input validation
This playbook will validate that all the vars in **fabric.yml**, **services.yml** and **ip-addresses.yml** are complete; all fields have a value and that all values are legal.

### Pre-validation
Checks nodes in the network for any current VPNs already configured. Unknown VPNs will get variable **surprise** set to *false*, while knwon (ie. defined in the service description) will get *True*.

### Config generation
Each node gets a directory under **output** which config is generated into. In all there is up to three configs generated (dependent on role of device):
  * *basic.cfg* - barebone config with only management
  * *running.cfg* - contains all infrastructure config (linknets, routing etc).
  * *service.cfg* - service specific config.

There is two options (in the hosts file) to control how to react to existing VRFs:
* **ignore_surprise** - if this option is set to *false*, any unknown VPNs will be removed; service.cfg will contain config to remove VPNs.
*  **overwrite_existing** - if set to *true*, service.cfg will contain config that overwrites the existing VPN, if set to *false* it will skip that VPN.

### Config deployment
The network config is deployed with the **ios_config** module in Ansible, service config is deployed with **napalm_install_config**.

### Config validation
During config generation, a validation file for **napalm_validate** is also generated. It checks that all interfaces is configured with the correct IP, that BGP is running correctly, and that all devices in a VPN can ping each other. A report is finally generated in the configs device specific directory.

### Logging
When the var logging is set to *True* it will log the output of the following actions; all config deployment via the **ios_config** module, all validations done by the **napalm_validate** module. All this logging will be stored in the logging directory.