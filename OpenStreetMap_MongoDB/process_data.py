#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

OSMFILE = "brooklyn.osm"
# List of validate street names
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Crescent", "Expressway", "Highway", "Loop", "Plaza"
            "Row", "Terrace", "Walk", "Turnpike", "Tunnel"]

# Mapping of abbreviated street names to validate ones
mapping = { "St": "Street", "St.": "Street", "Blvd": "Boulevard", "Pl": "Place", "Brg": "Bridge", "Cres": "Crescent",
            "Ct": "Court", "Dr": "Drive", "Expy": "Expressway", "Hwy": "Highway", "Ln": "Lane", "Pky": "Parkway",
            "Plz": "Plaza", "Rd": "Road", "Sq": "Square", "Ter": "Terrace", "Tpke": "Turnpike", "Tunl": "Tunnel",
            "Ave": "Avenue"}



# Validate the name_type for tiger
def is_valid_name_type (elem, value):
    return (elem.startswith("name_type") and (":" not in value))

# Update street names
def update_street_name(name, mapping):
    street_type = name.rsplit(' ',1)[-1]
    if street_type in mapping.keys():
        temp_name = name.rsplit(' ',1)[-2]
        street_type = mapping[street_type]
        name = ' '.join([temp_name, street_type])
    return name

# Update tiger street name type
def update_tiger(name, mapping):
    name = name.rsplit(';')
    for i in range(len(name)):
        count = 0
        if name[i] in list(mapping.keys()):
            name[i] = mapping[name[i]]
    name = ";".join(name)
    return name

# Updatae invalid zip code
valid_postcode = re.compile(r'^[0-9]{5}(?:-[0-9]{4})?$')
def update_postcode (zip):
    if (valid_postcode.match(zip)):
        return (zip)
    else:
        return ("Need_to_be_fixed")

# Save those tags json file for MongoDB database
problemchars = re.compile(r'[=\+/&<>\'"\?%#$@\,\. \t\r\n]')


CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def shape_element(elem):
    node = {}
    node['created'] = {}
    node['pos'] = [0,0]

    if elem.tag == 'node' or elem.tag == 'way':
        node['type'] = elem.tag
        for k, v in elem.attrib.items():
            # Attributes in the CREATED array
            if k in CREATED:
                node['created'][k] = v
            # Attributes of latitude & longitude
            elif k == 'lat':
                try:
                    lat = float(v)
                    node['pos'][0] = lat
                except ValueError:
                    pass
            elif k == 'lon':
                try:
                    lon = float(v)
                    node['pos'][1] = lon
                except ValueError:
                    pass
            else:
                node[k] = v

        # Second level tag
        for tag in elem.iter('tag'):
            key = tag.attrib['k']
            val = tag.attrib['v']
            if (not problemchars.search(key)) and (key.startswith('addr:')):
                if 'address' not in node:
                    node['address'] = {}
                else:
                    name = key[5:]
                    if ':' not in name:
                        if name == 'street':
                            val = update_street_name(val, mapping)
                        elif name == 'postcode':
                            val = update_postcode(val)
                        node['address'][name] = val

            elif (not problemchars.search(key)) and (key.startswith('tiger:')):
                if 'tiger' not in node:
                    node['tiger'] = {}
                else:
                    name = key[6:]
                    if is_valid_name_type(name, val):
                        val = update_tiger(val, mapping)

                    node['tiger'][name] = val
            else:
                if not problemchars.search(key):
                    node[key] = val

        if elem.tag == "way":
            node['node_refs'] = []
            for n in elem.iter('nd'):
                ref = n.attrib['ref']
                node['node_refs'].append(ref)

        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

process_map(OSMFILE, False)
