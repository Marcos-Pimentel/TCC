import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import json
from os import walk
import networkx.algorithms.euler as euler
from itertools import combinations
import sys
import matplotlib.pyplot as plt

#in the output files, there is no weight on the edges, so it is needed to also use the input files to get these values

test_config_name = "tests_020_005"
out_path = test_config_name+"/output/"
in_path = "Instances/"
table_path = "Tables/"+test_config_name+'/'


def eulerize(G):
    """Transforms a graph into an Eulerian graph.

    If `G` is Eulerian the result is `G` as a MultiGraph, otherwise the result is a smallest
    (in terms of the number of edges) multigraph whose underlying simple graph is `G`.

    Parameters
    ----------
    G : NetworkX graph
       An undirected graph

    Returns
    -------
    G : NetworkX multigraph

    Raises
    ------
    NetworkXError
       If the graph is not connected.

    See Also
    --------
    is_eulerian
    eulerian_circuit

    References
    ----------
    .. [1] J. Edmonds, E. L. Johnson.
       Matching, Euler tours and the Chinese postman.
       Mathematical programming, Volume 5, Issue 1 (1973), 111-114.
    .. [2] https://en.wikipedia.org/wiki/Eulerian_path
    .. [3] http://web.math.princeton.edu/math_alive/5/Notes1.pdf

    Examples
    --------
        >>> G = nx.complete_graph(10)
        >>> H = nx.eulerize(G)
        >>> nx.is_eulerian(H)
        True

    """
    if G.order() == 0:
        raise nx.NetworkXPointlessConcept("Cannot Eulerize null graph")
    if not nx.is_connected(G):
        raise nx.NetworkXError("G is not connected")
    odd_degree_nodes = [n for n, d in G.degree() if d % 2 == 1]
    G = nx.MultiGraph(G)
    if len(odd_degree_nodes) == 0:
        return G
    
    # get all shortest paths between vertices of odd degree
    odd_deg_pairs_paths = [
        (m, {n: nx.shortest_path(G, source=m, target=n, weight='weight')})
        for m, n in combinations(odd_degree_nodes, 2)
    ]

    # use the number of vertices in a graph + 1 as an upper bound on
    # the maximum length of a path in G
    upper_bound_on_max_path_length = len(G) + 1

    # use "len(G) + 1 - len(P)",
    # where P is a shortest path between vertices n and m,
    # as edge-weights in a new graph
    # store the paths in the graph for easy indexing later
    Gp = nx.Graph()
    for n, Ps in odd_deg_pairs_paths:
        for m, P in Ps.items():
            if n != m:
                dist = 0
                for i in range(len(P)-1):
                    dist += G.edges[P[i],P[i+1],0]['weight']
                
                Gp.add_edge(
                    m, n, weight=dist, path=P
                )

    # find the minimum weight matching of edges in the weighted graph
    best_matching = nx.Graph(list(nx.max_weight_matching(Gp)))

    # duplicate each edge along each path in the set of paths in Gp
    for m, n in best_matching.edges():
        path = Gp[m][n]["path"]
        G.add_edges_from(nx.utils.pairwise(path))
        for e in G.edges:
            if e[2] != 0:
                G.edges[e]['weight'] = G.edges[e[0], e[1], 0]['weight']
    return G

def total_weight(G):
    weight = 0
    for e in G.edges:
        weight += G.edges[e]['weight']
    return weight

def read_input(file):
    content = None
    with open(file, "r") as arq:
        content = json.load(arq)
    return content

files = next(walk(out_path), (None, None, []))[2]

dict_list = dict()

dict_list['Lpr-a-01-2C'] = list()
dict_list['Lpr-a-01-3C'] = list()
dict_list['Lpr-a-02-2C'] = list()
dict_list['Lpr-a-03-2C'] = list()
dict_list['Lpr-a-03-3C'] = list()
dict_list['Lpr-a-03-4C'] = list()
dict_list['Lpr-a-03-5C'] = list()
dict_list['Lpr-a-04-4C'] = list()
dict_list['Lpr-a-04-5C'] = list()
dict_list['Lpr-a-05-4C'] = list()
dict_list['Lpr-b-01-2C'] = list()
dict_list['Lpr-b-01-3C'] = list()
dict_list['Lpr-b-02-2C'] = list()
dict_list['Lpr-b-03-4C'] = list()
dict_list['Lpr-b-04-4C'] = list()
dict_list['Lpr-b-05-6C'] = list()

for file in files:
    
    in_file_path = in_path+file
    out_file_path = out_path+file
    
    in_content = read_input(in_file_path)
    out_content = read_input(out_file_path)
    
    solution_info = out_content['SolutionInfo']
    
    if solution_info['Status'] == 2:
        time = solution_info['Runtime']
    else:
        time = 3600
    
    deadhead = 1e+100
    gap = solution_info['MIPGap']
    objective = solution_info['ObjVal']
    
    file_name_breakdown = file.split('-')
    table_name = file_name_breakdown[0]+'-'+file_name_breakdown[1]+'-'+file_name_breakdown[2]+'-'+file_name_breakdown[3]
    
    
    if objective != 1e+100:
        out_vars = out_content['Vars']
        
        #create the graph for each district
        
        deadhead = 0
        gained_imparity = 0
        imparity_quotient = 0
        demand_disparity = 0
        total_demand = 0
        depots_demand = list()
        
        for d in in_content['DEPOTS']:
            demand = 0
            G = nx.Graph()
            aux_list = list()
            for i in out_vars:
                if 'DepotEdgeAssign['+str(d)+',' in i['VarName'] and i['X'] >= 0.9:
                    edge = i['VarName'].split('(')[1].split(')')[0].split(', ')
                    edge_name = '(' + edge[0] + ',' + edge[1] + ')'
                    dist = in_content['EDGES'][edge_name]['DISTANCE']
                    G.add_edge(edge[0], edge[1], weight=dist)
                    demand += float(in_content['EDGES'][edge_name]['DEMAND'])
            
            depots_demand.append(demand)
            total_demand += demand
            
            if not euler.is_eulerian(G):
                try:
                    G1 = eulerize(G)
                except nx.exception.NetworkXError:
                    nx.draw(G, with_labels=True)
                    plt.savefig(f'error_{file}_{d}.PNG')
                    sys.exit()
                deadhead += total_weight(G1)-total_weight(G)
            
        
        
        
        for i in out_vars:
            if 'LooseParity' in i['VarName']:
                gained_imparity += 1
        
        vertices = list()
        for i in in_content['EDGES']:
            aux = i.split('(')[1].split(',')[0]
            if aux not in vertices:
                vertices.append(aux)
        
        imparity_quotient = gained_imparity/len(vertices)
        
        time = round(time,4)
        gained_imparity = round(gained_imparity,4)
        imparity_quotient = round(imparity_quotient,4)
        objective = round(objective,4)
        gap = round(gap,4)
        
        dict_list[table_name].append({'Instance':file, 'Time':time, 'Gap':gap, 'Objective':objective, 'Gained Imparity':gained_imparity, 'Imparity Quotient':imparity_quotient, 'Deadhead':deadhead})
        
        avg_demand = total_demand/len(depots_demand)
        
        for i in depots_demand:
            if avg_demand - i > demand_disparity:
                demand_disparity = avg_demand - i
            elif i - avg_demand > demand_disparity:
                demand_disparity = i - avg_demand
        
        # if file == 'Lpr-a-01-3C-7B.json':
        #     print(100*demand_disparity/avg_demand)
        
        #calculate the deadhead value
        #create the pandas table with the values
        
        #fields of the table:
        #Number of integer variables (NIV)
        #Time
        #solver Gap
        #Objective Value
        #Gained Imparity
        #Imparity Quotient
        #Deadhead
        
for i in dict_list:
    df = pd.DataFrame(dict_list[i])
    df.to_csv(table_path+i+".csv", index=False)
# df = pd.DataFrame(dict_list)
# df.to_csv(test_config_name+".csv",index=False)