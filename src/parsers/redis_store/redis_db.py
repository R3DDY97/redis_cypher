#!/usr/bin/env python3

import os
import collections
import redis


R3DIS = redis.StrictRedis()


def add_node(node_data):
    node_id, mapping = node_data  # mapping should have id, property, incoming n outgoing relations as keys
    R3DIS.hmset(node_id, mapping)
    R3DIS.save()


def delete_node(node_id):
    R3DIS.hdel(node_id, 'id', 'property', 'in_reln', 'out_rltn')
    R3DIS.save()


def add_relation(relation_data):
    source, relation, target = relation_data
