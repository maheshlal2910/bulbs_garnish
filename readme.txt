This is a simple wrapper over Bulbs - a Python framework for Neo4j.

Using bulbs_granish you can make your models appear more responsible.
Also, there are a few changes to certain methods that Bulbs models provide.

Usage:

1) ActiveModel

Eg. 
@ActiveModel
class SomeModel(Node):
    element_type = 'some_model'

methods added --->

SomeModel.register(graph):
Adds a proxy object to the graph object passed in.

SomeModel.get_or_create(**kwds):
Calls get_or_create in the node_proxy added to the graph with the id field name 
and the id field value.

More examples in the tests.
