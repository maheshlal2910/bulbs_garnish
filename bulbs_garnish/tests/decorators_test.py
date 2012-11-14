# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

import unittest
from bulbs.model import Node, Relationship
from bulbs.property import String, Integer
from config import graph_db_path

from bulbs_garnish.bulbs_garnish.decorators import *

@IsMirrorRelationshipOf("knows")
@ActiveModel
class Knows(Relationship):
    label='knows'


@ActiveModel
class ParentOf(Relationship):
    label="parent_of"


@ActiveModel
class Unknown(Node):
    element_type='unknown'


@HasRelationship({ParentOf:'user'})
@HasRelationship({Knows:'user'})
@ActiveModel
class User(Node):
    element_type='user'
    username = String(nullable=False)
    age= Integer()
    document_primaries=['username']


class ActiveModelTests(unittest.TestCase):
    
    def setUp(self):
        self.g = graph_db_path()
        User.register(self.g)

    def test_ActiveModel_should_add_register_method_to_model(self):
        self.assertTrue('register' in dir(User))

    def test_ActiveModel_should_add_proxy_for_that_model(self):
        self.assertTrue('user' in dir(self.g))

    def test_ActiveModel_should_add_graph_to_model(self):
        self.assertTrue('g' in dir(User))
        self.assertTrue( User.g == self.g)
    
    def test_ActiveModel_should_honor_relationships_and_nodes_alike(self):
        self.assertTrue('register' in dir(Knows))
        self.assertTrue('register' in dir(User))
    
    def test_ActiveModel_should_allow_get_or_create_for_Nodes(self):
        self.assertTrue('get_or_create' in dir(User))
    
    def test_ActiveModel_should_NOT_allow_get_or_create_for_Relationships(self):
        self.assertTrue('get_or_create' not in dir(Knows))
    
    def test_ActiveModel_get_or_create_should_return_existing_node(self):
        expected_user = self.g.user.create(username="user2")
        retreived_user = User.get_or_create(username="user2")
        self.assertTrue(expected_user == retreived_user)
    
    def test_ActiveModel_get_or_create_should_create_new_node(self):
        user = User.get_or_create(username="user1")
        self.assertIsNot(user, None)
        self.assertEquals(user.username, "user1")
    
    def test_ActiveModel_should_allow_get_unique_on_nodes(self):
        self.assertTrue('get_unique' in dir(User))
    
    def test_ActiveModel_should_NOT_allow_get_unique_on_relationships(self):
        self.assertTrue('get_unique' not in dir(Knows))
    
    def test_ActiveModel_get_unique_should_return_existing_node(self):
        expected_user = self.g.user.create(username="user2")
        retreived_user = User.get_unique(username="user2")
        self.assertTrue(expected_user == retreived_user)
    
    def test_ActiveModel_get_unique_should_return_none_if_nothing_found(self):
        self.assertIsNone(User.get_unique(username="user2"))
    
    def test_ActiveModel_should_add_method_update(self):
        self.assertTrue('update' in dir(User))
    
    def test_ActiveModel_update_should_update_the_object_with_said_values(self):
        user = self.g.user.create(username="user2")
        user.update(age=27)
        user = self.g.user.get(user._id)
        self.assertEquals(27, user.age)
    
    def test_ActiveModel_get_or_create_should_create_new_node_with_dict(self):
        user_id = dict(username='johndoe')
        user = User.get_or_create(**user_id)
        self.assertEquals('johndoe', user.username)
    
    def tearDown(self):
        self.g.clear()


class HasRelationshipTest(unittest.TestCase):

    def setUp(self):
        self.g = graph_db_path()
        ParentOf.register(self.g)
        User.register(self.g)
        Knows.register(self.g)
        Unknown.register(self.g)
        self.g.add_proxy('knows', Knows)
        self.user = self.g.user.create(username='user1')
        self.known_user = self.g.user.create(username='user2')
    
    def test_has_relationship_adds_the_method_provided(self):
        self.assertTrue('knows' in dir(self.user))
    
    def test_the_method_saves_relationship_to_another_object_if_provided(self):
        user_3 = User.get_or_create(username='user3')
        self.user.knows(user_3)
        self.assertTrue(user_3 in self.user.outV('knows'))
    
    def test_the_method_accepts_None(self):
        self.assertTrue(self.user.knows() is None)
        self.user.knows(self.known_user)
        self.assertTrue(self.user.knows() is not None)
    
    def test_throws_error_if_unsupported_type_supplied(self):
        unknown = self.g.unknown.create()
        with self.assertRaises(AssertionError):
            self.user.knows(unknown)
    
    def test_shouldnt_add_relationship_if_already_exists(self):
        self.user.knows(self.known_user)
        count_of_known_people = sum(1 for user in self.user.knows())
        self.assertEquals(count_of_known_people, 1)
    
    def test_should_add_relationship_if_none_exists_previously(self):
        self.known_user.knows(self.user)
        self.assertTrue(self.user in self.known_user.outV('knows'))
    
    def test_should_add_the_dual_relation_in_case_dual_is_defined(self):
        self.user.knows(self.known_user)
        self.assertTrue(self.known_user in self.user.knows())
        self.assertTrue(self.user in self.known_user.knows())
    
    def test_shouldnt_add_dual_to_relationships_which_arent_dual(self):
        self.user.parent_of(self.known_user)
        self.assertTrue(self.known_user.parent_of() is None)
    
    def tearDown(self):
        self.g.clear()

class IsMirrorRelationshipOfTest(unittest.TestCase):
    
    def setUp(self):
        self.g = graph_db_path()
        self.g.add_proxy('knows', Knows)
        self.g.add_proxy('user', User)
        self.user = self.g.user.create(username='user1')
    
    def test_should_add_dual_in_class(self):
        self.assertEquals(Knows.dual, 'knows')
    
    def tearDown(self):
        self.g.clear()


