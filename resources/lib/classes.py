"""`Addon` and `Skin` classes

"""


import os
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

import datetime
import shutil
from sqlite3 import dbapi2
import xml.etree.ElementTree as ET
import zipfile

from dialogger import dialogger


dummy_addon_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
dummy_addon_xml += ''
dummy_addon_xml += '<addon id="{0}" name="{0}" version="0.0.0" provider-name="Mathematical Muscle">'
dummy_addon_xml += '    <requires>'
dummy_addon_xml += '        <import addon="xbmc.python" version="2.14.0"/>'
dummy_addon_xml += '    </requires>'
dummy_addon_xml += '    <extension point="xbmc.python.script" library="addon.py">'
dummy_addon_xml += '    </extension>'
dummy_addon_xml += '    <extension point="xbmc.addon.metadata">'
dummy_addon_xml += '        <platform>all</platform>'
dummy_addon_xml += '        <summary lang="en">Placeholder</summary>'
dummy_addon_xml += '        <description lang="en">Placeholder</description>'
dummy_addon_xml += '        <language>en</language>'
dummy_addon_xml += '    </extension>'
dummy_addon_xml += '</addon>'


class Addon(object):
    def __init__(self, addonid, zippath=None, repo=None, uninstall=None):
        self.addonid = addonid
        self.zippath = zippath
        self.repo = repo

        self.enabled = self._isenabled()
        self.installed = True if self.enabled else self._isinstalled()

        if uninstall is None:
            self.install()
        else:
            self.uninstall()

    def setSetting(self, id, value):
        if self.installed:
            xbmcaddon.Addon(self.addonid).setSetting(id, value)

    def getSetting(self, id):
        if self.installed:
            return xbmcaddon.Addon(self.addonid).getSetting(id)

    def install(self):
        if self.enabled:
            return

        elif self.installed:
            self._enable()
            return

        elif xbmcvfs.exists(xbmc.translatePath('special://home/addons/{0}/addon.xml'.format(self.addonid))):
            self._add_to_database()

        elif self.repo is not None and Addon(self.repo).enabled:
            if not xbmcvfs.exists(xbmc.translatePath('special://home/addons/{0}'.format(self.addonid))):
                xbmcvfs.mkdir(xbmc.translatePath('special://home/addons/{0}'.format(self.addonid)))

            with open(xbmc.translatePath('special://home/addons/{0}/addon.xml'.format(self.addonid)), 'w') as f:
                f.write(dummy_addon_xml.format(self.addonid))

            self._add_to_database()
            xbmc.executebuiltin('UpdateAddonRepos')

        elif self.zippath is not None and xbmcvfs.exists(xbmc.translatePath(self.zippath)):
            z_in = zipfile.ZipFile(xbmc.translatePath(self.zippath), 'r')
            z_out = xbmc.translatePath('special://home/addons')
            z_in.extractall(z_out)
            self._add_to_database()

    def _isenabled(self):
        enabled_addons = eval(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Addons.GetAddons", "params": {"enabled": true}, "id": 1}'))['result']
        enabled_addons = [x['addonid'] for x in enabled_addons['addons']]
        return self.addonid in enabled_addons

    def _isinstalled(self):
        all_addons = eval(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Addons.GetAddons", "id": 1}'))['result']
        all_addons = [x['addonid'] for x in all_addons['addons']]
        return self.addonid in all_addons

    def _enable(self):
        xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Addons.SetAddonEnabled", "params": {"addonid": "' + self.addonid + '", "enabled": true}, "id": 1}')
        self.enabled = True

    def _add_to_database(self):
        conn = dbapi2.connect(xbmc.translatePath('special://profile/Database/Addons27.db'))
        conn.text_factory = str

        now = datetime.datetime.now()
        date_time = str(now).split('.')[0]
        sql = 'REPLACE INTO installed (addonID,enabled,installDate) VALUES(?,?,?)'
        conn.execute(sql, (self.addonid, 1, date_time))
        conn.commit()
        xbmc.executebuiltin('XBMC.UpdateLocalAddons()')

        self.enabled = True
        self.installed = True
        
    def uninstall(self):
        if self.installed:
            if xbmcvfs.exists(xbmc.translatePath('special://home/addons/{0}/'.format(self.addonid))):
                xbmcgui.Dialog().ok('KSU', "rmtree")
                shutil.rmtree(xbmc.translatePath('special://home/addons/{0}/'.format(self.addonid)), ignore_errors=True)
            xbmc.executebuiltin('XBMC.UpdateLocalAddons()')
            self.enabled = False
            self.installed = False


class Skin(Addon):
    def __init__(self, addonid, zippath=None, repo=None, uninstall=None):
        self.addonid = addonid
        self.zippath = zippath
        self.repo = repo

        self.enabled = self._isenabled()
        self.installed = True if self.enabled else self._isinstalled()

        if uninstall is None:
            self.install()
            if not self.iscurrent():
                self.set_as_current()
        else:
            if not self.iscurrent():
                self.uninstall()

    def iscurrent(self):
        return xbmc.translatePath('special://skin').strip(os.sep).split(os.sep)[-1] == self.addonid

    def set_as_current(self):
        if self.installed:
            xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.SetSettingValue","id":1,"params":{"setting":"lookandfeel.skin","value":"' + self.addonid + '"}}')

    def setSetting(self, id, value):
        if self.iscurrent():
            if value in ['True', 'False']:
                xbmc.executebuiltin("Skin.SetBool({0}, {1})".format(id, value))
            else:
                xbmc.executebuiltin("Skin.SetString({0}, {1})".format(id, value))

    #def getSetting(self, id):
    #    return xbmcaddon.Addon(self.addonid).getSetting(id)


class GUI(object):
    def __init__(self, id, value):
        if value in ['true', 'false'] or value.isdigit():
            xbmc.executeJSONRPC('{"jsonrpc":"2.0", "id":1, "method":"Settings.SetSettingValue","params":{"setting":"' + id + '","value":' + value + '}}')
        else:
            xbmc.executeJSONRPC('{"jsonrpc":"2.0", "id":1, "method":"Settings.SetSettingValue","params":{"setting":"' + id + '","value":"' + value + '"}}')
            

class Source(object):
    def __init__(self, sourcetype=None, name=None, path=None, allowsharing='true', pathversion="1"):
        # handle missing inputs
        if allowsharing is None:
            allowsharing = 'true'
        if pathversion is None:
            pathversion = "1"
            
        self.sourcetype = sourcetype
        self.name = name
        self.path = path
        self.element = ET.Element('source')
        
        _name = ET.Element('name')
        _name.text = name
        _path = ET.Element('path', attrib={'pathversion': pathversion})
        _path.text = path
        _allowsharing = ET.Element('allowsharing')
        _allowsharing.text = allowsharing
        
        self.element.insert(0, _name)
        self.element.insert(1, _path)
        self.element.insert(2, _allowsharing)
        
    def insert(self):
        if None not in [self.sourcetype, self.name, self.path]:
            # Kodi's "sources.xml" file
            kodi_sources_xml = xbmc.translatePath('special://home/userdata/sources.xml')
            if not xbmcvfs.exists(kodi_sources_xml):
                xbmcgui.Dialog().ok("Kodi Setter-Upper", "`userdata/sources.xml` does not exist")
            
            else:
                tree = ET.parse(kodi_sources_xml)
                root = tree.getroot()
                branch = root.find(self.sourcetype)
                
                if self.path not in [s.text for source in branch for s in source if s.tag == 'path']:
                    branch.insert(-1, self.element)
                    
                    dialogger("Writing `userdata/sources.xml`")
                    tree.write(kodi_sources_xml, encoding='UTF-8')
                    
                    with open(kodi_sources_xml, 'r+') as f:
                        lines = f.read().splitlines(True)
                        f.seek(0)

                        # declaration exists --> omit it
                        if lines[0].startswith('<?'):
                            f.writelines(lines[1:])
                            f.truncate()
                            
                else:
                    dialogger("No changes to `userdata/sources.xml`")
