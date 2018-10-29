import datetime
import collections

def uppercase_all(arg): 
    return arg.upper() 


def split_newlines(arg,index):
    return arg.split('\n')[index]


def timestamper(arg):
    return str('{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now()))+'_'+arg


def balance_graph(arg):
    """ Takes a list of neighbor tuples and returns it 
    reverse-sorted based on neighbor occurences  """
    
    #Counts how many times each neighbor occurs
    count = collections.Counter([x for (x,y) in arg]+[y for (x,y) in arg])
    
    #Expand each neighbor tuple with a summary of its neighbor occurence counts    
    temp = [tup + (count[tup[0]]+count[tup[1]],) for tup in arg]

    #Reverse sort neighbor tuples based on neighbor count
    temp.sort(key=lambda item: item[2], reverse=True)

    #Return list of neighbor tuples without neighbor count
    return [(x,y) for (x,y,z) in temp]


class FilterModule(object): 
    def filters(self): 
        return {
        'uppercase_all': uppercase_all,
        'split_newlines': split_newlines,
        'timestamper': timestamper,
        'balance_graph': balance_graph,
        }
