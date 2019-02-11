# Testing Scenarios

*1_VPNs* is the default scenario that has been used as the base throughout. All the other scenarios here are tweaks of that.

## 0 VPNs defined
No VPNs are defined in **service.yml**, two CE nodes is defined in **fabric.yml**.

### Expected result
Empty list of VPNs for each provider node, no VRF defined on interfaces toward CEs. Basically pure IPv4 service.

## 1 VPN defined
One VPN is defined in **service.yml**, one pair of CE nodes is defined in **fabric.yml**.

### Expected result
Working 1 VPN node.yml file generated

## 2 VPNs
Two identical VPNs is defined in **service.yml**, two pairs of CE nodes is defined in **fabric.yml**.

### Expected results
Working 2 VPN node.yml file generated.

## 2 identical VPNs
Two identical VPNs is defined in **service.yml**, two pairs of CE nodes is defined in **fabric.yml**.

### Expected result
As if only *one* VPN is defined (ignore duplicates). Should give a warning.

## 1 VPN and incomplete fabric
One VPN is defined in **service.yml**, but only one CE node is defined in **fabric.yml**.

### Expected result
Generates node.yml file with only one CE node and respective ports in shutdown on the *left-out* PE node. Should give a warning.

## Interfaces not matching
One VPNs is defined in **service.yml**, two CE nodes is defined in **fabric.yml**. Interfaces used in *fabric* is not matching those defined in *hardware*.

### Expected result
If interfaces is in use multiple places, prioritise Provider nodes. Should give a warning.

## No CE nodes
One VPN is defined in **service.yml**, no CE nodes is defined in **fabric.yml**.

### Expected result
Should give a nodes.yml file with only Provider nodes. This is state before any CE nodes are provisioned.

## No fabric IP addresses defined
One VPNs is defined in **service.yml**, two CE nodes is defined in **fabric.yml**. No fabric IP addresses is defined for CE nodes.

### Expected result
Gives a node.yml file with all relevant interfaces in shutdown. Should give a warning.

## No hardware defined in fabric
One VPN is defined in **service.yml**, two CE nodes is defined in **fabric.yml**. Hardware is not defined in **fabric.yml**.

### Expected result
Should give a nodes.yml file without any management nodes, nor unused interfaces. Should give a warning.

## Not all provider nodes defined in fabric
One VPN is defined in **service.yml**, two  CE nodes is defined in **fabric.yml**. Not all ISP nodes is not defined in **fabric.yml**

### Expected result
Gives a node.yml file nodes missing provider information; no BGP and no VPNs is defined on these nodes. Should give a warning.