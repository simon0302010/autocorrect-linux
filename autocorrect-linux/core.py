import click
from subprocess import PIPE, Popen
from pynput.keyboard import Key, Listener

letters = {}
texts = {}

def get_window_id():
    try:
        root = Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=PIPE, stderr=PIPE)
        root_output, _ = root.communicate()
        
        if root_output:
            for line in root_output.decode().split('\n'):
                if "_NET_ACTIVE_WINDOW(WINDOW):" in line:
                    parts = line.split()
                    for part in parts:
                        if part.startswith('0x') and len(part) > 3:
                            window_id = part.rstrip(',')  # Remove trailing comma
                            return window_id
    except Exception as e:
        click.echo(e)
    return "Unknown"

def on_press(key):
    current_window_id = str(get_window_id())
    if current_window_id not in letters:
        letters[current_window_id] = []
    if hasattr(key, "char") and key.char is not None:
        letters[current_window_id].append(key.char)
    elif key == Key.backspace:
        if letters[current_window_id]:
            letters[current_window_id].pop()
    elif key == Key.space or key == Key.enter:
        letters[current_window_id].append(" ")
    
    text = "".join(letters[current_window_id])
    texts[current_window_id] = text
    click.echo(f"{current_window_id}: {texts[current_window_id]}")
    
def main():
    with Listener(on_press=on_press) as listener:
        listener.join()