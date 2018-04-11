#!/usr/bin/env python3
''''supporting functions for parsing query'''

from redis_store import redis_db


def directed_update(source_node, cypher_reln, target_node):
    '''update nodes, directed relations, entity and store in redis'''
    cypher_reln[1]["target_node"].append(target_node)
    cypher_reln[1]["source_node"].append(source_node)
    source_node[1]["outgoing_relns"].append({"relation": cypher_reln, "node": target_node})
    target_node[1]["incoming_relns"].append({"relation": cypher_reln, "node": source_node})
    redis_db.add_entities([cypher_reln, source_node, target_node])
    redis_db.add_nodes([source_node, target_node])
    redis_db.add_relation(cypher_reln)


def undirected_update(source_node, cypher_reln, target_node):
    '''update nodes, undirected relations, entity and store in redis'''
    cypher_reln[1]["undirected_nodes"].append(target_node, source_node)
    source_node[1]["undirected_relns"].append({"relation": cypher_reln, "node": target_node})
    target_node[1]["undirected_relns"].append({"relation": cypher_reln, "node": source_node})
    # redis_db.add_entities([cypher_reln, source_node, target_node])
    redis_db.add_nodes([source_node, target_node])
    redis_db.add_relation(cypher_reln)
