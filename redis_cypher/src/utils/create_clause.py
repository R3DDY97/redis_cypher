#!/usr/bin/env python3
"""supporting functions for filtering clauses queries."""

import redis_db
import parser_utils
import re_utils


GRAPH_NODES = redis_db.get_allnodes()
LABELS = redis_db.R3DIS.smembers("labels")
NODE_IDS = redis_db.R3DIS.smembers("id")


def create_handler(create_query):
    query_nodes, query_relations = re_utils.regex_entities(create_query)

    # same node with multiple relations ? - to do
    nodes_list = parser_utils.parse_nodes(query_nodes)
    node_ids = set([node[1]["id"] for node in nodes_list])
    NODE_IDS.update(node_ids)
    redis_db.add_entities(nodes_list)

    # same relation with multiple source and target nodes ? - to do
    relationship_list = parser_utils.parse_relationships(query_relations)
    if relationship_list:
        target_nodes, source_nodes, relations = zip(*relationship_list)
        rel_nodes = target_nodes + source_nodes

        extra_nodes = [n for n in rel_nodes if n[1]["id"] not in NODE_IDS]
        redis_db.add_relations(relations)
        redis_db.add_entities(extra_nodes)
    # created_entities = {"nodes": nodes_list + extra_nodes,
    #                     "relations": relations}
    # return created_entities
