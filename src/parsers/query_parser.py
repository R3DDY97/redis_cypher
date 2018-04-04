#!/usr/bin/env python3
'''parses cypher query commands'''

import os
import re
import json
from redis_store import redis_db
import re_utils


# writing clauses       = [CREATE, DELETE, DETACH_DELETE, SET, REMOVE]
# projecting cluases    = [RETURN, WITH, UNWIND]
# reading clauses       = [MATCH]
# reading subclause     = [WHERE, SKIP, LIMIT, 'ORDER BY']
# read_write_subclauses = [MERGE, CALL]

# RE_NODE = re.compile(r"\(.*?\)")
# RE_RELATION = re.compile(r"\[.*?\]")
# RE_PROPERTY = re.compile(r"{.*?}")


# NODE_RGX = r"\(.*?\)"
# RELATION_RGX = r"\[.*?\]"
# PROPERTY_RGX = r"{.*?}"
# NODE_ID_RGX = r"([^{,])+"


class CypherGraph():

    # clauses_dict = {"CREATE": self.parse_create, "MATCH": self.parse_match, "RETURN": self.parse_return, }

    graph_nodes = []
    graph_relations = []

    # NODE_RGX = r"\(.*?\)"
    # RELATION_RGX = r"\[.*?\]"
    # PROPERTY_RGX = r"{.*?}"
    # NODE_ID_RGX = r"([^{,])+"

    def parse_query(self, query):
        '''checks for main cluase in the query and calls appropriate clause parser'''
        re_clause = re_utils.regex_clause(query)
        if re_clause:
            clause, query = re_clause
        else:
            return None
        # return clauses_dict[clause](query)
        if clause == "CREATE":
            return self.parse_create(query)

        if clause == "MATCH":
            return self.parse_match(query)

    def parse_create(self, query):
        self.cypher_nodes = []
        while True:
            node_parsed = self.parse_node(query)
            if node_parsed:
                cypher_node, query = node_parsed
                self.cypher_nodes.append(cypher_node)
            if query and query[0] == ",":
                query = query[1:].strip()
            else:
                break

        if query and query[0] == "-":
            return self.handle_relationship(query.strip("-"))
            source_node = self.cypher_nodes[-1]
            parsed_rltn = self.parse_relationship(query.strip("-"))
            if not parsed_rltn:
                print("Error in syntax")
                os.sys.exit()
            relationship, query = parsed_rltn
            if query[0] == ">":
                # directed relationship
                parsed_target = self.parse_node(query[1:].strip())

        if self.cypher_nodes:
            for node in self.cypher_nodes:
                redis_db.add_node(node)
        return query

    def parse_node(self, query):
        '''returns python obj type to save into db and refer easily from cypher node entity'''
        re_node = re_utils.regex_node(query)

        if not re_node:
            return None
        node, query = re_node

        re_property = re_utils.regex_property(node)
        node_id, node_property = re_property or (node, {})
        node_name, *node_label = node_id.split(":")

        cypher_node = [node_id, {"name": node_name, "label": node_label, "property": node_property,
                                 "incoming_relns": {}, "outgoing_relns": {}, "undirected_relns": {}}]
        self.graph_nodes.append(cypher_node)
        return cypher_node, query

    def parse_relation(self, query):
        '''returns python obj type to save into db and refer easily from cypher relation entity'''
        re_rltn = re_utils.regex_relation(query)
        if not re_rltn:
            return None
        relation, query = re_rltn
        re_property = re_utils.regex_property(relation)
        reln_id, reln_property = re_property or (relation, {})
        reln_name, *reln_label = reln_id.split(":")
        cypher_reln = [reln_id, {"name": reln_name, "label": reln_label, "property": reln_property,
                                 "source_node": {}, "target_node": {}, "undirected_nodes": {}}]
        return cypher_reln, query

    def handle_relationship(self, query):
        source_node = self.cypher_nodes[-1]
        parsed_relation = self.parse_relation(query)
        if not parsed_relation:
            print("syntax error")
            os.sys.exit()
        relation_entity, query = parsed_relation
        if query[0] == ">":
            # directed relationship
            directionality = "directed"
            query = query.strip("> ")
        else:
            directionality = "undirected"

        parsed_node = self.parse_node(query)
        if not parsed_node:

            print("syntax error ----- 'NO target node found'")
        target_node, query = parsed_node
        return source_node, relation_entity, target_node, query

    def parse_match(self, query):
        pass

    def execute_cypher(self, cypher_query):
        query = cypher_query
        if not cypher_query[0] in ["'", '"']:
            return self.parse_query(query)


# def main(self, ):
#     os.system("clear")
#     execute_cypher('cypher_query')


# if __name__ == '__main__':
#     main()
