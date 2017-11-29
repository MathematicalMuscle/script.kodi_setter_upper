"""Install and configure addons

"""


import xml.etree.ElementTree as ET


def parse(xml_path, ksu_class):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    xml_items = [(item.attrib, [(setting.attrib['id'], setting.attrib['value']) for setting in item]) for item in root]

    for item in xml_items:
        x = ksu_class(**item[0])

        for id, value in item[1]:
            x.setSetting(id, value)
