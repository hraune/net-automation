# filters
from netaddr import IPSet

def subtract_subnet(original_subnet, remove_subnets):
    """Remove a list of subnets from original subnet and returns a
    list of new subnets sans those removed"""
    print(original_subnet, remove_subnets)
    orinal = IPSet([original_subnet])
    for subnet in remove_subnets:
        orinal.remove(subnet)
    return [str(subnet) for subnet in orinal.iter_cidrs()]

class FilterModule(object): 
    def filters(self): 
        return {
        'subtract_subnet': subtract_subnet,
        }
