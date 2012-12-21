# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from bulbs.model import Node, Relationship

class IsMirrorRelationshipOf(object):
    
    def __init__(self, relationship):
        self.dual = relationship
    
    def __call__(self, cls):
        setattr(cls, 'dual', self.dual)
        return cls


class HasRelationship(object):
    
    def __init__(self, relationship):
        self.relationship = relationship
    
    def __call__(self, cls):
        relationship, rel_class = self.relationship.items()[0]
        func = self.__create_proxy(relationship, rel_class)
        setattr(cls, relationship.label, func)
        return cls
    
    def __create_proxy(self, relationship, rel_class):
        def proxy_func(self, entity=None):
            assert entity is None or entity.element_type==rel_class
            if entity is None:
                return self.outV(relationship.label)
            rels = self.outV(relationship.label)
            if rels is None or entity not in rels:
                print True
                getattr(self.g,relationship.label).create(self, entity)
                if 'dual' in dir(relationship):
                    getattr(entity, relationship.dual)(self)
        return proxy_func


def ActiveModel(cls):
    def register(self, graph):
        if('element_type' in dir(cls)):
            graph.add_proxy(cls.element_type, cls)
        if('label' in dir(cls)):
            graph.add_proxy(cls.label, cls)
        cls.g = graph
    setattr(cls, 'register', classmethod(register))
    if('element_type' in dir(cls)):
        def get_or_create(cls, **kwds):
            key = cls.document_primaries[0]
            print key
            val = kwds[key]
            return getattr(cls.g,cls.element_type).get_or_create(key, val, **kwds)
        setattr(cls, 'get_or_create', classmethod(get_or_create))
        def get_unique(cls, **kwds):
            return getattr(cls.g,cls.element_type).index.get_unique(**kwds)
        setattr(cls, 'get_unique', classmethod(get_unique))
        
        def update(self, **val):
            for attribute in val:
                if attribute in dir(self):
                    setattr(self, attribute, val[attribute]) 
            self.save()
            return self
        setattr(cls, 'update', update)
    return cls
