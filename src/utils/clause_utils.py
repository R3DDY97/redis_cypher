#!/usr/bin/env python3
"""supporting parsers for parsing query."""

# import os

import parser_utils
import re_utils
import redis_db
import filter_utils


# writing clauses       = [CREATE, DELETE, DETACH_DELETE, SET, REMOVE]
# projecting cluases    = [RETURN, WITH, UNPWIND]
# reading clauses       = [MATCH]
# reading subclause     = [WHERE, SKIP, LIMIT, 'ORDER BY']
# read_write_subclauses = [MERGE, CALL]


clauses_dict = {"CREATE": lambda pattern: eval_create(pattern),
                "SET": lambda pattern: eval_set(pattern),
                "MATCH": lambda pattern: eval_match(pattern),
                "RETURN": lambda pattern: eval_return(pattern), }

graph_data = {"nodes": [], "relations": []}
cypher_nodes = []
cypher_relations = []


def evaluate_cypher(query):
    cluases_query = re_utils.regex_query(query)
    first_clause, first_pattern = cluases_query[0]
    result = clauses_dict[first_clause](first_pattern)
    print(result)


def eval_create(clause_query):
    query_nodes, query_relations = re_utils.regex_entities(clause_query)
    nodes_list = parser_utils.parse_nodes(query_nodes)
    relationship_list = parser_utils.parse_relationships(query_relations)
    target_nodes, source_nodes, relations = zip(*relationship_list)
    for i in [nodes_list, relations, target_nodes, source_nodes]:
        redis_db.add_entities(i)

    # redis_db.add_nodes(entities_created["nodes"])
    # redis_db.add_relations(entities_created["relations"])


def eval_set(query):
    pass


def eval_match(match_query):
    re_where = re_utils.regex_where(match_query)
    if re_where:
        match_query, where_query = re_where
    query_entities = re_utils.regex_entities(match_query)
    nodes, relations = query_entities
    node_list = parser_utils.parse_nodes(nodes)
    if relations:
        relations = parser_utils.parse_relationships(relations)
    matched_dict = filter_utils.match_filter(node_list)
    where_dict = filter_utils.handle_where(where_query)
    match_where = []

    redis_db.R3DIS.scan


def eval_return(clause_query):
    pass
