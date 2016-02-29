'''
Created on 22 feb. 2016

@author: brandtp
'''
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import dump
import json
import warnings
import copy

ns = json.load(open("../namespaces.json"))

class E(ET.Element):
    def __init__(self, name):
        super().__init__(name)
    
    def __eq__(self, other):
        if self.tag != other.tag: return False
        if self.text != other.text: return False
        if self.tail != other.tail: return False
        if self.attrib != other.attrib: return False
        if len(self) != len(other): return False
        return all(c1.__eq__(c2) for c1, c2 in zip(self, other))

    def __ne__(self, other):
        return not self.__eq__(other)

class Entity(E):
    '''
    classdocs
    '''
    
    def __init__(self, n, element):
        e = 'entity' + str(n)
        super().__init__('{' + ns["xmlns"] + '}' + e )
        self.append(element.find('xmlns:' + e + '/edoal:Class', ns))
        
class Entity1(Entity):
 
    def __init__(self, element):
        super().__init__(1, element)

 
class Entity2(Entity):
 
    def __init__(self, element):
        super().__init__(2, element)

     
class Relation(E):

    def __init__(self, el):
        '''
        Constructor
        '''
        super().__init__('xmlns:relation')
        self.text = el.find('xmlns:relation', ns).text


class Measure(ET.Element):

    def __init__(self, el):
        '''
        Constructor
        '''
        super().__init__('xmlns:measure')
        self.text = el.find('xmlns:measure', ns).text
        

class Transformation(ET.Element):

    def __init__(self, params):
        '''
        Constructor
        '''


class Linkkey(ET.Element):

    def __init__(self, params):
        '''
        Constructor
        '''

