# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from bulbs.neo4jserver import Graph, Config
from bulbs.config import DEBUG

GRAPH='http://localhost:4747/db/data'

def graph_db_path():
    config = Config(GRAPH)
    graph = Graph(config)
    return graph 

