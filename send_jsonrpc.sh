#!/bin/bash

send_jsonrpc ()
{
  if ! [[ -v KODI_HOST ]]; then
    # EXAMPLE: KODI_HOST="http://10.0.0.120:8080"
    read -p "Kodi IP address:  " KODI_IP
    read -p "Kodi port:  " KODI_PORT
    export KODI_HOST="http://$KODI_IP:$KODI_PORT"
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
