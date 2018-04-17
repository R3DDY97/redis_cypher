#!/usr/bin/env python3
"""supporting functions for filtering clauses queries."""

import redis_db
# from parser_utils import parse_item
import parser_utils
import re_utils


GRAPH_NODES = redis_db.get_allnodes()
LABELS = redis_db.R3DIS.smembers("labels")
NODE_IDS = redis_db.R3DIS.smembers("id")


# handle --> and <-- or plain []- any relation  , lable-many nodes-return many nodes property,
# type(r),

def match_handler(match_query):
    re_where = re_utils.regex_where(match_query)
    match_query, where_query = re_where
    match_nodes, match_relations = parser_utils.parse_match(match_query)
    match_labels = {node[1]["id"]: node[1]["label"] for node in match_nodes}
    if not match_labels:
        subgraph = GRAPH_NODES
        return subgraph
    if where_query:
        return where_handler(where_query, match_labels)
    subgraph = {mid: redis_db.attribute_nodes(match_labels[mid]) for mid in match_labels}
    return subgraph


def where_handler(where_query, match_labels):
    where_dict = parser_utils.parse_where(where_query)
    subgraph = {}
    for mid, attr in where_dict.items():
        matched_nodes = redis_db.attribute_nodes(match_labels[mid])
        for key, value in attr.items():
            final_list = {mid: node for node in matched_nodes if node[key] == value}
            subgraph.update(final_list)
    return subgraph
