"""Utilities

"""


import xbmc


# get the platform
if xbmc.getCondVisibility("System.Platform.Android"):
    PLATFORM = 'android'
elif xbmc.getCondVisibility("System.Platform.Windows"):
    PLATFORM = 'windows'
elif xbmc.getCondVisibility("System.Platform.OSX"):
    PLATFORM = 'osx'
elif xbmc.getCondVisibility("System.Platform.IOS"):
    PLATFORM = 'ios'
elif xbmc.getCondVisibility("System.Platform.Darwin"):
    PLATFORM = 'darwin'
elif xbmc.getCondVisibility("System.Platform.ATV2"):
    PLATFORM = 'atv2'
elif xbmc.getCondVisibility("System.Platform.Linux.RaspberryPi"):
    PLATFORM = 'raspberrypi'
elif xbmc.getCondVisibility("System.Platform.Linux"):
    PLATFORM = 'linux'
