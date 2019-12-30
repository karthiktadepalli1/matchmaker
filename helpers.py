# helper functions used across the board

def listify_rankings(ranking_dict):
    """
    Given a dictionary of rankings, returns a list where the values are sorted by rank.
    Assumes preferences are strict. Will misbehave if they are not.
    """
    rankList = [-1 for item, rank in ranking_dict.items()]
    for item, rank in ranking_dict.items():
        rankList[rank-1] = item
    return rankList
