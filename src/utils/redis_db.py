#!/usr/bin/env python3

# import os
# import collections
import redis

R3DIS = redis.StrictRedis()


def add_node(node_data):
    node_id, mapping = node_data
    result = R3DIS.hmset(name="node:{}".format(node_id), mapping=mapping)
    R3DIS.save()
    print(result)


def add_nodes(nodes_list):
    for node in nodes_list:
        add_node(node)


def delete_node(node_id):
    R3DIS.hdel(node_id, 'id', 'property', 'in_reln', 'out_rltn')
    R3DIS.hdel("node:{}".format(node_id), 'id', 'property', 'in_reln', 'out_rltn')
    R3DIS.save()


def add_relation(relation_data):
    reln_id, mapping = relation_data
    R3DIS.hmset(name="relation:{}".format(reln_id), mapping=mapping)
    R3DIS.save()


def add_relations(relations_list):
    for relation in relations_list:
        add_relation(relation)


def add_entity(entity_data):
    if not entity_data:
        print("Cant store empty entity in DB ")
    entity_id, mapping = entity_data
    R3DIS.hmset(name=entity_id, mapping=mapping)
    result = R3DIS.save()
    print(result)


def add_entities(entity_list):
    if not entity_list:
        print("Cant store empty entity list in DB ")
    for entity in entity_list:
        entity_id, mapping = entity
        R3DIS.hmset(name=entity_id, mapping=mapping)
        if "label" in mapping:
            R3DIS.sadd("labels", mapping["label"])
        else:
            R3DIS.sadd(mapping["type"])
    R3DIS.save()


def get_allnodes():
    cursor, byte_nodes = R3DIS.scan(cursor=0, match="node*")
    node_keys = bytes2str(byte_nodes)
    nodes = {node: bytes2str(R3DIS.hgetall(node)) for node in node_keys}
    return nodes


def bytes2str(byte_group):
    if isinstance(byte_group, list):
        str_group = [b.decode() for b in byte_group]
    if isinstance(byte_group, dict):
        str_group = {k.decode(): v.decode() for k, v in byte_group.items()}
    return str_group


def dict2hash():
    pass


def list2set():
    pass


def get_match(item):
    cursor, byte_nodes = R3DIS.scan(cursor=0, match="{}*".format(item))
    node_keys = bytes2str(byte_nodes)
    nodes = {node: bytes2str(R3DIS.hgetall(node)) for node in node_keys}
    return nodes


def update_node_adjacancy(node_data):
    pass


def update_relation_adjcancy(relation_data):
    pass
