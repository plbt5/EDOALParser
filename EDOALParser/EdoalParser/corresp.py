'''
Created on 31 jan. 2016

@author: brandtp

A EdoalParser represents the core of an EDOAL alignment. Refer
to http://alignapi.gforge.inria.fr/edoal.html for its specification.

'''


# from EdoalParser.cellElements import Entity1, Entity2
import json
try:
    from lxml import etree
    print("running with lxml.etree")
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree
        print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree
            print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree
                print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree
                    print("running with ElementTree")
                except ImportError:
                    print("Failed to import ElementTree from any known place")
          

ns = json.load(open("../namespaces.json"))

class Correspondence():
    '''
    The Correspondence class equals an Alignment mapping: <align:map><align:Cell>...</align:Cell></align:map>
    This class can be used to programmatically process the contents of the EDOAL alignment, by addressing its constituent parts as attributes of the class.
    corresp ::= <Cell {rdf:about=" URI "} /> 
                    <entity1> entity </entity1>
                    <entity2> entity </entity2>
                    <relation> STRING </relation>
                    <measure> STRING </measure>
                    (<transformation> transformation </transformation>)*
                    (<linkkey> linkkey </linkkey>)*
                </Cell>
    '''


    def __init__(self, element):
        '''
        Correspondence Constructor
        '''
        if (element == None) or (type(element) != etree.Element):
            raise AttributeError
        else:
            #TODO: Test whether 'element' points to the <map> element in the EDOAL tree
            self.about = element.get('{' + ns['rdf'] + '}about', default='')
            self.entity1 = element.find('xmlns:entity1', ns)
            self.entity2 = element.find('xmlns:entity2', ns)
#             self.entity1 = Entity1(element)
#             self.entity2 = Entity2(element)
            self.relation = element.find('xmlns:relation', ns)
            #TODO: Turn Relation into canonical form
            self.measure = element.find('xmlns:measure', ns)
            if element.find('xmlns:transformation', ns) != None:
                #TODO: Failure to take into account more than one transformations
                self.transformation = element.find('xmlns:transformation', ns)
            if element.find('xmlns:linkkey', ns) != None:
                #TODO: Failure to take into account more than one linkkeys
                self.linkkey = element.find('xmlns:linkkey', ns)
            
    def __eq__(self, other):
        return ((self.about == other.about) and (self.entity1 == other.entity1) and (self.entity2 == other.entity2) and \
                (self.relation == other.relation) and (self.measure == other.measure) and \
                (self.transformation == other.transformation) and (self.linkkey == other.linkkey))
            
    def __ne__(self, other):
        return not self.__eq__(other)