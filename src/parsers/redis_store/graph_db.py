#!/usr/bin/env python3

import os
import collections
import redis


class CypherRedis():

    R3DIS = redis.StrictRedis()

    def add_node(self, node_data):
        node_id, mapping = node_data  # mapping should have id, property, incoming n outgoing relations as keys
        self.R3DIS.hmset(node_id, mapping)

    def delete_node(self, node_id):
        self.R3DIS.hdel(node_id, 'id', 'property', 'in_reln', 'out_rltn')

    def add_relation(self, relation_data):
        source, relation, target = relation_data
