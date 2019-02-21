import datetime
import collections
from math import ceil
from netaddr import IPSet
import ipaddress

def uppercase_all(arg):
    '''Returns arg in upper case'''
    return arg.upper() 

def split_newlines(arg, index):
    '''Based on index, returns a given line of arg'''
    return arg.split('\n')[index]

def timestamper(arg):
    '''Returns a timestamp'''
    return str('{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now()))+'_'+arg

def format_uptime(arg):
    '''Returns arg number of seconds as seconds, minutes, hours, days'''
    return str(datetime.timedelta(seconds=arg))

def get_key(arg, i=0):
    '''Returns a given key of a dict'''
    return list(arg.keys())[i]

def get_keys(arg):
    '''Returns all the keys of a dict'''
    return list(arg.keys())

def balance_graph(graph):
    """ Takes a list of neighbor tuples and returns it 
    reverse-sorted based on neighbor occurences  """
    
    # Counts how many times each neighbor occurs
    count = collections.Counter([x for (x,y) in graph]
                                    + [y for (x,y) in graph])

    # Group neighbors based on neighbor occurence count
    neigh_count = {}
    for tup in graph:
        total = count[tup[0]]+count[tup[1]]
        if total in neigh_count:
            neigh_count[total].append(tup)
        else:
            neigh_count[total] = [tup]

    # Within tuples with same neighbor count, reorder tuples so 
    # that the most occuring neighbor is first
    reordered = []
    for key in neigh_count:
        value = neigh_count[key]
        count = collections.Counter([x for (x,y) in value]
                                        + [y for (x,y) in value])
        for tup in value:
            if count[tup[1]] > count[tup[0]]:
                reordered.append((tup[1],tup[0],key))
            else:
                reordered.append(tup+(key,))

    # Reverse sort neighbor tuples based on neighbor count
    reordered.sort(key=lambda item: item[2], reverse=True)

    # Return list of neighbor tuples without neighbor count
    return [(x,y) for (x,y,z) in reordered]

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

    # Unpacks the fabric and node dictionaries, keeping only the names
    nodes = [n['name'] for n in nodes]
    fabric = [node for f in fabric for node in [f['right'],f['left']]]
    
    # Returns the list of fabric names subtracted from the list of all nodes
    return list(set(nodes) - set(fabric))

def unique_list(arg):
    '''Returns a list containing only unique elements, order is 
    not preserved!'''
    return list(set(arg))

def fabric_dict_to_tuples(arg):
    '''Converts a list of dictionaries into a list of tuples'''
    ret = ([(item['right'],item['right_port']) for item in arg ] 
            + [(item['left'],item['left_port']) for item in arg ])
    return ret

def get_all_node_names(arg):
    '''Returns a list of all the node names'''
    return [node['name'] for node in arg]

def get_all_fabric_names(arg):
    '''Returns a list of all the node names in a fabric dictionary'''
    return [node for item in arg for node in [item['right'],item['left']]]

def subtract_list(x,y):
    '''Subtracts all elements in y from x and returns it as a list'''
    return list(set(x)-set(y))

def merge_lists_from_list_of_dict(arg,dict_key):
    '''Given a list of dictionaries with the same keys, returns a merged list
    of all the lists for a given key'''
    return [i for item in arg for i in item[dict_key]]

def count_unique_entries_in_list_of_dicts(arg):
    '''Counts unique entries in a list of dictionaries'''
    ret = list({item['name']:item for item in arg}.values())
    return len(ret)

def nodes_is_fully_defined(arg):
    '''Verifies that each node in a list of nodes has a name, mgmt IP 
    and loopback IP'''
    for node in arg:
        if not ('name' in node and node['name'] != ''):
            return False
        if not ('mgmt' in node and node['mgmt'] != ''):
            return False
        if not ('loopback' in node and node['loopback'] != ''):
            return False
    return True

def bgp_is_fully_defined(arg):
    '''Verifies that all bgp entries are valid; the AS Number is valid and that
    each neighbor pair contains 2 routers'''
    for bgp in arg:
        if not ('asn' in bgp and 1 < bgp['asn'] < 4294967294):
            return False
        for neighbor in bgp['neighbors']:
            if not ('left' in neighbor and neighbor['left'] != ''):
                return False
            if not ('right' in neighbor and neighbor['right'] != ''):
                return False
    return True

def hardware_is_fully_defined(arg):
    '''Verifies that all hardware entries are valid; name is present, a 
    management address is defined and is using an interface present in the 
    hardware, a list of all possible interfaces is defined and that there is 
    devices assigned to the hardware.'''
    for hardware in arg:
        if not ('name' in hardware and hardware['name'] != ''):
            return False
        if not ('mgmt_int' in hardware and hardware['mgmt_int'] != ''):
            return False
        if not ('interface' in hardware and len(hardware['interfaces']) > 0):
            return False
        if not ('devices' in hardware and len(hardware['devices']) > 0):
            return False
        if hardware['mgmt_int'] not in hardware['interfaces']:
            return False
    return True

def fabric_is_fully_defined(arg, hw):
    '''Verifies that a fabric is valid; left node and its left_port is defined,
    right node and its right_port is defined and that all ports are interfaces
    defined in the hardware.'''
    all_intfs = [intf for intf_list in hw for intf in intf_list['interfaces']]
    for fabric in arg:
        if not ('left' in fabric and fabric['left'] != ''):
            return False
        if not ('left_port' in fabric and fabric['left_port'] != '' 
                    and fabric['left_port'] in all_intfs):
            return False
        if not ('right' in fabric and fabric['right'] != ''):
            return False                    
        if not ('right_port' in fabric and fabric['right_port'] != '' 
                    and fabric['right_port'] in all_intfs):
            return False
    return True

def proper_linknets(arg):
    '''Verifies that a list of linknets are all proper IP network addresses'''
    for linknet in arg:
        try:
            network_addr = ipaddress.ip_network(linknet)
        except ValueError:
            return False
    return True

def proper_ip_address(arg):
    '''Verifies that a given IP is a proper IP address'''
    try:
        ip_addr = ipaddress.ip_address(arg)
    except ValueError:
        return False
    return True

def check_route_distinguisher(arg):
    '''Checks if a given arg is a valid route distinguisher(RD). A valid RD is
    6 bytes; (2byte ASN):(4byte any value) or (4byte IP):(2byte any value)'''
    if ':' in arg and len(arg.split(':')) == 2:
        front,back = arg.split(':')
        if proper_ip_address(front) and ceil(int(back).bit_length()/8.0) <= 2:
            return True
        elif (not proper_ip_address(front) 
                and ceil(int(front).bit_length()/8) <= 2 
                and ceil(int(back).bit_length()/8) <= 4):
            return True
        else:
            return False
    return False
    
def vpnv4_is_fully_defined(arg):
    '''Verifies that a list vpnv4 services is valid; valid route distinguisher,
    ospf ID, list of nodes and a state'''
    for vpn in arg:
        if not  (vpn['name'] != '' and len(vpn['name'] <= 32)):
            return False
        if not (check_route_distinguisher(vpn['rd'])):
            return False
        if not (1 <= vpn['ospfid'] <= 65535):
            return False
        if not (isinstance(vpn['nodes'], dict) and len(vpn['nodes']) >= 2):
            return False
        if vpn['state'] == '':
            return False
    return True

class FilterModule(object): 
    def filters(self): 
        return {
        'uppercase_all': uppercase_all,
        'split_newlines': split_newlines,
        'timestamper': timestamper,
        'format_uptime': format_uptime,
        'get_keys': get_keys,
        'balance_graph':balance_graph,
        'get_key': get_key,
        'subtract_subnet': subtract_subnet,
        'is_in_tuplist': is_in_tuplist,
        'nodes_not_in_fabric': nodes_not_in_fabric,
        'unique_list':unique_list,
        'fabric_dict_to_tuples':fabric_dict_to_tuples,
        'get_all_node_names':get_all_node_names,
        'get_all_fabric_names':get_all_fabric_names,
        'subtract_list':subtract_list,
        'merge_lists_from_list_of_dict':merge_lists_from_list_of_dict,
        'unique_entries_in_list_of_dicts':unique_entries_in_list_of_dicts,
        'nodes_is_fully_defined':nodes_is_fully_defined,
        'bgp_is_fully_defined':bgp_is_fully_defined,
        'hardware_is_fully_defined':hardware_is_fully_defined,
        'fabric_is_fully_defined':fabric_is_fully_defined,
        'proper_linknets':proper_linknets,
        'proper_ip_address':proper_ip_address,
        'check_route_distinguisher':check_route_distinguisher,
        'vpnv4_is_fully_defined':vpnv4_is_fully_defined,
        } 

