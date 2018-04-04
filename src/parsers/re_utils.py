#!/usr/bin/env python3
'''helps in parsing and getting entities from cypher query statement using regexp'''


import re
import json


# writing clauses       = [CREATE, DELETE, DETACH_DELETE, SET, REMOVE]
# projecting cluases    = [RETURN, WITH, UNWIND]
# reading clauses       = [MATCH]
# reading subclause     = [WHERE, SKIP, LIMIT, 'ORDER BY']
# read_write_subclauses = [MERGE, CALL]

# RE_NODE = re.compile(r"\(.*?\)")
# RE_RELATION = re.compile(r"\[.*?\]")
# RE_PROPERTY = re.compile(r"{.*?}")


# NODE_RGX = r"\(.*?\)"
# RELATION_RGX = r"\[.*?\]"
# PROPERTY_RGX = r"{.*?}"
# NODE_ID_RGX = r"([^{,])+"


def regex_clause(query):
    '''returns cypher clause if query satrts with any'''
    re_clause = re.match(r"[a-zA-Z]+", query.strip())
    if re_clause:
        clause, query = re_clause.group(), query[re_clause.end():].strip()
        return clause, query
    else:
        return None


def regex_node(query):
    re_node = re.match(r"\(.*?\)", query)
    if re_node:
        node, query = re_node.group()[1:-1], query[re_node.end():].strip()
        return node, query
    return None

# def entity_object(self, entity):
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
