#!/bin/bash

source send_jsonrpc.sh 


# GUI settings
send_jsonrpc "ksu_class" "GUI" "id" "general.settinglevel" "value" "3"
send_jsonrpc "ksu_class" "GUI" "id" "filelists.showhidden" "value" "true"
send_jsonrpc "ksu_class" "GUI" "id" "services.webserver" "value" "true"
send_jsonrpc "ksu_class" "GUI" "id" "services.esallinterfaces" "value" "true"
send_jsonrpc "ksu_class" "GUI" "id" "services.upnplookforexternalsubtitles" "value" "true"
send_jsonrpc "ksu_class" "GUI" "id" "addons.unknownsources" "value" "true"
send_jsonrpc "ksu_class" "GUI" "id" "services.upnprenderer" "value" "true"
send_jsonrpc "ksu_class" "GUI" "id" "audiooutput.guisoundmode" "value" "0"

# Mathematical Muscle Repository
send_jsonrpc "ksu_class" "Addon" "addonid" "repository.mathematical_muscle" "zippath" "special://home/addons/script.kodi_setter_upper/zips/repository.mathematical_muscle-1.0.0.zip"

# Remote Downloader
send_jsonrpc "ksu_class" "Addon" "addonid" "script.remote_downloader" "repo" "repository.mathematical_muscle"

# Kodi Setter-Upper
send_jsonrpc "ksu_class" "Addon" "addonid" "script.kodi_setter_upper" "id" "dialog" "value" "false"

# Confluence
send_jsonrpc "ksu_class" "Skin" "addonid" "skin.confluence" "repo" "repository.xbmc.org"
