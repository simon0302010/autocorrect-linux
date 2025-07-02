import platform
import threading

from pynput.keyboard import Listener

from .core import core, gui, utils

listener = None
running = False

python_version = platform.python_version()

print(f"Running on Python {python_version}")


def key_listener():
    global listener
    listener = Listener(on_press=core.on_press)
    listener.start()
    listener.join()


def stop():
    global listener, running
    if core.gui_root is not None:
        core.gui_root.withdraw()
    if listener is not None:
        listener.stop()
        listener = None
    running = False


def start():
    global listener, running
    if core.gui_root is not None:
        core.gui_root.deiconify()
    if listener is None:
        t = threading.Thread(target=key_listener, daemon=True)
        t.start()
    running = True


def toggle():
    global running
    if running:
        stop()
    else:
        start()


def run_gui():
    root, textboxes = gui.build_gui()
    core.gui_root = root
    core.text1, core.text2, core.text3, core.stats = textboxes
    start()
    root.mainloop()


def main():
    global gui_thread, running
    gui_thread = threading.Thread(target=run_gui, daemon=True)
    gui_thread.start()

    # Start hotkey listener in a separate thread
    hotkey_thread = threading.Thread(
        target=utils.hotkey_listener, args=(toggle,), daemon=True
    )
    hotkey_thread.start()

    gui_thread.join()
