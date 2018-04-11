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


graph_nodes = []
graph_relations = []


def parse_query(query):
    '''checks for main cluase in the query and calls appropriate clause parser'''
    re_clause = regex_clause(query)
    if re_clause:
        clause, query = re_clause
    else:
        return None
    # return clauses_dict[clause](query)
    if clause == "CREATE":
        return parse_create(query)

    if clause == "MATCH":
        return parse_match(query)


def parse_create(query):
    cypher_nodes = []
    while True:
        node_parsed = parse_node(query)
        if node_parsed:
            cypher_node, query = node_parsed
            cypher_nodes.append(cypher_node)
        if query and query[0] == ",":
            query = query[1:].strip()
        else:
            break

    if query[0] == "-":
        return handle_relationship(query.strip("-"))
        source_node = cypher_nodes[-1]
        parsed_rltn = parse_relationship(query.strip("-"))
        if not parsed_rltn:
            print("Error in syntax")
            os.sys.exit()
        relationship, query = parsed_rltn
        if query[0] == ">":
            # directed relationship
            parsed_target = parse_node(query[1:].strip())

    if cypher_nodes:
        for node in cypher_nodes:
            redis_db.add_node(node)
    return query


def parse_node(query):
    '''returns python obj type to save into db and refer easily from cypher node entity'''

    re_node = regex_node(query)
    if not re_node:
        return None
    node, query = re_node

    re_property = regex_property(node)
    node_id, node_property = re_property or (node, {})
    node_name, *node_label = node_id.split(":")

    cypher_node = [node_id, {"name": node_name, "label": node_label, "property": node_property,
                             "incoming_relns": {}, "outgoing_relns": {}, "undirected_relns": {}}]
    graph_nodes.append(cypher_node)
    return cypher_node, query


def parse_relation(query):
    '''returns python obj type to save into db and refer easily from cypher relation entity'''
    re_rltn = regex_relation(query)
    if not re_rltn:
        return None
    relation, query = re_rltn
    re_property = regex_property(relation)
    reln_id, reln_property = re_property or (relation, {})
    reln_name, *reln_label = reln_id.split(":")
    cypher_reln = [reln_id, {"name": reln_name, "label": reln_label, "property": reln_property,
                             "source_node": {}, "target_node": {}, "undirected_nodes": {}}]
    return cypher_reln, query


def handle_relationship(query):
    source_node = cypher_nodes[-1]
    parsed_relation = parse_relation(query)
    if not parsed_relation:
        print("syntax error")
        os.sys.exit()
    relation_entity, query = parsed_relation
    if query[0] == ">":
        # directed relationship
        directionality = "directed"
        query = query.strip("> ")
    else:
        directionality = "undirected"

    parsed_node = parse_node(query)
    if not parsed_node:

        print("syntax error ----- 'NO target node found'")
    target_node, query = parsed_node
    return source_node, relation_entity, target_node, query


def parse_match(query):
    pass


def regex_clause(query):
    '''returns cypher clause if query satrts with any'''
    re_clause = re.match(r"[a-zA-Z]+", query.strip())
    if re_clause:
        clause, query = re_clause.group(), query[re_clause.end():].strip()
        return clause, query
    else:
        return None


def regex_node(query):
    re_node = re.match(r"(.*?)", query)
    if re_node:
        node, query = re_node.group()[1:-1], query[re_node.end():].strip()
        return node, query
    return None

# def entity_object(entity):
#     ''''takes cypher entity and returns its name:label, property'''
#     re_property = regex_property(entity)
#     if not re_property:
#         return entity
#     return re_property


def regex_property(entity):
    ''''regex to get property and id of cypher entity '''
    re_property = re.search(r"{.*?}", entity)
    if re_property:
        entity_id, entity_property = entity[:re_property.start()], re_property.group().replace("'", '"')
        entity_property = json.loads(entity_property)
        return entity_id, entity_property
    return None


def regex_relation(query):
    '''returns relation entity and query after parsing query'''
    re_rltn = re.match(r"\[.*?\]", query)
    if re_rltn:
        relation, query = re_rltn.group()[1:-1], query[re_rltn.end():].strip("- ")
        return relation, query
    return None


def execute_cypher(cypher_query):
    if not cypher_query[0] in ["'", '"']:
        return parse_query(cypher_query)


def main():
    os.system("clear")
    execute_cypher('cypher_query')


if __name__ == '__main__':
    main()
