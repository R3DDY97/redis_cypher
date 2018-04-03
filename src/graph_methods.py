#!/usr/bin/env python3
''' implementing opencypher graph QL in redis DB'''
import json
from collections import (ChainMap, Counter, defaultdict, deque)
import redis
# property graph = [ 'entity', 'path ', 'token, 'property', ]
# entitiy = {'node':{'label', 'incoming_rltn', 'outgoing_rltn'},
#             'relationship': {source_node, 'target_node'}}
# path = [length]
# token = ['label', 'relationship type', 'property key']
# property = ('property key, {value: opencypher_scalar || list(opencypher_scalars)})
# cypher_graph = {size:no_of_nodes, }


class Graph():
    ''''property graph object'''

    R3DIS = redis.StrictRedis()
    graph_dict = defaultdict(dict)

    def create_node(self, node_details):
        '''create node in redis db'''
        node, label, property_dict = node_details.values()

    def create_relationship(self, relationship_details):
        '''generate relation between nodes'''
        pass

    def create_path(self, nodes, relationships):
        '''creates path form matching pattern'''
        pass

    def delete_node(self, node_details):
        '''delets node from graph'''
        pass

    def detach_node(self, node_details):
        '''delets node from graph'''
        pass

    @classmethod
    def objectify_bytes(cls, data):
        ''''returns python dict obj from redis output'''
        return json.loads(data.decode().replace("'", '"'))

    def get_node(self, node):
        '''return node node_details from redis DB'''
        node_details = self.R3DIS.hgetall(node)
        return node_details
