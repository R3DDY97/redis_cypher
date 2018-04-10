#!/usr/bin/env python3
"""evaluates and executes cypher query commands."""

import clause_utils


class Graph():

    def execute_cypher(self, query):
        """Takes cypher query as argument, parses and updates in redis-server"""
        if isinstance(query, str):
            return clause_utils.evaluate_cypher(query)
        print("Syntax error\nQuery should be string using OpenCypher GQL syntax")
        return None
