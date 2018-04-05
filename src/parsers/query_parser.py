#!/usr/bin/env python3
'''parses cypher query commands'''

import os
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

    # clauses_dict = {"CREATE": self.parse_create,
    #                 "MATCH": self.parse_match, "RETURN": self.parse_return, }

    graph_data = {"nodes": [], "relations": []}
    cypher_nodes = []
    cypher_relations = []

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
        if clause == "SET":
            return self.parse_set(query)

    def parse_create(self, query):
        '''parses and stores cypher CREATE clause query request'''
        while True:
            node_parsed = self.parse_node(query)
            if node_parsed:
                cypher_node, query = node_parsed
                self.cypher_nodes.append(cypher_node)
                self.graph_data["nodes"].append(cypher_node)
            if query and query[0] == ",":
                query = query[1:].strip()
            else:
                break

        if query and query[0] == "-":
            query = self.handle_relationship(query.strip("-"))

        if query and query[0] in "<-":
            # incoming relation while making Path query .. will do later
            pass

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
        node_id, node_property = re_property or (node.strip(), {})
        node_name, *node_label = node_id.split(":")
        mapping = {"name": node_name, "label": node_label,
                   "property": node_property, "incoming_relns": [],
                   "outgoing_relns": [], "undirected_relns": []}
        cypher_node = ["node:{}".format(node_id), mapping]
        self.graph_data["nodes"].append(cypher_node)
        self.cypher_nodes.append(cypher_node)
        # redis_db.add_node(cypher_node)
        return cypher_node, query

    def parse_relation(self, query):
        '''returns python obj type to save into db and refer easily from cypher relation entity'''
        re_rltn = re_utils.regex_relation(query)
        if not re_rltn:
            return None
        relation, query = re_rltn
        re_property = re_utils.regex_property(relation)
        reln_id, reln_property = re_property or (relation.strip(), {})
        reln_name, *reln_label = reln_id.split(":")
        mapping = {"name": reln_name, "label": reln_label,
                   "property": reln_property, "source_node": [],
                   "target_node": [], "undirected_nodes": []}
        cypher_reln = ["relation:{}".format(reln_id), mapping]
        self.graph_data["relations"].append(cypher_reln)
        self.cypher_relations.append(cypher_reln)
        # redis_db.add_relation(cypher_reln)
        return cypher_reln, query

    def handle_relationship(self, query):
        '''process cypher relationship between nodes'''
        source_node = self.cypher_nodes[-1]
        parsed_relation = self.parse_relation(query)
        if not parsed_relation:
            print("syntax error")
            os.sys.exit()
        cypher_reln, query = parsed_relation
        directed = query[0] == ">"
        if directed:            # directed relationship
            query = query.strip("> ")

        parsed_node = self.parse_node(query)
        if not parsed_node:
            print("syntax error ----- 'NO target node found'")
            os.sys.exit()
        target_node, query = parsed_node
        if directed:
            self.directed_update(source_node, cypher_reln, target_node)
        else:
            self.undirected_update(source_node, cypher_reln, target_node)
        return query

    @classmethod
    def directed_update(cls, source_node, cypher_reln, target_node):
        '''update nodes, directed relations, entity and store in redis'''
        cypher_reln[1]["target_node"].append(target_node)
        cypher_reln[1]["source_node"].append(source_node)
        source_node[1]["outgoing_relns"].append({"relation": cypher_reln, "node": target_node})
        target_node[1]["incoming_relns"].append({"relation": cypher_reln, "node": source_node})
        redis_db.add_entities([cypher_reln, source_node, target_node])

    @classmethod
    def undirected_update(cls, source_node, cypher_reln, target_node):
        '''update nodes, undirected relations, entity and store in redis'''
        cypher_reln[1]["undirected_nodes"].append(target_node, source_node)
        source_node[1]["undirected_relns"].append({"relation": cypher_reln, "node": target_node})
        target_node[1]["undirected_relns"].append({"relation": cypher_reln, "node": source_node})
        redis_db.add_entities([cypher_reln, source_node, target_node])

    def parse_set(self, query):
        pass

    def parse_match(self, query):
        pass

    def parse_return(self, query):
        pass

    def execute_cypher(self, cypher_query):
        ''''Takes cypher query as argument, parses and updates in redis-server'''
        query = cypher_query
        if not cypher_query[0] in ["'", '"']:
            return self.parse_query(query)
        print("Syntax error")
        return None



# def main(self, ):
#     os.system("clear")
#     execute_cypher('cypher_query')


# if __name__ == '__main__':
#     main()
