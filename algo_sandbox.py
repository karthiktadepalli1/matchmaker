"""
design of an agent for an assignment market -
- like the teacher class in ech
- has an ID, a preference set over the items, a (possible) item of ownership

design of an item in an assignment market to be compatible with the given agent class
- has a name


REDESIGN

"""
import numpy as np
import pulp as plp

# def serialdict(agents, items, ordering = None):
#     # normalize so that |agents| = |items| beforehand
#     assignment = {}
#     orderedAgents = np.random.permutation(agents)
#     if ordering is not None:
#         orderedAgents = ordering
#     for agent in orderedAgents:
#         available = [i for i in agent.prefs if i in items]
#         assignment[agent] = available[0]
#         items.remove(available[0])
#     return assignment
#
# def rand(agents, items):
#     np.random.shuffle(agents)
#     np.random.shuffle(items)
#     assignment = dict(zip(agents, items))
#     return assignment
#
# def rv(agents, items, rv):


# this is all designed with graph Inputs

def pre_bipartite(G):
    # preprocess to ensure |students| = |schools|
    all = G.nodes()
    students = [n for n in all if n['bipartite'] = 0]
    schools = [n for n in all if n['bipartite'] = 1]
    dummyRanks = [n+1 for i in range(n)]
    if len(students) < len(schools):
        m, n = len(students), len(schools)
        dummyData = dict(zip(schools, dummyRanks))
        type = 0
    elif len(students) > len(schools):
        m, n = len(schools), len(students)
        dummyData = dict(zip(students, dummyRanks))
        type = 1
    else:
        return G
    for i in range(1, n-m+1):
        name = 'dummy' + str(i)
        G.add_node(name, bipartite = type, ranking = dummyDate)
        # G.node[name]['bipartite'] = type
        # G.node[name]['ranking'] = dummyData
    return G

def serialdictG(G, ordering = None):
    agents = G.nodes()
    if ordering is not None:
        agents = ordering
    matchG = nx.Graph()
    for agent in agents:
        # ensure agent isn't a dummy agent
        if 'dummy' in agent:
            agents.append(agent)
            continue
        # filter objects that have been assigned already
        itemsLeft = G.neighbors(agent)
        ranks = agent['ranking']
        for k in ranks.keys():
            if k not in itemsLeft:
                ranks.pop(k, None)
        # determine preferred object
        best = ranks.values().min()
        for item, rank in ranks.items():
            if rank == best:
                # create an assignment, remove from graph
                matchG.add_edge(agent, item)
                G.remove_node(item)
                G.remove_node(agent)
    return matchG

def randG(G):
    agents = G.nodes()
    matchG = nx.Graph()
    for agent in agents:
        nbrs = G.neighbors(agent)
        chosen = np.random.choice(nbrs)
        matchG.add_edge(agent, chosen)
        G.remove(agent)
        G.remove(chosen)
    return matchG

def galeShapleyG(G):
    all = G.nodes()
    students = [n for n in all if n['bipartite'] = 0]
    schools = [n for n in all if n['bipartite'] = 1]
    matches = []
    n = min(len(students), len(schools))
    while len(matches) < n:
        for 
