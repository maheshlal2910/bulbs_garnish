# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from bulbs.neo4jserver import Graph
from bulbs.config import Config

GRAPH='http://localhost:4747/test_db/data'

def graph_db_path():
    config = Config(GRAPH)
    graph = Graph(config)
    return graph 

