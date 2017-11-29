"""An addon for getting Kodi setup and configured

"""


import xbmc
import xbmcvfs

import sys

from resources.lib import classes, sources, utils, xml_parser


# create the "Kodi Setter Upper" folder in addon_data
if not xbmcvfs.exists(xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper')):
    xbmcvfs.mkdir(xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper'))

# create 'config' folder
if not xbmcvfs.exists(xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/config')):
    xbmcvfs.mkdir(xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/config'))

# create 'keymaps' folder
if not xbmcvfs.exists(xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/keymaps')):
    xbmcvfs.mkdir(xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/keymaps'))
    xbmcvfs.copy(xbmc.translatePath('special://home/addons/script.kodi_setter_upper/keymaps/android_keymap.xml'), xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/keymaps/android_keymap.xml'))
    xbmcvfs.copy(xbmc.translatePath('special://home/addons/script.kodi_setter_upper/keymaps/linux_keymap.xml'), xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/keymaps/linux_keymap.xml'))
    xbmcvfs.copy(xbmc.translatePath('special://home/addons/script.kodi_setter_upper/keymaps/windows_keymap.xml'), xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/keymaps/windows_keymap.xml'))

# create 'scripts' folder
if not xbmcvfs.exists(xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/scripts')):
    xbmcvfs.mkdir(xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/scripts'))

# create 'zips' folder
if not xbmcvfs.exists(xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/zips')):
    xbmcvfs.mkdir(xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/zips'))

# create 'down.py'
if not xbmcvfs.exists(xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/scripts/down.py')):
    with open(xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/scripts/down.py'), 'w') as f:
        f.write('import sys\nimport xbmc\n\nfor i in range(int(sys.argv[1])):\n    xbmc.executebuiltin("Action(Down)")')

# create 'up.py'
if not xbmcvfs.exists(xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/scripts/up.py')):
    with open(xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/scripts/up.py'), 'w') as f:
        f.write('import sys\nimport xbmc\n\nfor i in range(int(sys.argv[1])):\n    xbmc.executebuiltin("Action(Up)")')

# create 'addons.xml'
addons_xml = xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/config/addons.xml')
if not xbmcvfs.exists(addons_xml):
    xbmcvfs.copy(xbmc.translatePath('special://home/addons/script.kodi_setter_upper/config/addons.xml'), addons_xml)

# create 'guisettings.xml'
guisettings_xml = xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/config/guisettings.xml')
if not xbmcvfs.exists(guisettings_xml):
    xbmcvfs.copy(xbmc.translatePath('special://home/addons/script.kodi_setter_upper/config/guisettings.xml'), guisettings_xml)

# create 'skin.xml'
skin_xml = xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/config/skin.xml')
if not xbmcvfs.exists(skin_xml):
    with open(skin_xml, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<skins>\n</skins>')

# create 'sources.xml'
sources_xml = xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/config/sources.xml')
if not xbmcvfs.exists(sources_xml):
    xbmcvfs.copy(xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/config/sources.xml'), sources_xml)


if __name__ == '__main__':
    # perform actions sent via JSON-RPC
    if len(sys.argv) > 1:
        params = {}
        for arg in sys.argv[1:]:
            params[str(arg.split('=')[0])] = str(arg.split('=')[1])
            
        if params.get('ksu_class') == 'Addon' and 'addonid' in params:
            x = classes.Addon(params['addonid'], params.get('zippath'), params.get('repo'))
            if 'id' in params and 'value' in params:
                x.setSetting(params['id'], params['value'])
                
        elif params.get('ksu_class') == 'Skin' and 'addonid' in params:
            x = classes.Skin(params['addonid'], params.get('zippath'), params.get('repo'))
            if 'id' in params and 'value' in params:
                x.setSetting(params['id'], params['value'])
            
        elif params.get('ksu_class') == 'GUI' and 'id' in params and 'value' in params:
            x = classes.GUI(params['id'], params['value'])
            
        elif params.get('ksu_class') == 'Source':
            x = classes.Source(params.get('sourcetype'), params.get('name'), params.get('path'), params.get('allowsharing'), params.get('pathversion'))
            x.insert()
        
    # parse the configuration files
    else:
        sources_xml = xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/config/sources.xml')
        sources.modify(sources_xml)

        # modify GUI settings
        xml_parser.parse(guisettings_xml, classes.GUI)

        # install and configure addons
        xml_parser.parse(addons_xml, classes.Addon)

        # install and configure the skin
        xml_parser.parse(skin_xml, classes.Skin)
        xbmc.executebuiltin("ReloadSkin")

        # create "keymap.xml"
        keymap_xml = xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/keymaps/{0}_keymap.xml'.format(utils.PLATFORM))
        if xbmcvfs.exists(keymap_xml):
            with open(keymap_xml, 'r') as f:
                text = f.read()
            with open(xbmc.translatePath('special://userdata/keymaps/keymap.xml'), 'w') as f:
                f.write(text)
