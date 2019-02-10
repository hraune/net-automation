# Testing Scenarios

*1_VPNs* is the default scenario that has been used as the base throughout. All the other scenarios here are tweaks of that.

## 0 VPNs defined
No VPNs are defined in **service.yml**, two CE nodes is defined in **fabric.yml**.

### Expected result
blah

## 1 VPN defined
One VPN is defined in **service.yml**, one pair of CE nodes is defined in **fabric.yml**.

### Expected result
blah

## 2 VPNs
Two identical VPNs is defined in **service.yml**, two pairs of CE nodes is defined in **fabric.yml**.

### Expected results
blah

## 2 identical VPNs
Two identical VPNs is defined in **service.yml**, two pairs of CE nodes is defined in **fabric.yml**.

### Expected result
blah

## 1 VPN and incomplete fabric
One VPN is defined in **service.yml**, but only one CE node is defined in **fabric.yml**.

### Expected result
blah

## Interfaces not matching
One VPNs is defined in **service.yml**, two CE nodes is defined in **fabric.yml**. Interfaces used in *fabric* is not matching those defined in *hardware*.

### Expected result
blah

## No CE nodes
One VPN is defined in **service.yml**, no CE nodes is defined in **fabric.yml**.

### Expected result
blah

## No fabric IP addresses defined
One VPNs is defined in **service.yml**, two CE nodes is defined in **fabric.yml**. No fabric IP addresses is defined for CE nodes.

### Expected result
blah

## No hardware defined in fabric
One VPN is defined in **service.yml**, two CE nodes is defined in **fabric.yml**. Hardware is not defined in **fabric.yml**.

### Expected result
blah

## Not all provider nodes defined in fabric
One VPN is defined in **service.yml**, two  CE nodes is defined in **fabric.yml**. Not all ISP nodes is not defined in **fabric.yml**

### Expected result
blah

## Interfaces reused in fabric
One VPN is defined in **service.yml**, two CE nodes is defined in **fabric.yml**. The same interface is duplicated and reused in the *fabric*

### Expected result
blah