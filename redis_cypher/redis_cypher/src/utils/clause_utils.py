#!/usr/bin/env python3
"""supporting parsers for parsing query."""

# import os

import parser_utils
import re_utils
import redis_db
import match_clause
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
    output = None
    for c, q in clauses_query:
        if c == "CREATE":
            eval_create(q)
        else:
            output = clauses_dict[c](q, output)
    print(output)
    return output


def eval_create(clause_query):
    query_nodes, query_relations = re_utils.regex_entities(clause_query)
    nodes_list = parser_utils.parse_nodes(query_nodes)
    node_ids = set([node[1]["id"] for node in nodes_list])
    NODE_IDS = redis_db.R3DIS.smembers("id")
    NODE_IDS.update(node_ids)
    relationship_list = parser_utils.parse_relationships(query_relations)
    target_nodes, source_nodes, relations = zip(*relationship_list)
    rel_nodes = target_nodes + source_nodes
    extra_nodes = [n for n in rel_nodes if n[1]["id"] not in NODE_IDS]
    # for i in [relations, target_nodes, source_nodes, nodes_list]:
    for i in [relations, extra_nodes, nodes_list]:
        redis_db.add_entities(i)


def eval_set(set_query):
    nodes, relations = re_utils.regex_entities(set_query)
    nodes = {key: value for key, value in nodes}
    redis_db.R3DIS.add_entities(nodes)


def eval_match(match_query):
    re_where = re_utils.regex_where(match_query)
    if re_where:
        match_query, where_query = re_where

    nodes, relations = re_utils.regex_entities(match_query)
    match_nodes = parser_utils.parse_nodes(nodes)
    if relations:
        relations = parser_utils.parse_relationships(relations)
    return match_clause.match_handler(match_nodes, re_where)


def eval_return(return_query, return_input):
    return_items = [dict([cond.split(".")]) for cond in return_query.split(",")]
    final_return = [[return_input[k][v] for k, v in cond.items()] for cond in return_items]
    print(final_return)
    return final_return


clauses_dict = {"CREATE": eval_create,
                "SET": eval_set,
                "MATCH": eval_match,
                "RETURN": eval_return, }
