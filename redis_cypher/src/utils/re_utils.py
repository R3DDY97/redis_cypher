#!/usr/bin/env python3
'''helps in parsing and getting entities from cypher query statement using regexp'''

import re


def regex_query(query):
    '''searches cypher query and returns (tuple clause, sub_query) list'''
    re_clause = re.findall(r"CREATE|WITH|MATCH|RETURN", query)
    re_query = re.split(r"CREATE|WITH|MATCH|RETURN", query)[1:]
    clause_list = [(c, q) for c, q in zip(re_clause, re_query)]
    return clause_list


def regex_where(match_query):
    '''searches cypher query and returns (tuple clause, sub_query) list'''
    re_where = re.findall("WHERE", match_query)
    if not re_where:
        return match_query, None

    match_subquery, where_query = re.split("WHERE", match_query)
    re_and = re.findall("AND", where_query)
    if re_and:
        where_query = re.split("AND", where_query)
    else:
        where_query = [where_query]
    return match_subquery, where_query


def regex_entities(clause_query):
    matched_entities = re.findall(r"\(.*?\)(?!-)", clause_query)
    re_relations = re.findall(r"\([\w,:'\s{}]+?\)<?-\[.*?\]->?\(.*?\)", clause_query)
    relationships = [regex_relation(re_relation) for re_relation in re_relations]
    nodes = [item.strip(" ()") for item in matched_entities if item not in re_relations]
    return nodes, relationships


def regex_relation(re_relation):
    if re_relation:
        directed = "->" in re_relation or "<-" in re_relation
        nodes = [node.strip(" ()") for node in re.findall(r"\(.*?\)", re_relation)]
        relationship = re.search(r"\[.*?\]", re_relation).group().strip(" []")
    return directed, nodes, relationship


def regex_property(entity):
    ''''regex to fetch property from entities '''
    re_dict = re.search(r"{.*?}", entity)
    if re_dict:
        entity_id, entity_property = entity[:re_dict.start()].strip(), re_dict.group()
        return entity_id, entity_property
    return None


def regex_return(return_query):
    '''searches cypher query and returns (tuple clause, sub_query) list'''
    re_str = r"AS|ORDER BY|SKIP|LIMIT|type\(.*?\)"
    re_subclause = re.findall(re_str, return_query)
    if re_subclause:
        re_subquery = re.split(re_str, return_query)
        re_subclause = ["RETURN"] + re_subclause
        subclause_list = {c: q for c, q in zip(re_subclause, re_subquery)}
        return subclause_list
    return None
