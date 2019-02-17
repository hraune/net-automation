import datetime
from netaddr import IPSet

def uppercase_all(arg): 
    return arg.upper() 

def split_newlines(arg,index):
    return arg.split('\n')[index]

def timestamper(arg):
    return str('{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now()))+'_'+arg

def format_uptime(arg):
    return str(datetime.timedelta(seconds=arg))

def get_key(arg, i=0):
    return list(arg.keys())[i]

def get_keys(arg):
    return list(arg.keys())

def subtract_subnet(original_subnet, remove_subnets):
    """Subtract a list of subnets from original subnet and return leftover
    subnet(s) in a list"""
    original = IPSet([original_subnet])
    for subnet in remove_subnets:
        original.remove(subnet)
    
    return [str(subnet) for subnet in original.iter_cidrs()]

def is_in_tuplist(tuplist, value):
    """Checks if value is present in a list of tuples"""
    return len([tup for tup in tuplist if value in tup]) > 0

def nodes_not_in_fabric(nodes, provider_fabric, customer_fabric):
    """Returns nodes that are not defined in the fabric"""
    fabric = provider_fabric + customer_fabric

    #Unpacks the fabric and node dictionaries, keeping only the names
    nodes = [n['name'] for n in nodes]
    fabric = [node for f in fabric for node in [f['right'],f['left']]]
    
    return list(set(nodes) - set(fabric))

class FilterModule(object): 
    def filters(self): 
        return {
        'uppercase_all': uppercase_all,
        'split_newlines': split_newlines,
        'timestamper': timestamper,
        'format_uptime': format_uptime,
        'get_keys': get_keys,
        'get_key': get_key,
        'subtract_subnet': subtract_subnet,
        'is_in_tuplist': is_in_tuplist,
        'nodes_not_in_fabric': nodes_not_in_fabric,
        } 
