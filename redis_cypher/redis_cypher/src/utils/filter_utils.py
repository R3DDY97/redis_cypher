#!/usr/bin/env python3
"""supporting functions for filtering clauses queries."""

# import json
import redis_db
from parser_utils import parse_item

# def get_allnodes():
#     cursor, node_names = redis_db.R3DIS.scan(match="node:*")
#     while cursor != 0:
#         cursor, nodes = redis_db.R3DIS.scan(cursor=cursor, match="node:*")
#         node_names.extend(nodes)

#     byte_nodes = [redis_db.R3DIS.hgetall(i) for i in node_names]
#     redis_db.attribute_nodes = [{k.decode(): v.decode() for k, v in b.items()} for b in byte_nodes]
#     return redis_db.attribute_nodes


# def attribute_nodes(attr):
#     str_nodes = [i.replace(b"'", b'"').decode() for i in redis_db.R3DIS.smembers(attr)]
#     node_list = [json.loads(node) for node in str_nodes]
#     return node_list


GRAPH_NODES = redis_db.get_allnodes()
LABELS = redis_db.R3DIS.smembers("labels")
NODE_IDS = redis_db.R3DIS.smembers("id")


def match_handler(match_nodes, re_where):
    match_labels = {node[1]["id"]: node[1]["label"] for node in match_nodes}
    # match_labels = {node[1]["label"]: node[1]["id"] for node in match_nodes}
    if not match_labels:
        matched_nodes = GRAPH_NODES
        return matched_nodes
    # matched_nodes = [redis_db.attribute_nodes(attr) for attr in match_labels.values()]
    return where_handler(re_where, match_labels)


def where_handler(where_query, match_labels):
    where_conditions = [cond.split("=") for cond in where_query.split(",")]
    where_dict = {parse_item(i.split(".")[0]): {parse_item(i.split(".")[1]): parse_item(j)}
                  for i, j in where_conditions}
    return_input = {}
    for mid, attr in where_dict.items():
        matched_nodes = redis_db.attribute_nodes(match_labels[mid])
        # matched_nodes = {mid: redis_db.attribute_nodes(match_labels[mid])}
        for key, value in attr.items():
            final_list = {mid: node for node in matched_nodes if node[key] == value}
            return_input.update(final_list)
    return return_input
