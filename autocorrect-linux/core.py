import click
from pynput.keyboard import Key, Listener

global letters
letters = []

def on_press(key):
    if hasattr(key, "char") and key.char is not None:
        letters.append(key.char)
    elif key == Key.backspace:
        try:
            letters.pop()
        except IndexError:
            pass
    elif key == Key.space or Key.enter:
        letters.append(" ")
    elif key == Key.esc:
        return False
    
    click.echo("".join(letters))
    
def main():
    with Listener(
        on_press=on_press
    ) as listener:
        listener.join()