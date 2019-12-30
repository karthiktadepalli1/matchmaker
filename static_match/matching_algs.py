# algorithms for two-sided matching
from copy import deepcopy
import networkx as nx
from matchmaker.helpers import listify_rankings

def deferredAcceptance(Gph):
    """
    Implements the student-proposing deferred acceptance algorithm.
    """
    G = deepcopy(Gph)
    nx.set_node_attributes(G, {'currMatch': None, 'numProposals': 0})
    students = [(student, data) for student, data in G.nodes.items() if data['bipartite'] == 1]
    schools = [(school, data) for school, data in G.nodes.items() if data['bipartite'] == 0]
    while True:
        freeStudents = [(n, d) for n, d in students if d['currMatch'] is None]
        if len(freeStudents) == 0:
            break
        for student, stuDict in freeStudents:
            stuRanks = listify_rankings(stuDict['ranking'])
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
        match = d['currMatch']
        if match != 'unmatched':
            matchG.add_edge(n, match)
    return matchG

def rank_value_match(Gph, rank_matrix):
    """
    TODO: implement two-sided rank-value matching.
    Gph: nx.Graph
        a graph with students and students on which the matching takes place.
    rank_matrix: int[][]
        a matrix where a_ij denotes the value of a match which the student ranks as i and the school ranks as j.
    """
    lenStu = len(students)
    lenSch = len(schools)
    rankval_lp = pulp.lpProblem("rank-value", pulp.LpMaximize)
    students = [(student, data) for student, data in G.nodes.items() if data['bipartite'] == 1]
    schools = [(school, data) for school, data in G.nodes.items() if data['bipartite'] == 0]
    assig = [[]]
    for i in range(lenStu):
        for school in schools:
            assig[i].append(pulp.LpVariable('x' + str(students[i]) + str(school), lowBound=0, upBound=1, cat='Continuous'))
        assig.append([])
    for i in range(lenStu):
        for j in range(lenSch):
            student_rank = students[i]['ranking'][schools[j]]
            school_rank = schools[j]['ranking'][students[i]]
            rankValue = rank_matrix[student_rank-1][school_rank-1]
            rankval_lp += rankValue * assig[i][j]
    rankval_lp.solve()
    matchG = nx.Graph()
    matchG.add_nodes_from(Gph)
    for i in range(lenStu):
        for j in range(lenSch):
            if assig[i][j].varValue == 1:
                matchG.add_edge(students[i], schools[j])
    return matchG
