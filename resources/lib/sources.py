"""Add to the `sources.xml` file

"""

import os
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

import xml.etree.ElementTree as ET

PY2 = sys.version_info[0] == 2

if not PY2:
    from .dialogger import dialogger
else:
    from dialogger import dialogger


def modify(sources_xml):
    """Insert the "files" sources from `sources_xml` into Kodi's "sources.xml" file

    """
    # the new `sources_xml` file
    sources_xml = xbmc.translatePath(sources_xml)
    if not xbmcvfs.exists(sources_xml):
        return
    
    tree2 = ET.parse(xbmc.translatePath(sources_xml))
    root2 = tree2.getroot()
    files2 = root2.find('files')

    write_sources = False

    # Kodi's "sources.xml" file
    kodi_sources_xml = xbmc.translatePath('special://home/userdata/sources.xml')
    if xbmcvfs.exists(kodi_sources_xml):
        tree = ET.parse(kodi_sources_xml)
        root = tree.getroot()
        files = root.find('files')

        with open(kodi_sources_xml, 'r') as f:
            text = f.read()

        for f in files2:
            for ff in f:
                if ff.tag == 'path':
                    if ff.text not in text:
                        write_sources = True
                        files.insert(-1, f)

    else:
        dialogger("`userdata/sources.xml` does not exist")
        write_sources = True
        root = ET.Element('sources')
        root.insert(0, root2.find('files'))
        tree = ET.ElementTree(root)

    if write_sources:
        dialogger("Writing `userdata/sources.xml`")
        tree.write(kodi_sources_xml, encoding='UTF-8')
        strip_xml_declaration(kodi_sources_xml)
        
        with open(kodi_sources_xml, 'r+') as f:
            lines = f.read().splitlines(True)
            f.seek(0)

            # declaration exists --> omit it
            if lines[0].startswith('<?'):
                f.writelines(lines[1:])
                f.truncate()
            
    else:
        dialogger("No changes to `userdata/sources.xml`")
