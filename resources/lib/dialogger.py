"""Display a message

"""


import xbmcaddon
import xbmcgui


dialog = xbmcaddon.Addon('script.kodi_setter_upper').getSetting('dialog') == 'true'


def dialogger(message, dialog=dialog):
    """Display ``message`` if ``dialog``

    Parameters
    ----------
    message : str
        the message to potentially be displayed
    dialog : bool
        whether or not to display dialog messages

    """
    if dialog:
        xbmcgui.Dialog().ok('Kodi Setter Upper', message)
