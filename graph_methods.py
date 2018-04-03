#!/usr/bin/env python3
''' implementing opencypher graph QL in redis DB'''
import json
import redis

R3DIS = redis.StrictRedis()

def create_node(label=None, alias=None, node_property=None):
    '''create node in redis db'''
    mapping = {'label' : label, "alias": alias, 'node_property': node_property}
    R3DIS.hmset("alias:label", mapping)

def objectify_bytes(data):
    ''''returns python dict obj from redis output'''
    return json.loads(data.decode().replace("'", '"'))


def make_relation(node1, node2, label='', alias='', rel_property=''):
    '''generate relation between nodes'''
    node1_details, node2_details = map(get_node, (node1, node2))
    mapping = {node1: node1_details, node2: node2_details, 'relation':rel_property}
    R3DIS.hmset(alias+":"+label, mapping=mapping)


def get_node(node):
    '''return node node_details from redis DB'''
    node_details = R3DIS.hgetall(node)
    return node_details
