import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

####################################################################################
# 1. Explore all the tags in this sample file.
##   Print out all different tags and count the number of each tag
def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename):
        if elem.tag in tags:
            tags[elem.tag] += 1
        else:
            tags[elem.tag] = 1
    return tags

tags = count_tags('sample.osm')
pprint.pprint(tags)


####################################################################################
# 2. Explore the 'k' value of the all the tags in 'way' element
##   Print out the 'k' value of tag and count them

def print_all_way_tag (filename):
    tag_k = {}
    for event, elem in ET.iterparse(filename):
        if (elem.tag == 'way'):
            for tag in elem.iter('tag'):
                temp = tag.attrib['k']
                if temp in tag_k.keys():
                    tag_k[temp] += 1
                else:
                    tag_k[temp] = 1
    return tag_k

tags_k = print_all_way_tag ('sample.osm')
pprint.pprint(tags_k)

####################################################################################
# 3. Audit addr:street names for element in 'way'

osm_file = open("sample.osm","rb")
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_types = defaultdict(set)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road","Trail", "Parkway"]

def audit_street_type (street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name (elem):
    return (elem.attrib['k'] == "addr:street")

def audit():
    for event, elem in ET.iterparse(osm_file, events = ("start",)):
        if (elem.tag == "way"):
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    pprint.pprint(dict(street_types))

if __name__ == '__main__':
    audit()

####################################################################################
# 4. Audit addr:postcode for element in 'way'
osm_file = open("sample.osm","rb")
zip_code = {}

def audit_zip_code (zip_code, zip):
    if zip in zip_code.keys():
        zip_code[zip] += 1
    else:
        zip_code[zip] = 1

def print_sorted_zipcode (d):
    keys = d.keys()
    keys = sorted(keys, key = lambda x: int(x))
    for k in keys:
        v = d[k]
        print ("%s: %d" % (k,v))

def is_zip_code (elem):
    return (elem.attrib["k"] == "addr:postcode")

def audit():
    for event, elem in ET.iterparse(osm_file):
        if (elem.tag == "way"):
            for tag in elem.iter("tag"):
                if is_zip_code(tag):
                    audit_zip_code(zip_code, tag.attrib["v"])
    print_sorted_zipcode(zip_code)
    #print(*zip_code, sep='\n')

if __name__ == '__main__':
    audit()
####################################################################################
