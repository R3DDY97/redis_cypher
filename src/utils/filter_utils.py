#!/usr/bin/env python3
''''supporting functions for filtering clauses queries'''

import decode_redis
import redis_db


def match_filter(match_nodes):
    # match_ids, match_labels = zip(*match_nodes)
    graph_nodes = redis_db.R3DIS.scan("node:*")
    labels_to_match = {l: i for i, l in zip(*match_nodes)}
    if not labels_to_match:
        matched_nodes = decode_redis.decode_list(graph_nodes)
    matched_nodes = [i for i in graph_nodes if i[1]["label"] in labels_to_match]
    matched_ids = [labels_to_match[i] for i in matched_nodes if i[1]["label"] in labels_to_match]
    return {i: n for i, n in zip(matched_ids, matched_nodes)}


def handle_where(where_query):
    where_conditions = [cond.split("=") for cond in where_query.split(", ")]
    where_dict = {i.split(".")[0]: (i.split(".")[1], j) for i, j in where_conditions}


def handle_return(return_query):
    pass
