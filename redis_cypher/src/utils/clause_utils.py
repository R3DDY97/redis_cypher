#!/usr/bin/env python3
"""supporting parsers for parsing query."""

# import os

# import parser_utils
import re_utils
import redis_db
import create_clause
import match_clause
import return_clause
# import filter_utils


# writing clauses       = [CREATE, DELETE, DETACH_DELETE, SET, REMOVE]
# projecting cluases    = [RETURN, WITH, UNPWIND]
# reading clauses       = [MATCH]
# reading subclause     = [WHERE, SKIP, LIMIT, 'ORDER BY']
# read_write_subclauses = [MERGE, CALL]


graph_data = {"nodes": [], "relations": []}
cypher_nodes = []
cypher_relations = []


def evaluate_cypher(query):
    clauses_query = re_utils.regex_query(query)
    # first_clause, first_pattern = clauses_query.pop(0)
    # if first_clause == "CREATE":
    #     clauses_dict[first_clause](first_pattern)
    for c, q in clauses_query:
        if c == "CREATE":
            eval_create(q)
        if c == "MATCH":
            sub_graph = eval_match(q)
        if c == "RETURN":
            eval_return(q, sub_graph)


def eval_create(create_query):
    created_graph = create_clause.create_handler(create_query)
    if created_graph:
        return created_graph


def eval_set(set_query):
    nodes, relations = re_utils.regex_entities(set_query)
    nodes = {key: value for key, value in nodes}
    redis_db.R3DIS.add_entities(nodes)


def eval_match(match_query):
    matched_graph = match_clause.match_handler(match_query)
    return matched_graph


def eval_return(return_query, subgraph):
    returned = return_clause.return_handler(return_query, subgraph)
    return returned


# clauses_dict = {"CREATE": eval_create,
#                 "SET": eval_set,
#                 "MATCH": eval_match,
#                 "RETURN": eval_return, }
