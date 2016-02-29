'''
Created on 23 feb. 2016

@author: brandtp
'''
import unittest
from EdoalParser.alignment import Alignment, removeWS
from EdoalParser.corresp import Correspondence

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

import json


class Test(unittest.TestCase):


    def setUp(self):        

        # Use of testCases can be useful, but not now
        self.testCases = {}
        self.testCases['CaseName'] = {'pass': 'someName-value-or-datastruct',
                                      'fail': 'someName-value-or-datastruct' }        
        
        # Define some of the generic stuff
        self.ns = json.load(open("../namespaces.json")) 
        with open("testResources/test01/align.xml", 'rt') as f:
            rdf = etree.parse(f)
        self.root = rdf.getroot()
    
#
#
# All Tests
#
#
        
    def testAlignment(self):
        align = Alignment(self.root)
        assert align.xml == 'yes'
        assert align.about == "http://oms.omwg.org/ontoA-ontoB/"
        assert align.creator.text == 'PaulBrandt'
        assert align.date.text == '2015/08/25'
        assert align.method.text == 'manual'
        assert align.purpose.text == 'initial example for a simple Alignment'
        assert align.level == '2EDOAL'
        assert align.type.text == '?*' 
        
        #TODO: Test for equality of ontology elements in Alignment
#         assert align.onto1 == 
#         assert align.onto2 == 
        assert len(align.corresp) == 1
        

    def testCorrespondence(self):
        align = self.root.find('xmlns:Alignment', self.ns)
        element = align.find('xmlns:map/xmlns:Cell', self.ns)
        assert not element == None
        # Create the correspondence from the element
        c = Correspondence(element)
        
        # Fist test: Establish correctness, i.e., all attributes of the Correspondence object
        assert c.about == "MappingRule_0"
        
        ent1 = element.find('xmlns:entity1', self.ns)
        # Remove all the spaces and newlines, and replace for None, otherwise the assertion fails
        ent1 = removeWS(ent1)
        if ent1.text =='' :
            ent1.text = None
        if ent1.tail =='' :
            ent1.tail = None
        assert c.entity1 == ent1
        
        ent2 = element.find('xmlns:entity2', self.ns)
        # Remove all the spaces and newlines, and replace for None, otherwise the assertion fails
        ent2 = removeWS(ent2)
        if ent2.text =='' :
            ent2.text = None
        if ent2.tail =='' :
            ent2.tail = None
        assert c.entity2 == ent2
        
        assert c.relation.text == 'Equivalence'
        assert c.measure.text == '1.0'
        assert not hasattr(c, 'transformation')
        assert not hasattr(c, 'linkkey')
        
        # Second test: must be able to handle None elements
        element = None
        with self.assertRaises(AttributeError):
            d = Correspondence(element)

    def tearDown(self):
        pass
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCorrespondence']
    unittest.main()