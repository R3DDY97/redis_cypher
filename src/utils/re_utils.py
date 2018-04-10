#!/usr/bin/env python3
'''helps in parsing and getting entities from cypher query statement using regexp'''

import re


def regex_query(query):
    '''searches cypher query and returns (tuple clause, sub_query) list'''
    re_clause = re.findall("CREATE|MATCH|RETURN", query)
    re_query = re.split("CREATE|MATCH|RETURN", query)[1:]
    clause_list = [(c, q) for c, q in zip(re_clause, re_query)]
    return clause_list


def regex_where(match_query):
    '''searches cypher query and returns (tuple clause, sub_query) list'''
    re_where = re.findall("WHERE", match_query)
    if re_where:
        match_subquery, where_query = re.split("WHERE", match_query)
        return match_subquery, where_query
    return None


def regex_entities(clause_query):
    matched_entities = re.findall(r"\(.*?\)(?!-)", clause_query)
    re_relations = re.findall(r"\([\w,:'\s{}]+?\)-\[.*?\]->\(.*?\)", clause_query)
    relationships = [regex_relation(re_relation) for re_relation in re_relations]
    nodes = [item for item in matched_entities if item not in re_relations]
    return nodes, relationships


def regex_relation(re_relation):
    if re_relation:
        directed = "->" in re_relation
        nodes = re.findall(r"\(.*?\)", re_relation)
        relationship = re.search(r"\[.*?\]", re_relation).group()
    return directed, nodes, relationship


def regex_property(entity):
    ''''regex to fetch property from entities '''
    re_dict = re.search(r"{.*?}", entity)
    if re_dict:
        entity_id, entity_property = entity[1:re_dict.start()], re_dict.group()
        return entity_id, entity_property
    return None
