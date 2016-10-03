import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import json

####################################################################################
# 1. Explore all the tags start with "Tiger:" in 'way' element.

osm_file = open("sample.osm","rb")
tiger_tag_re = re.compile(r'^Tiger', re.IGNORECASE)
tiger_tag_types = defaultdict(set)

def audit_tiger_tag (tiger_tag_types, tag_type, tag_value):
    tiger_tag_types[tag_type].add(tag_value)


def is_tiger_tag (elem):
    return (tiger_tag_re.search(elem.attrib['k']))

def audit():
    for event, elem in ET.iterparse(osm_file, events = ("start",)):
        if (elem.tag == "way"):
            for tag in elem.iter("tag"):
                if is_tiger_tag(tag):
                    audit_tiger_tag(tiger_tag_types, tag.attrib['k'], tag.attrib['v'])
    pprint.pprint(dict(tiger_tag_types))

if __name__ == '__main__':
    audit()
