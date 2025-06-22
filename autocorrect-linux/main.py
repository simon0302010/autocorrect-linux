import threading
from time import sleep
from pynput.keyboard import Listener

from . import core
from . import gui

def key_listener():
    with Listener(on_press=core.on_press) as listener:
        listener.join()
        
def main():
    root, textboxes = gui.build_gui()
    
    core.gui_root = root
    core.text1, core.text2, core.text3 = textboxes
    
    listener_thread = threading.Thread(target=key_listener, daemon=True)
    listener_thread.start()
    
    root.mainloop()