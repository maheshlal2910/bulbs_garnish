# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from bulbs.model import Node, Relationship
from bulbs.property import String


class Node(Node):
    document_primaries= ['model_id']
    model_id = String(nullable = False)


class Relationship(Relationship):
    pass
