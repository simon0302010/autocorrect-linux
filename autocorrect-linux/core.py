import os
import click
import enchant
import enchant.pypwl
from . import utils
from pynput.keyboard import Key, Listener

# set variables
gui_root = None
text1 = None
text2 = None
text3 = None

# dictionaries to store letters, texts, and learned words
letters = {}
texts = {}
learned_words = {}

pwl_path = os.path.join(utils.data_dir, "pwl.txt")

if not os.path.exists(pwl_path):
    open(pwl_path, 'a').close()

# load dictionaries
pwl = enchant.pypwl.PyPWL(pwl_path)
dictionary = enchant.DictWithPWL("en", pwl_path)

def get_suggestions(word):
    valid_suggestions = []
    
    suggestions = dictionary.suggest(word)
    if suggestions:
        for suggestion in suggestions:
            if suggestion.startswith(word):
                valid_suggestions.append(suggestion)
        return valid_suggestions
    else:
        return False

def update_suggestions(suggestions):
    if gui_root and text1:
        def update_text():
            if suggestions[0] is not None:
                text1.delete("1.0", "end")
                text1.insert("1.0", suggestions[0])
            if suggestions[1] is not None:
                text2.delete("1.0", "end")
                text2.insert("1.0", suggestions[1])
            if suggestions[2] is not None:
                text3.delete("1.0", "end")
                text3.insert("1.0", suggestions[2])
        gui_root.after(0, update_text)

def suggest_next():
    update_suggestions([None, "Next Word 1", "Next Word 2"])

def suggest(last_word, text, words):
    update_suggestions([f'"{last_word}"', None, None])
    if last_word:
        suggestions = get_suggestions(last_word)
        if suggestions and len(suggestions) >= 2:
            update_suggestions([None, suggestions[0], suggestions[1]])
        elif suggestions and len(suggestions) == 1:
            update_suggestions([None, suggestions[0], ""])
        else:
            update_suggestions([None, "", ""])
    elif text.endswith(" "):
        if words[-2]:
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
            
            suggest_next()
        else:
            suggest_next()

def on_press(key):
    global gui_root, text1, text2, text3
    global letters, texts, learned_words, pwl

    current_window_id = str(utils.get_window_id())
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
            if last_word.strip:
                last_word = last_word.strip()
                if last_word and dictionary.check(last_word):
                    click.secho(last_word, fg="green")
                    update_suggestions([f'"{last_word}"', None, None])
                else:
                    suggest(last_word, text, words)
            else:
                suggest(last_word, text, words)
                    
def main():
    with Listener(
        on_press=on_press
    ) as listener:
        listener.join()