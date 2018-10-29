import datetime
import collections

def uppercase_all(arg): 
    return arg.upper() 


def split_newlines(arg,index):
    return arg.split('\n')[index]


def timestamper(arg):
    return str('{:%Y%m%d-%H%M%S}'.format(datetime.datetime.now()))+'_'+arg


def balance_graph(graph):
    """ Takes a list of neighbor tuples and returns it 
    reverse-sorted based on neighbor occurences  """
    
    # Counts how many times each neighbor occurs
    count = collections.Counter([x for (x,y) in graph]+[y for (x,y) in graph])

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
        count = collections.Counter([x for (x,y) in value]+[y for (x,y) in value])
        for tup in value:
            if count[tup[1]] > count[tup[0]]:
                reordered.append((tup[1],tup[0],key))
            else:
                reordered.append(tup+(key,))

    # Reverse sort neighbor tuples based on neighbor count
    reordered.sort(key=lambda item: item[2], reverse=True)

    # Return list of neighbor tuples without neighbor count
    return [(x,y) for (x,y,z) in reordered]


class FilterModule(object): 
    def filters(self): 
        return {
        'uppercase_all': uppercase_all,
        'split_newlines': split_newlines,
        'timestamper': timestamper,
        'balance_graph': balance_graph,
        }
