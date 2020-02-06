import goody
import prompt
from collections import defaultdict


def read_graph(file : open) -> {str:{str}}:
    dictionary = defaultdict(set)
    for _,dictitems in enumerate(file):
        dictitems = tuple(dictitems.rstrip().split(';'))
        dictionary[dictitems[0]].add(dictitems[1])
    return(dict(dictionary))

def graph_as_str(graph : {str:{str}}) -> str:
    return "".join([f"  {k} -> {sorted(v)}\n" for k, v in sorted(graph.items())])
    
def reachable(graph : {str:{str}}, start : str, trace : bool = False) -> {str}:
    reached_set, exploring_list = set(), [start]
    while len(exploring_list) != 0:
        if trace == True: 
            print(f"reached set    = {reached_set}\n"
                  f"exploring list = {exploring_list}")
        if graph.get(exploring_list[0]):
            for node in graph.get(exploring_list[0]):
                if node not in reached_set:
                    exploring_list.append(node)
        x = exploring_list.pop(0)
        reached_set.add(x)
        if trace == True:
            print(f"removing node {x} from the exploring list; adding it to reached list\n"
                  f"after adding all nodes reachable directly from a but not already in reached, exploring = {exploring_list}\n")
    return reached_set


if __name__ == '__main__':
    # Write script here
    graph = read_graph(goody.safe_open('Enter the file name describing this graph','r','Illegal file name'))
    print(f'\nGraph: a node -> [showing all its destination nodes]\n{graph_as_str(graph)}')
    while True: 
        start = prompt.for_string('\nEnter the starting node (or enter quit)', is_legal=(lambda x : x in graph.keys() or x == 'quit'), error_message='Illegal: not a source node')
        if start == 'quit':
            break
        trace = input('Enter whether to trace this algorithm[True]: ')
        destinations = reachable(graph, start, True if trace == 'True' else False)
        print(f'From node {start} its reachable nodes:  {destinations}')
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc1.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()