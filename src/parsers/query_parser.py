#!/usr/bin/env python3
'''parses cypher query commands'''

import os
import re
import json
from redis_store import redis_db


# writing clauses       = [CREATE, DELETE, DETACH_DELETE, SET, REMOVE]
# projecting cluases    = [RETURN, WITH, UNWIND]
# reading clauses       = [MATCH]
# reading subclause     = [WHERE, SKIP, LIMIT, 'ORDER BY']
# read_write_subclauses = [MERGE, CALL]

# RE_NODE = re.compile(r"\(.*?\)")
# RE_RELATION = re.compile(r"\[.*?\]")
# RE_PROPERTY = re.compile(r"{.*?}")

NODE_RGX = r"\(.*?\)"
RELATION_RGX = r"\[.*?\]"
PROPERTY_RGX = r"{.*?}"
NODE_ID_RGX = r"([^{,])+"


def parse_query(query):
    '''checks for main cluase in the query and calls appropriate clause parser'''
    re_clause = re.search(r"[a-zA-Z]+", query.strip())
    if re_clause:
        clause, query = re_clause.group(), query[re_clause.end():].strip()
    else:
        return None
    if clause == "CREATE":
        return parse_create(query)
    if clause == "MATCH":
        pass


def parse_create(query):
    cypher_nodes = []
    while True:
        node_parsed = parse_node(query)
        if node_parsed:
            cypher_node, query = parse_node(query)
            cypher_nodes.append(cypher_node)
        if query and query[0] == ",":
            query = query[1:].strip()
        else:
            break
    if cypher_nodes:
        for node in cypher_nodes:
            redis_db.add_node(node)
    return query


def parse_node(query):
    re_node = re.match(NODE_RGX, query)
    if not re_node:
        return None
    node, query = re_node.group()[1:-1], query[re_node.end():].strip()
    re_property = re.search(PROPERTY_RGX, node)
    if re_property:
        node_id, node_property = node[:re_property.start()], re_property.group().replace("'", '"')
        node_property = json.loads(node_property)
    else:
        node_id = node
        node_property = {}
    node_name, *node_label = node_id.split(":")

    cypher_node = [node_id, {"name": node_name,
                             "label": node_label,
                             "property": node_property,
                             "relations": {"incoming": {}, "outgoing": {}, "undirected": {}}
                             }]
    return cypher_node, query


# def re_parsing(pattern, query):
#     result = re.match(pattern, query)
#     if not result:
#         return None
#     matched, query = result.group(), query[result.end():]
#     return matched, query


def execute_cypher(cypher_query):
    if not cypher_query[0] in ["'", '"']:
        return parse_query(cypher_query)


def main():
    os.system("clear")
    execute_cypher('cypher_query')


if __name__ == '__main__':
    main()
