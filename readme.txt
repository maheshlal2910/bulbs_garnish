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

SomeModel.get_unique(params):
Gets unique objects matching the said criteria using the underlying Bulbs API

model_instance.update(**kwds):
Update the instance with the supplied values and save it


2) HasRelationship

Eg.

@HasRelationship({SomeRelationship: 'some_model'})
@ActiveModel
class AnotherModel(Node):
    element_type = 'another_model'

Note---> 
*'some_model' is the element_name of SomeModel
* SomeRelationship will be a valid relationship which will be annotated by activemodel

methods added --->

another_model_instance.some_relationship(node = None)
Returns all the nodes this node has 'some_relationship' with if node = None.
Else creates 'some_relationship' between another_model_instance and node.

Note: 'some_relationship' is the label of SomeRelationship


More examples in the tests.
