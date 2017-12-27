# Usage

There are two ways to use this addon:

1. JSON-RPC

2. By placing/editing the files `addons.xml`, `guisettings.xml`, `skin.xml`, and `sources.xml` in the userdata folder for this addon (`special://userdata/addon_data/script.kodi_setter_upper/config/`)


## JSON-RPC Usage

There are two ways to use this addon via JSON-RPC: URL and command line.  For example, to set this addon's setting "dialog" to "true," you could do either of the following:

* Modify the IP address and port and go to this URL in your browser:

  [http://10.0.0.120:8080/jsonrpc?request={"jsonrpc":"2.0","id":1,"method":"Addons.ExecuteAddon","params":{"addonid":"script.kodi_setter_upper","params":{"ksu_class":"Addon","addonid":"script.kodi_setter_upper", "id":"dialog", "value":"true"}}}](http://10.0.0.120:8080/jsonrpc?request={"jsonrpc":"2.0","id":1,"method":"Addons.ExecuteAddon","params":{"addonid":"script.kodi_setter_upper","params":{"ksu_class":"Addon","addonid":"script.kodi_setter_upper", "id":"dialog", "value":"true"}}})

* Execute the following commands in the terminal:

  ```bash
  source send_jsonrpc.sh

  send_jsonrpc "ksu_class" "Addon" "addonid" "script.kodi_setter_upper" "id" "dialog" "value" "true"
  ```

To execute different actions, simply modify the parameters in the URL or the arguments to the function `send_jsonrpc`.  


## JSON-RPC Examples

### Install an addon (including skins)

#### From a zip file

```bash
send_jsonrpc "ksu_class" "Addon" "addonid" "repository.mathematical_muscle" "zippath" "special://home/addons/script.kodi_setter_upper/zips/repository.mathematical_muscle-1.0.0.zip"
```

#### From a repository

*Note:* The repository must be installed for this to work properly.

```bash
send_jsonrpc "ksu_class" "Addon" "addonid" "script.remote_downloader" "repo" "repository.mathematical_muscle"
```

#### From a URL

```bash
send_jsonrpc "ksu_class" "Addon" "addonid" "script.test" "url" "https://github.com/MathematicalMuscle/script.test/archive/master.zip"
```


### Disable an addon

```bash
send_jsonrpc "ksu_class" "Addon" "addonid" "script.test" "disable" "true"
```


### Uninstall an addon

```bash
send_jsonrpc "ksu_class" "Addon" "addonid" "script.test" "uninstall" "true"
```


### Install a skin and set it as the current skin

```bash
send_jsonrpc "ksu_class" "Skin" "addonid" "skin.confluence_mm" "repo" "repository.mathematical_muscle"
```


### Set an addon setting

```bash
send_jsonrpc "ksu_class" "Addon" "addonid" "script.kodi_setter_upper" "id" "dialog" "value" "true"
```


### Set a skin setting

```bash
send_jsonrpc "ksu_class" "Skin" "addonid" "skin.confluence_mm" "id" "HomeProgramButton1" "value" "script.remote_downloader"
```


### Set a GUI setting

```bash
send_jsonrpc "ksu_class" "GUI" "id" "filelists.showhidden" "value" "true"
```


### Add a source (doesn't work for adding sources to Kodi's library)

```bash
send_jsonrpc "ksu_class" "Source" "sourcetype" "files" "name" "*mathematicalmuscle" "path" "https://mathematicalmuscle.github.io/"
```


### Download a file

```bash
send_jsonrpc "ksu_class" "Download" "url" "https://github.com/MathematicalMuscle/Mathematical_Muscle_Repo/raw/master/zips/repository.mathematical_muscle/repository.mathematical_muscle-1.0.0.zip"
```
