#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import re

def GpxReader(xmlfile: str, ns={'ns0': 'http://www.topografix.com/GPX/1/1'}, yield_wpt=False):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    count = 0
    for wpt in root.findall('ns0:wpt', ns):
        r = {}

        """ The latitude of the point. Decimal degrees, WGS84 datum. """
        r['latitude'] = wpt.attrib.get('lat')

        """ The longitude of the point. Decimal degrees, WGS84 datum. """
        r['longitude'] = wpt.attrib.get('lon')

        """ The GPS name of the waypoint. This field will be transferred to and from the GPS. GPX does not place restrictions on the length of this field or the characters contained in it. It is up to the receiving application to validate the field before sending it to the GPS. """
        r['name'] = wpt.find('ns0:name',ns).text

        """ Type (classification) of the waypoint. (For OsmAnd, this corresponds to the group.) """
        r['type'] = wpt.find('ns0:type',ns).text

        try:
            """ A text description of the element. Holds additional information about the element intended for the user, not the GPS. """
            r['description'] = wpt.find('ns0:desc',ns).text
        except:
            pass

        try:
            """ GPS waypoint comment. Sent to GPS as comment. """
            r['cmt'] = wpt.find('ns0:cmt',ns).text
        except:
            pass
        if (yield_wpt):
            yield r, wpt
        else:
            yield r

def OsmandFavouritesReader(xmlfile: str, ns={'ns0': 'http://www.topografix.com/GPX/1/1', 'osmand': 'https://osmand.net'}):
    """ Add known fields used by osmand from the 'extensions' node to the dictionary with key 'osmand' """
    for r,wpt in  GpxReader(xmlfile=xmlfile, yield_wpt=True):
        ext = wpt.find('ns0:extensions', ns)
        r['osmand'] = {}
        try:
            r['osmand']['address'] = ext.find('osmand:address', ns).text
        except:
            pass

        try:
            r['osmand']['background'] = ext.find('osmand:background', ns).text
        except:
            pass

        try:
            r['osmand']['icon'] = ext.find('osmand:icon', ns).text
        except:
            pass

        try:
            r['osmand']['color'] = ext.find('osmand:color', ns).text
        except:
            pass

        yield r

def MyFavouritesReader(xmlfile: str):
    for r in OsmandFavouritesReader(xmlfile):
        """ parse 'description' field for iso date strings and add as separate key to dictionary """
        if 'description' in r:
            rx_result = re.search('([0-9]{4}-[0-9]{2}-[0-9]{2})', r['description'])
            if rx_result:
                r['overnight_date'] = rx_result[1] 
        yield r 
