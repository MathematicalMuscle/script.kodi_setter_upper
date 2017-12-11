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
import urllib
import xml.etree.ElementTree as ET
import zipfile

from dialogger import dialogger


dummy_addon_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
dummy_addon_xml += '<addon id="{0}" name="{0}" version="0.0.0" provider-name="Mathematical Muscle">\n'
dummy_addon_xml += '    <requires>\n'
dummy_addon_xml += '        <import addon="xbmc.python" version="2.14.0"/>\n'
dummy_addon_xml += '    </requires>\n'
dummy_addon_xml += '    <extension point="xbmc.python.script" library="addon.py">\n'
dummy_addon_xml += '    </extension>\n'
dummy_addon_xml += '    <extension point="xbmc.addon.metadata">\n'
dummy_addon_xml += '        <platform>all</platform>\n'
dummy_addon_xml += '        <summary lang="en">Placeholder</summary>\n'
dummy_addon_xml += '        <description lang="en">Placeholder</description>\n'
dummy_addon_xml += '        <language>en</language>\n'
dummy_addon_xml += '    </extension>\n'
dummy_addon_xml += '</addon>'


class Addon(object):
    def __init__(self, addonid, zippath=None, repo=None, url=None, uninstall=None, disable=None):
        self.addonid = addonid
        self.zippath = zippath
        self.repo = repo
        self.url = url
        
        self.dependencies = None
        
        if self.addonid in ['xbmc.python', 'repository.xbmc.org', 'xbmc.gui']:
            self.enabled = True
            self.installed = True
            
        else:
            if self.exists:
                self.enabled = self._isenabled()
                self.installed = True if self.enabled else self._isinstalled()
            else:
                self.enabled = False
                self.installed = False

            # if it's not already installed and it's not supposed to be uninstalled, then install it
            if uninstall is None:
                self.install()
                
                # if it's supposed to be disabled, then disable it
                if disable is not None:
                    self._disable()
            else:
                # if it's supposed to be uninstalled, then uninstall it
                self.uninstall()
    
    @property
    def exists(self):
        return xbmcvfs.exists(xbmc.translatePath('special://home/addons/{0}/addon.xml'.format(self.addonid))) or self.addonid == 'xbmc.python'
        
    @property
    def meets_dependencies(self):
        self._get_dependencies()
        return self.dependencies is not None and all([Addon(a).installed for a in self.dependencies]) # and all([Addon(a).getVersion() != '0.0.0' for a in self.dependencies])

    def setSetting(self, id, value):
        if self.enabled:
            xbmcaddon.Addon(self.addonid).setSetting(id, value)

    def getSetting(self, id):
        if self.enabled:
            return xbmcaddon.Addon(self.addonid).getSetting(id)
            
    def getVersion(self):
        if self.enabled:
            return xbmcaddon.Addon(self.addonid).getAddonInfo('version')
        #if self.exists:
        #    tree = ET.parse(addon_xml)
        #    root = tree.getroot()
        #    return root.attrib['version']
        else:
            return None

    def install(self):
        # 1) install from a URL
        if self.url is not None:
            self._download()
            self._zip_install()

        # 2) install from a zip file
        elif self.zippath is not None and xbmcvfs.exists(xbmc.translatePath(self.zippath)):
            self._zip_install()
            
        # 3) it's already installed and enabled ==> do nothing
        elif self.enabled:
            return

        # 4) it's already installed ==> enable it
        elif self.installed:
            self._enable()
            return

        # 5) the `addon.xml` file already exists ==> install and enable the addon
        elif self.exists:
            self._add_to_database()

        # 6) install a dummy addon and update it from the repos
        elif self.repo is not None and Addon(self.repo).installed:
            self._repo_install()
        
    def uninstall(self):
        dialogger('Uninstalling {0}'.format(self.addonid))
        if xbmcvfs.exists(xbmc.translatePath('special://home/addons/{0}/'.format(self.addonid))):
            shutil.rmtree(xbmc.translatePath('special://home/addons/{0}/'.format(self.addonid)), ignore_errors=True)
                
        if self.installed:
            xbmc.executebuiltin('XBMC.UpdateLocalAddons()')
            
        self.enabled = False
        self.installed = False

    def _isenabled(self):
        enabled_addons = eval(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Addons.GetAddons", "params": {"enabled": true}, "id": 1}'))['result']
        enabled_addons = [x['addonid'] for x in enabled_addons['addons']]
        return self.addonid in enabled_addons

    def _isinstalled(self):
        all_addons = eval(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Addons.GetAddons", "id": 1}'))['result']
        all_addons = [x['addonid'] for x in all_addons['addons']]
        return self.addonid in all_addons

    def _enable(self):
        if self.meets_dependencies:
            xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Addons.SetAddonEnabled", "params": {"addonid": "' + self.addonid + '", "enabled": true}, "id": 1}')
            self.enabled = True

    def _disable(self):
        xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Addons.SetAddonEnabled", "params": {"addonid": "' + self.addonid + '", "enabled": false}, "id": 1}')
        self.enabled = True

    def _add_to_database(self):
        # if all of its requirements are satisfied, go ahead and add it to the database
        if self.meets_dependencies:
            dialogger('Adding {0} to database'.format(self.addonid))
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
        else:
            dialogger('Dependencies not met, not adding {0} to database'.format(self.addonid))
        
    def _repo_install(self):
        # if the addon folder doesn't exist, create it
        if not xbmcvfs.exists(xbmc.translatePath('special://home/addons/{0}'.format(self.addonid))):
            xbmcvfs.mkdir(xbmc.translatePath('special://home/addons/{0}'.format(self.addonid)))

        # if an `addon.xml` doesn't exist, create a dummy one
        with open(xbmc.translatePath('special://home/addons/{0}/addon.xml'.format(self.addonid)), 'w') as f:
            f.write(dummy_addon_xml.format(self.addonid))

        self._add_to_database()
        
        # try to update the addon
        xbmc.executebuiltin('UpdateAddonRepos')
        xbmc.executebuiltin('XBMC.UpdateLocalAddons()')
        
        # if the dummy addon didn't update from a repo, then uninstall it
        #try:
        #    if self.getVersion() == '0.0.0':
        #        self.uninstall()
        #except:
        #    pass
        
    def _zip_install(self):
        # make sure the zip file contains an `addon.xml` file
        z_in = zipfile.ZipFile(xbmc.translatePath(self.zippath), 'r')
        namelist = z_in.namelist()
        addon_xml_list = sorted([z for z in namelist if z.endswith('addon.xml')], key=lambda x: len(x))
        
        if len(addon_xml_list) > 0:
            prefix = addon_xml_list[0][:-9]
            
            # if the addon folder already exists, remove it
            if xbmcvfs.exists(xbmc.translatePath('special://home/addons/{0}/'.format(self.addonid))):
                shutil.rmtree(xbmc.translatePath('special://home/addons/{0}/'.format(self.addonid)), ignore_errors=True)
            
            # unzip the contents into the addon's folder            
            if prefix == '':
                path = xbmc.translatePath('special://home/addons/{0}'.format(self.addonid))
                z_in.extractall(path)       
            elif prefix == self.addonid:
                path = xbmc.translatePath('special://home/addons')
                z_in.extractall(path)
            else:
                path = xbmc.translatePath('special://home/addons')
                z_in.extractall(path)
                xbmcvfs.rename(xbmc.translatePath('special://home/addons/{0}'.format(prefix)), xbmc.translatePath('special://home/addons/{0}'.format(self.addonid)))
                
            self._add_to_database()
    
    def _download(self):
        download_folder = xbmcaddon.Addon('script.kodi_setter_upper').getSetting('download_folder')
        if download_folder == '':
            download_folder = xbmc.translatePath('special://userdata/addon_data/script.kodi_setter_upper/downloads')
            xbmcaddon.Addon('script.kodi_setter_upper').setSetting('download_folder', download_folder)
            
        self.zippath = os.path.join(xbmc.translatePath(download_folder), self.addonid + '.zip')
        d = Download(self.url, self.zippath)
        
    def _get_dependencies(self):     
        addon_xml = xbmc.translatePath('special://home/addons/{0}/addon.xml'.format(self.addonid))
        
        if xbmcvfs.exists(addon_xml):
            tree = ET.parse(addon_xml)
            root = tree.getroot()
            
            dependencies = root.find('requires')
            if dependencies is not None:
                self.dependencies = [r.attrib['addon'] for r in dependencies]
            else:
                self.dependencies = []
        else:
            self.dependencies = None


class Skin(Addon):
    def __init__(self, addonid, zippath=None, repo=None, url=None, uninstall=None, disable=None):
        self.addonid = addonid
        self.zippath = zippath
        self.repo = repo
        self.url = url

        self.enabled = self._isenabled()
        self.installed = True if self.enabled else self._isinstalled()

        if uninstall is None:
            self.install()
            
            if not self.iscurrent():
                if disable is not None:
                    self._disable()
                else:
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
                dialogger(self.path)
                
                if self.path not in [s.text for source in branch for s in source if s.tag == 'path']:
                    branch.insert(-1, self.element)
                    
                    dialogger("Writing `userdata/sources.xml`")
                    indent(tree.getroot())
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


class Download(object):
    def __init__(self, url, dest=None, no_dialog=None):
        if dest is None:
            xbmcgui.Dialog().ok('Kodi Setter-Upper', '`Download()` -- argument `dest` cannot be `None`')
            raise TypeError
            
        self.url = url
        self.dest = xbmc.translatePath(dest)
           
        # if the destination folder doesn't exist, create it
        if not xbmcvfs.exists(os.path.dirname(self.dest)):
            xbmcvfs.mkdir(os.path.dirname(self.dest))
            
        # if the destination file exists, delete it
        if xbmcvfs.exists(self.dest):
            xbmcvfs.delete(self.dest)
        
        # https://github.com/tvaddonsco/plugin.program.indigo/blob/master/installer.py#L987
        if no_dialog is None:
            # create a Dialog Progress box
            dp = xbmcgui.DialogProgress()
            dp.create("Download Progress:", "", '', 'Please Wait')                
            dp.update(0, "Downloading: " + os.path.basename(dest), '', 'Please Wait')
            
            # download the file
            urllib.urlretrieve(self.url, self.dest, lambda nb, bs, fs, url=self.url: _pbhook(nb, bs, fs, url, dp))
            
        else:
            # download the file
            urllib.urlretrieve(self.url, self.dest)
                
        


def indent(elem, level=0):
    # http://stackoverflow.com/a/33956544
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def _pbhook(numblocks, blocksize, filesize, url, dp):
    # https://github.com/tvaddonsco/plugin.program.indigo/blob/master/installer.py#L995
    try:
        percent = min((numblocks * blocksize * 100) / filesize, 100)
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled():
        raise Exception("Canceled")
        dp.close()
