'''
Created on 26 feb. 2016

@author: brandtp
'''
import json
from EdoalParser.corresp import Correspondence

try:
    from lxml import ET
    print("running with lxml.etree")
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as ET
        print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as ET
            print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as ET
                print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as ET
                    print("running with ElementTree")
                except ImportError:
                    print("Failed to import ElementTree from any known place")
          

from xml.etree.ElementTree import dump
ns = json.load(open("../namespaces.json"))


def removeWS(el):
    '''
    Tooling function to remove whitespaces from xml-etree elements
    '''
    t=''.join(el.text.splitlines())
    el.text = ''.join(t.split())
    t=''.join(el.tail.splitlines())
    el.tail = ''.join(t.split())
    return el
    

class Alignment(object):
    '''
    Represents the parsed EDOAL Alignment. Each first level XML element is represented as an attribute, as follows:
        self.xml     ::== string
        self.about   ::== string
        self.creator ::== xml.etree.Element
        self.date    ::== xml.etree.Element
        self.method  ::== xml.etree.Element
        self.purpose ::== xml.etree.Element
        self.level   ::== string
        self.type    ::== xml.etree.Element
        self.onto1   ::== xml.etree.Element
        self.onto2   ::== xml.etree.Element
        self.corresp ::== List of xml.etree.Element

    <Alignment rdf:about="http://oms.omwg.org/ontoA-ontoB/">
        <xml>yes</xml>
        <dc:creator>PaulBrandt</dc:creator>
        <dc:date>2015/08/25</dc:date>
        <method>manual</method>
        <purpose>initial example for a simple Alignment</purpose>
        <level>2EDOAL</level>
        <type>?*</type>
        <onto1>...</onto1> 
        <onto2>...</onto2>
        (<map>...</map>)*
    </Alignment>
    '''


    def __init__(self, el):
        '''
        Constructor
        '''
        #TODO: Consider other EDOAL levels than 2EDOAL only
        #TODO: Consider other alignments than EDOAL only, e.g., SPIN
        if el == None or type(el) != ET.Element:
            raise AttributeError
        else:
            align = el.find('xmlns:Alignment', ns)
            t = align.get('{' + ns['rdf'] + '}about', default='')
            if t == '' or t == None: raise AttributeError
            if align.find('xmlns:xml', ns).text != 'yes' or align.find('xmlns:level', ns).text != '2EDOAL': raise AttributeError
            self.xml = 'yes'
            self.about = t
            self.creator = align.find('dc:creator', ns)
            self.date = align.find('dc:date', ns)
            self.method = align.find('xmlns:method', ns)
            self.purpose = align.find('xmlns:purpose', ns)
            self.level = '2EDOAL'
            self.type = align.find('xmlns:type', ns)
            self.onto1 = align.find('xmlns:onto1', ns)
            self.onto2 = align.find('xmlns:onto2', ns)
            self.corresp = []
            for t in align.findall('xmlns:map/xmlns:Cell', ns):
                self.corresp.append(Correspondence(t))
            if len(self.corresp) == 0: raise AttributeError('No mappings found in Alignment' + self.about)

    def __eq__(self, other):
        return ((self.about == other.about) and (self.xml == other.xml) and (self.creator == other.creator) and \
                (self.date == other.date) and (self.method == other.method) and (self.purpose == other.purpose) and \
                (self.level == other.level) and (self.type == other.type) and \
                (self.onto1 == other.onto1) and (self.onto2 == other.onto2) and \
                (all(c1 == c2) for c1, c2 in zip(self.corresp, other.corresp)) )
            
    def __ne__(self, other):
        return not self.__eq__(other)



