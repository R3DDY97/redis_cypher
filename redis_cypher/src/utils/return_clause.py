#!/usr/bin/env python3
"""supporting functions for filtering clauses queries."""

# import redis_db
import parser_utils
# import re_utils


# GRAPH_NODES = redis_db.get_allnodes()
# LABELS = redis_db.R3DIS.smembers("labels")
# NODE_IDS = redis_db.R3DIS.smembers("id")


def return_handler(return_query, subgraph):
    parsed_return = parser_utils.parse_return(return_query)
    print(parsed_return)
    print(subgraph)
    returned = [subgraph[mid][key] for mid, key in parsed_return]
    print(returned)
    return returned
