#!/usr/bin/env python3
'''helps in parsing and getting entities from cypher query statement using regexp'''

import re
# import json


def regex_query(query):
    '''searches cypher query and returns (tuple clause, sub_query) list'''
    re_clause = re.findall("CREATE|MATCH|WHERE|RETURN", query)
    re_query = re.split("CREATE|MATCH|WHERE|RETURN", query)[1:]
    clause_list = [(c, regex_entities(q)) for c, q in zip(re_clause, re_query)]
    return clause_list


def regex_entities(clause_query):
    matched_entities = re.findall(r"\(.*?\)(?!-)", clause_query)
    relations = re.findall(r"\([\w,:'\s{}]+?\)-\[.*?\]->\(.*?\)", clause_query)
    nodes = [item for item in matched_entities if item not in relations]
    return nodes, relations


def regex_property(entity):
    ''''regex to get property and id of cypher entity '''
    re_dict = re.search(r"{.*?}", entity)
    if re_dict:
        entity_id, entity_property = entity[1:re_dict.start()], re_dict.group()
        entity_property = dict((i.split(":") for i in entity_property[1:-1].split(",")))
        entity_property = fix_syntax(entity_property)
        return entity_id.strip(), entity_property
    return None


def fix_syntax(entity_property):
    '''returns input dict with parsing numbers'''
    entity_property = {k.strip(" '\""): v.strip() for k, v in entity_property.items()}
    for k, v in entity_property.items():
        if not "'" in v or '"' in v:
            entity_property[k] = str2number(v)
        else:
            entity_property[k] = v.strip(" '\"")
    return entity_property


def str2number(string):
    try:
        number = int(string)
    except ValueError:
        number = float(string)
    return number
