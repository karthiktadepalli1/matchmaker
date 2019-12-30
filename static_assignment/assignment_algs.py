import numpy as np
import pulp
from copy import deepcopy
import networkx as nx
from networkx.algorithms import bipartite
from networkx.algorithms.cycles import find_cycle
from networkx.algorithms.matching import max_weight_matching
from matchmaker.helpers import listify_rankings

def serialDictatorship(Gph, ordering = None):
    G = deepcopy(Gph)
    agents = [(agent, data) for agent, data in G.nodes.items() if data['bipartite'] == 1]
    items = [(item, data) for item, data in G.nodes.items() if data['bipartite'] == 0]
    np.random.shuffle(agents)
    if ordering is not None:
        agents = ordering
    matchG = nx.Graph()
    matchG.add_nodes_from(G)
    for agent in agents:
        # remove already assigned objects
        itemsLeft = G.neighbors(agent)
        ranks = listify_rankings(agent['ranking'])
        for k in ranks:
            if k not in itemsLeft:
                ranks.remove(k)
        # match to preferred object
        if len(ranks) > 0:
            matchG.add_edge(agent, ranks[0])
            G.remove_node(ranks[0])
        # else unassigned
    return matchG

def randomAssignment(Gph):
    G = deepcopy(Gph)
    agents = [(agent, data) for agent, data in G.nodes.items() if data['bipartite'] == 1]
    items = [(item, data) for item, data in G.nodes.items() if data['bipartite'] == 0]
    matchG = nx.Graph()
    matchG.add_nodes_from(G)
    n = min(len(agents), len(items))
    for i in range(n):
        agent = agents[i]
        nbrs = G.neighbors(agent)
        chosen = np.random.choice(nbrs)
        matchG.add_edge(agent, chosen)
        G.remove(agent)
        G.remove(chosen)
    return matchG

def TTC(Gph, initial):
    """
    Implements TTC given an initial ownership of houses.
    initial: a dictionary with agent:house pairs.
    """
    # map each house to the agent who initially owns it
    house_agent_dict = {v:k for k, v in initial.items()}
    # create manipulable copy of the matching graph
    G = deepcopy(Gph)
    nx.set_node_attributes(G, None, 'match')
    # create directed graph on which the TTC algorithm runs
    ttcGraph = nx.DiGraph()
    agents = [(agent, data) for agent, data in G.nodes.items() if data['bipartite'] == 1]
    ttcGraph.add_nodes_from(agents)
    # rankings must be a sorted list for TTC - preprocess to achieve that
    for n, d in ttcGraph.nodes(data=True):
        d['ranking'] = listify_rankings(d['rankings'])
    # run TTC
    while list(ttcGraph.nodes()) != []:
        # create ranking of available houses
        for n, d in ttcGraph.nodes(data=True):
            d['ranking'] = [i for i in d['ranking'] if house_agent_dict[i] in ttcGraph.nodes()]
        # create pointers from agents to the agent who owns the house they like most
        pointers = [(n, house_agent_dict(d['ranking'][0])) for n, d in all]
        for start, end in pointers:
            ttcGraph.add_edge(start, end)
        try:
            while True:
                cycle = find_cycle(ttcGraph)
                for start, end in cycle:
                    # create record of match to house
                    G.node[start]['match'] = initial[end]
                    ttcGraph.remove_node(start)
        except nx.exception.NetworkXNoCycle:
            pass
    # return the final matching
    matchG = nx.Graph()
    matchG.add_nodes_from(G)
    for n, d in G.nodes.items():
        matchG.add_edge(n, d['match'])
    return matchG

def max_weight(Gph, maxcardinality=True):
    return nx.Graph(max_weight_matching(Gph, maxcardinality))

def rank_value_assignment(Gph, rank_vector = list(range(len(Gph.nodes()), 0, -1)):
    """
    Implements the rank-value family of mechanisms (Featherstone, 2020) for assignment
    """
    rankval_lp = pulp.lpProblem("rank-value", pulp.LpMaximize)
    agents = [(agent, data) for agent, data in G.nodes.items() if data['bipartite'] == 1]
    items = [(item, data) for item, data in G.nodes.items() if data['bipartite'] == 0]
    assig = [[]]
    for i in range(len(agents)):
        for item in items:
            assig[i].append(pulp.LpVariable('x' + str(agents[i]) + str(item), lowBound=0, upBound=1, cat='Continuous'))
        assig.append([])
    for i in range(len(agents)):
        for j in range(len(items)):
            rank = agents[i]['ranking'][items[j]]
            rankValue = rank_vector[rank-1]
            rankval_lp += rankValue * assig[i][j]
    rankval_lp.solve()
    matchG = nx.Graph()
    matchG.add_nodes_from(Gph)
    for i in range(len(agents)):
        for j in range(len(items)):
            if assig[i][j].varValue == 1:
                matchG.add_edge(agents[i], items[j])
    return matchG

#
# def psm(G):
#


# def galeShapleyG(G):
#     matchG = nx.Graph()
#     matchG.add_nodes_from(G)
#     nx.set_node_attributes(matchG, values=None, name='currMatch')
#     all = matchG.nodes(data=True)
#     students = [(n, d) for n, d in all if d['bipartite'] = 1]
#     schools = [(n, d) for n, d in all if d['bipartite'] = 0]
#     n = min(len(students), len(schools))
#     # free => unmatched + still have a school to propose to
#     freeStudents = deepcopy(students)
#     freeschools = deepcopy(schools)
#     while len(freeStudents) > 0:
#         for student in freeStudents:
#             stuRanks = student[1]['ranking']
#             for school in stuRanks:
#                 if school in freeschools:
#                     freeschools.remove(school)
#                     school[1]['currMatch'] = student[0]
#                     freeStudents.remove(student)
#                     student[1]['currMatch'] = school[0]
#                     break
#                 else:
#                     c = [(s, d) for s, d in schools if s == school]
#                     schDict = c[0][1]
#                     cRanks = schDict['ranking']
#                     if cRanks[schDict['currMatch']] > cRanks[student[0]]:
#                         freeStudents.remove(student)
#                         schDict['currMatch'] = student[0]
# def serialdict(agents, items, ordering = None):
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


# this is all designed with graph inputs

# def pre_bipartite(G):
#     # preprocess to ensure |students| = |schools|
#     # may be unnecessary - revisit
#     all = G.nodes()
#     students = [n for n in all if n['bipartite'] = 1]
#     schools = [n for n in all if n['bipartite'] = 0]
#     dummyRanks = [n+1 for i in range(n)]
#     if len(students) < len(schools):
#         m, n = len(students), len(schools)
#         dummyData = dict(zip(schools, dummyRanks))
#         type = 0
#     elif len(students) > len(schools):
#         m, n = len(schools), len(students)
#         dummyData = dict(zip(students, dummyRanks))
#         type = 1
#     else:
#         return G
#     for i in range(1, n-m+1):
#         name = 'dummy' + str(i)
#         G.add_node(name, bipartite=type, ranking=dummyData)
#     return G
