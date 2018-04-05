#!/usr/bin/env python3

import os
import collections
import redis


R3DIS = redis.StrictRedis()


def add_node(node_data):
    node_id, mapping = node_data  # mapping should have id, property, incoming n outgoing relations as keys
    R3DIS.hmset("node:{}".format(node_id), mapping)
    R3DIS.save()


def delete_node(node_id):
    R3DIS.hdel(node_id, 'id', 'property', 'in_reln', 'out_rltn')
    R3DIS.save()


def add_relation(relation_data):
    reln_id, mapping = relation_data
    R3DIS.hmset("relation:{}".format(reln_id), mapping)
    R3DIS.save()


def add_entity(entity_data):
    if not entity_data:
        print("Cant store empty entity in DB ")
        return None
    entity_id, mapping = entity_data
    R3DIS.hmset(entity_id, mapping)
    R3DIS.save()


def add_entities(entity_list):
    if not entity_list:
        print("Cant store empty entity list in DB ")
        return None
    for entity in entity_list:
        entity_id, mapping = entity
        R3DIS.hmset(entity_id, mapping)
    R3DIS.save()
