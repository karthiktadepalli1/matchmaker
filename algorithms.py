import numpy as np
import pulp as plp
from copy import deepcopy
import networkx as nx
from networkx.algorithms import bipartite
from networkx.algorithms.cycles import find_cycle
from networkx.algorithms.matching import max_weight_matching

def serialDictatorship(Gph, ordering = None):
    G = deepcopy(Gph)
    agents, items = bipartite.sets(G)
    np.random.shuffle(agents)
    if ordering is not None:
        agents = ordering
    matchG = nx.Graph()
    matchG.add_nodes_from(G)
    for agent in agents:
        # remove already assigned objects
        itemsLeft = G.neighbors(agent)
        ranks = agent['ranking']
        for k in ranks:
            if k not in itemsLeft:
                ranks.remove(k)
        # match to preferred object
        if len(ranks) > 0:
            matchG.add_edge(agent, ranks[0])
            G.remove_node(ranks[0])
        # else unassigned

        # best = ranks.values().min()
        # for item, rank in ranks.items():
        #     if rank == best:
        #         # create an assignment, remove from graph
        #         matchG.add_edge([agent, item])
        #         G.remove_node(item)
        #         G.remove_node(agent)
    return matchG

def randomAssignment(Gph):
    G = deepcopy(Gph)
    agents, items = bipartite.sets(G)
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

# # helper to return the metadata associated with a node
# def quickData(Gph, nodeName):
#     G = deepcopy(Gph)
#     for n, d in G.nodes.items():
#         if n == nodeName:
#             return d

def deferredAcceptance(Gph):
    G = deepcopy(Gph)
    nx.set_node_attributes(G, {'currMatch': None, 'numProposals': 0})
    students = [(student, data) for student, data in G.nodes.items() if data['bipartite'] == 0]
    schools = [(school, data) for school, data in G.nodes.items() if data['bipartite'] == 1]
    while True:
        freeStudents = [(n, d) for n, d in students if d['currMatch'] is None]
        if len(freeStudents) == 0:
            break
        for student, stuDict in freeStudents:
            stuRanks = deepcopy(stuDict['ranking'])
            numProps = stuDict['numProposals']
            stuRanks = stuRanks[numProps:]
            # ranks are represented as a list
            for school in stuRanks:
                numProps += 1
                schDict = G.node(school)
                if schDict['currMatch'] is None:
                    stuDict['currMatch'] = school
                    schDict['currMatch'] = student
                    break
                else:
                    schRanks = schDict['ranking']
                    toUnmatch = schDict['currMatch']
                    if schRanks[student] < schRanks[toUnmatch]:
                        schDict['currMatch'] = student
                        stuDict['currMatch'] = school
                        unmatchedStud = G.node(toUnmatch)
                        unmatchedStud['currMatch'] = None
                        break
            # this is only reached if all schools reject
            stuDict['currMatch'] = 'unmatched'

    matchG = nx.Graph()
    matchG.add_nodes_from(G)
    for n, d in matchG.nodes.items():
        matchedTo = d['currMatch']
        if matchedTo != 'unmatched':
            matchG.add_edge(n, matchedTo)

def TTC(Gph):
    G = deepcopy(Gph)
    ttcGraph = nx.DiGraph()
    ttcGraph.add_nodes_from(G)
    matchG = nx.Graph()
    matchG.add_nodes_from(G)
    nx.set_node_attributes(G, None, 'match')
    while list(ttcGraph.nodes()) != []:
        # remove unavailable agents
        all = ttcGraph.nodes.items(data=True)
        for n, d in all:
            d['ranking'] = [i for i in d['ranking'] if i in ttcGraph.nodes()]
        # create graph and remove cycles
        pointers = [(n, d['ranking'][0]) for n, d in all]
        for start, end in pointers:
            ttcGraph.add_edge(start, end)
        try:
            while True:
                cycle = find_cycle(ttcGraph)
                for start, end in cycle:
                    G.node[start]['match'] = end
                    ttcGraph.remove_node(start)
        except nx.exception.NetworkXNoCycle:
            pass

    # return the final matching
    for n, d in G.nodes.items():
        matchG.add_edge(n, d['match'])
    return matchG

def max_weight(Gph, maxcardinality=True):
    matchSet = max_weight_matching(Gph, maxcardinality)
    matchG = nx.Graph(matchSet)
    return matchG

def convert_input_to_graph(inputData):
    # read in agents - what form could they be in?

    # construct the graph - unless agents have constraints, this will be a complete graph


#
# def psm(G):
#


# def galeShapleyG(G):
#     matchG = nx.Graph()
#     matchG.add_nodes_from(G)
#     nx.set_node_attributes(matchG, values=None, name='currMatch')
#     all = matchG.nodes(data=True)
#     students = [(n, d) for n, d in all if d['bipartite'] = 0]
#     schools = [(n, d) for n, d in all if d['bipartite'] = 1]
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
#     students = [n for n in all if n['bipartite'] = 0]
#     schools = [n for n in all if n['bipartite'] = 1]
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