import datetime

def uppercase_all(arg): 
    return arg.upper() 

def split_newlines(arg,index):
    return arg.split('\n')[index]

def timestamper(arg):
    return str('{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now()))+'_'+arg

def get_key(arg, i=0):
    return list(arg.keys())[i]

def get_keys(arg):
    return list(arg.keys())

class FilterModule(object): 
    def filters(self): 
        return {
        'uppercase_all': uppercase_all,
        'split_newlines': split_newlines,
        'timestamper': timestamper
        'get_keys': get_keys
        'get_key': get_key
        } 
