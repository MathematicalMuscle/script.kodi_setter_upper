"""An addon for getting Kodi setup and configured

"""


import xbmc
import xbmcgui
import xbmcvfs

import os
import sys

from resources.lib import classes, sources, utils, xml_parser, get_local_ip_address


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

# create 'advancedsettings.xml'
advancedsettings_xml = xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/config/advancedsettings.xml')
if not xbmcvfs.exists(advancedsettings_xml):
    xbmcvfs.copy(xbmc.translatePath('special://home/addons/script.kodi_setter_upper/config/advancedsettings.xml'), advancedsettings_xml)

# create 'guisettings.xml'
guisettings_xml = xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/config/guisettings.xml')
if not xbmcvfs.exists(guisettings_xml):
    xbmcvfs.copy(xbmc.translatePath('special://home/addons/script.kodi_setter_upper/config/guisettings.xml'), guisettings_xml)

# create 'skin.xml'
skin_xml = xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/config/skin.xml')
if not xbmcvfs.exists(skin_xml):
    xbmcvfs.copy(xbmc.translatePath('special://home/addons/script.kodi_setter_upper/config/skin.xml'), skin_xml)

# create 'sources.xml'
sources_xml = xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/config/sources.xml')
if not xbmcvfs.exists(sources_xml):
    xbmcvfs.copy(xbmc.translatePath('special://home/addons/script.kodi_setter_upper/config/sources.xml'), sources_xml)
    
config_dir = xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/config/')


if __name__ == '__main__':
    # perform actions sent via JSON-RPC
    if len(sys.argv) > 1:
        params = {}
        for arg in sys.argv[1:]:
            params[str(arg.split('=')[0])] = str(arg.split('=', 1)[1])
            
        if params.get('ksu_class') == 'Addon' and 'addonid' in params:
            x = classes.Addon(params['addonid'], params.get('zippath'), params.get('repo'), params.get('url'), params.get('uninstall'), params.get('disable'))
            if 'id' in params and 'value' in params:
                x.setSetting(params['id'], params['value'])
                
        elif params.get('ksu_class') == 'Skin' and 'addonid' in params:
            x = classes.Skin(params['addonid'], params.get('zippath'), params.get('repo'), params.get('url'), params.get('uninstall'), params.get('disable'))
            if 'id' in params and 'value' in params:
                x.setSetting(params['id'], params['value'])
            
        elif params.get('ksu_class') == 'GUI' and 'id' in params and 'value' in params:
            x = classes.GUI(params['id'], params['value'])
            
        elif params.get('ksu_class') == 'Source':
            x = classes.Source(params.get('sourcetype'), params.get('name'), params.get('path'), params.get('allowsharing'), params.get('pathversion'))
            x.insert()
            
        elif params.get('ksu_class') == 'Download':
            x = classes.Download(params.get('url'), params.get('dest'), params.get('no_dialog'))

        elif params.get('ksu_class') == 'AdvancedSetting':
            if 'id' in params and 'value' in params:
                x = classes.AdvancedSetting(params.get('id'), params.get('value'))
        
    # parse the configuration files
    else:
        opts = ["Apply 'addons.xml' settings",
                "Apply 'advancedsettings.xml' settings",
                "Apply 'guisettings.xml' settings",
                "Apply 'skin.xml' settings",
                "Get local IP address",
                "Load 'keymap.xml' keymaps",
                "Load 'sources.xml' sources",
                "View a text file"]

        select = xbmcgui.Dialog().select('Kodi Setter-Upper', opts, 0)
        if select >= 0:
            selection = opts[select]
            
            if selection == "Apply 'addons.xml' settings":
                addons_xml = xbmcgui.Dialog().browse(1, 'Kodi Setter-Upper', 'files', mask='.xml', defaultt=config_dir)
                if os.path.isfile(addons_xml):
                    xml_parser.parse(addons_xml, classes.Addon)
                
            elif selection == "Apply 'advancedsettings.xml' settings":
                advancedsettings_xml = xbmcgui.Dialog().browse(1, 'Kodi Setter-Upper', 'files', mask='.xml', defaultt=config_dir)
                if os.path.isfile(advancedsettings_xml):
                    xml_parser.parse(advancedsettings_xml, classes.AdvancedSetting)
                
            elif selection == "Apply 'guisettings.xml' settings":
                guisettings_xml = xbmcgui.Dialog().browse(1, 'Kodi Setter-Upper', 'files', mask='.xml', defaultt=config_dir)
                if os.path.isfile(guisettings_xml):
                    xml_parser.parse(guisettings_xml, classes.GUI)
                
            elif selection == "Apply 'skin.xml' settings":
                skin_xml = xbmcgui.Dialog().browse(1, 'Kodi Setter-Upper', 'files', mask='.xml', defaultt=config_dir)
                if os.path.isfile(skin_xml):
                    xml_parser.parse(skin_xml, classes.Skin)
                
            elif selection == "Get local IP address":
                local_ip_address = get_local_ip_address.get_local_ip_address()
                xbmcgui.Dialog().ok('Local IP Address', local_ip_address)
                
            elif selection == "Load 'keymap.xml' keymaps":
                keymap_xml = xbmcgui.Dialog().browse(1, 'Kodi Setter-Upper', 'files', mask='.xml', defaultt=xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/keymaps/'))
                if os.path.isfile(keymap_xml):
                    with open(keymap_xml, 'r') as f:
                        text = f.read()
                    with open(xbmc.translatePath('special://userdata/keymaps/keymap.xml'), 'w') as f:
                        f.write(text)
                
            elif selection == "Load 'sources.xml' sources":
                sources_xml = xbmcgui.Dialog().browse(1, 'Kodi Setter-Upper', 'files', mask='.xml', defaultt=config_dir)
                if os.path.isfile(sources_xml):
                    sources.modify(sources_xml)

            elif selection == "View a text file":
                textfile = xbmcgui.Dialog().browse(1, 'Kodi Setter-Upper', 'files', defaultt=xbmc.translatePath('special://home'))
                if os.path.isfile(textfile):
                    with open(textfile, 'r') as f:
                        text = f.read()
                    xbmcgui.Dialog().textviewer(os.path.basename(textfile), text)

