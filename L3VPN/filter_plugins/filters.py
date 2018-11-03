# filters
from netaddr import IPSet

def uppercase_all(arg): 
    return arg.upper() 


def split_newlines(arg,index):
    return arg.split('\n')[index]


def subtract_subnet(original_subnet, remove_subnets):
    """Remove a list of subnets from original subnet and returns a
    list of new subnets sans those removed"""
    
    orinal = IPSet(original_subnet)
    for subnet in remove_subnets:
        orinal.remove(subnet)
    return [str(subnet) for subnet in orinal.iter_cidrs()]

class FilterModule(object): 
    def filters(self): 
        return {
        'uppercase_all': uppercase_all,
        'split_newlines': split_newlines,
        }
