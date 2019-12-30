# frontend for users to input data and interact with the algorithms

def read_from_dataframes(agents_df, items_df, restrictedMatch = None):
    """
    function to read dataframes into a complete graph representing the market.
    Dataframe must have one row per agent/item. If bipartite, one column must be labelled "bipartite" and be 1 or 0 depending on whether the row is an agent.
    """
    G = nx.Graph()
    agents = agent_df.to_dict('records')
    for agentDict in agents:
        agentDict['bipartite'] = 1
    lenAg = len(agents)
    agentTuples = [(i, agents[i]) for i in range(lenAg)]
    items = items_df.to_dict('records')
    for itemDict in items:
        itemDict['bipartite'] = 0
    lenIt = len(items)
    itemsTuples = [(i, items[i]) for i in range(lenAg, lenAg + lenIt)]
    G.add_nodes_from(agentTuples)
    G.add_nodes_from(itemsTuples)
    # add edges between every agent and item
    G.add_edges_from(itertools.product(range(lenAg), range(lenAg, lenAg + lenIt)))
    if restrictedMatch is not None:
        # TODO: implement a way to remove edges in the graph corresponding to restrictions on legitimate matches
    return G

def read_from_csvs(agents_filepath, items_filepath, restrictedMatch = None):
    agents_df = pd.read_csv(agents_filepath)
    items_df = pd.read_csv(items_filepath)
    return read_from_dataframes(agents_df, items_df, restrictedMatch)
