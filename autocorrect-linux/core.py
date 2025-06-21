import os
import click
import enchant
from subprocess import PIPE, Popen
import enchant.pypwl
from pynput.keyboard import Key, Listener

letters = {}
texts = {}
learned_words = {}

pwl_path = "pwl.txt"

if not os.path.exists(pwl_path):
    open(pwl_path, 'a').close()

# load dictionaries
pwl = enchant.pypwl.PyPWL(pwl_path)
dictionary = enchant.DictWithPWL("en", pwl_path)

# get id of focused window
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
    global letters, texts, learned_words, pwl

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
    words = text.split(" ")
    if words:
        last_word = words[-1]
        if not last_word.isnumeric():
            if last_word and dictionary.check(last_word):
                click.secho(last_word, fg="green")
            else:
                if last_word:
                    suggestions = dictionary.suggest(last_word)
                    if suggestions:
                        click.secho(suggestions[0], fg="red")
                    else:
                        click.secho(f"No suggestions for: {last_word}", fg="yellow")
                elif text.endswith(" "):
                    if not dictionary.check(words[-2]):
                        last_word = words[-2]
                        if last_word in learned_words:
                            learned_words[last_word]["uses"] += 1
                        else:
                            learned_words[last_word] = {"uses": 1}
                        click.secho(f"{last_word} has been used {learned_words[last_word]['uses']} times.", fg="yellow")
                        if learned_words[last_word]["uses"] >= 3:
                            pwl.add_to_pwl(last_word)
                            click.secho(f"Added {last_word} to PWL", fg="blue")
    
def main():
    with Listener(on_press=on_press) as listener:
        listener.join()