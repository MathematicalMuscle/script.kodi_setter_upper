#!/bin/bash

send_jsonrpc ()
{
  if ! [[ -v KODI_HOST ]]; then
    # EXAMPLE: KODI_HOST="http://10.0.0.120:8080"
    read -p "Kodi address:  " KODI_HOST
    export KODI_HOST
  fi

  # https://stackoverflow.com/a/44555048
  params=$(printf "\"%s\": \"%s\", " "$@")
  
  # https://stackoverflow.com/a/27658733
  payload="{\"jsonrpc\": \"2.0\", \"method\": \"Addons.ExecuteAddon\", \"id\": 1, \"params\": {\"addonid\": \"script.kodi_setter_upper\", \"params\": {${params::-2}}}}"

  curl -v -u xbmc:password -d "$payload" -H "Content-type:application/json" -X POST "${KODI_HOST}/jsonrpc"  &>/dev/null
}



# EXAMPLES:

# send_jsonrpc "ksu_class" "Addon" "addonid" "script.remote_downloader" "id" "download_local" "value" "No"
# send_jsonrpc "ksu_class" "GUI" "id" "audiooutput.guisoundmode" "value" "0"
# send_jsonrpc "ksu_class" "Skin" "addonid" "skin.confluence" "repo" "repository.xbmc.org"
# send_jsonrpc "ksu_class" "Skin" "addonid" "skin.confluence" "id" "HomeMenuNoWeatherButton" "value" "True"


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
