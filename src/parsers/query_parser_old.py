#!/usr/bin/env python3
'''parses cypher query commands'''

import re
import json


# writing clauses       = [CREATE, DELETE, DETACH_DELETE, SET, REMOVE]
# projecting cluases    = [RETURN, WITH, UNWIND]
# reading clauses       = [MATCH]
# reading subclause     = [WHERE, SKIP, LIMIT, 'ORDER BY']
# read_write_subclauses = [MERGE, CALL]

RE_NODE = re.compile(r"\(.*?\)")
RE_RELATION = re.compile(r"\[.*?\]")
RE_PROPERTY = re.compile(r"{.*?}")


def query_statement(query):
    '''checks for main cluase in the query and calls appropriate clause parser'''
    query_element_list = query.split()
    if query_element_list[0].upper() == 'CREATE':
        return create_clause_parser(query)


def create_clause_parser(query):
    nodes = RE_NODE.findall(query)
    relations = RE_RELATION.findall(query)


def parse_node(cypher_node):
    node_property = RE_PROPERTY.findall(node)


def parse_node(query):
    if not query[0] == '(' and query[-1] == ')':
        return None
