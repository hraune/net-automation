# filters

def uppercase_all(arg): 
    return arg.upper() 


def split_newlines(arg,index):
    return arg.split('\n')[index]


class FilterModule(object): 
    def filters(self): 
        return {
        'uppercase_all': uppercase_all,
        'split_newlines': split_newlines,
        }
