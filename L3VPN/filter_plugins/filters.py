# filters
from netaddr import IPSet

def subtract_subnet(original_subnet, remove_subnets):
    """Subtract a list of subnets from original subnet and return leftover
    subnet(s) in a list"""
    orinal = IPSet([original_subnet])
    for subnet in remove_subnets:
        orinal.remove(subnet)
    return [str(subnet) for subnet in orinal.iter_cidrs()]

def is_in_tuplist(tuplist, value):
    """Checks if value is present in a list of tuples"""
    return len([tup for tup in tuplist if value in tup]) > 0

class FilterModule(object): 
    def filters(self): 
        return {
        'subtract_subnet': subtract_subnet,
        'is_in_tuplist': is_in_tuplist,
        }
