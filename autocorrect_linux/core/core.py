import os
import re

import click
import distance
from pynput.keyboard import Key, Listener

from . import predict, utils

# set variables
gui_root = None
text1 = None
text2 = None
text3 = None
stats = None

# dictionaries to store letters, texts, and learned words
letters = {}
texts = {}
learned_words = {}

pwl_path = os.path.join(utils.data_dir, "pwl.txt")

if not os.path.exists(pwl_path):
    open(pwl_path, "a").close()

# load dictionary
dictionary = utils.load_dictionary(pwl_path=pwl_path)


def get_similar(word):
    list_tuples = sorted(distance.ifast_comp(word, dictionary))[:50]
    output = []
    for _, single_word in list_tuples:
        output.append(single_word)
    return output


def get_suggestions(prefix):
    suggestions = [w for w in dictionary if w.startswith(prefix) and w != prefix]

    if suggestions:
        return suggestions
    else:
        return False


def update_suggestions(suggestions, last_time=None):
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
            stats.delete("1.0", "end")
            if last_time is not None:
                stats.insert("1.0", f"inference took {round(last_time * 1000)}ms")

        gui_root.after(0, update_text)


def suggest_next(text):
    click.echo(f"Text: {text}")
    predictions = predict.generate(text, 3)
    update_suggestions(predictions)


def suggest(last_word: str, text: str, words):
    if last_word.lower() in dictionary:
        update_suggestions([last_word, None, None])
    else:
        update_suggestions([f'"{last_word}"', None, None])
    if last_word:
        suggestions = get_suggestions(last_word)
        if suggestions and len(suggestions) >= 2:
            update_suggestions([None, suggestions[0], suggestions[1]])
        elif suggestions and len(suggestions) == 1:
            update_suggestions([None, suggestions[0], ""])
        else:
            similar = get_similar(last_word)
            if similar and len(similar) >= 2:
                update_suggestions([None, similar[0], similar[1]])
            elif similar and len(similar) == 1:
                update_suggestions([None, similar[0], ""])
            else:
                update_suggestions([None, "", ""])
    elif text.endswith(" "):
        if words[-2]:
            if words[-2].lower() not in dictionary and not words[-2].isnumeric():
                last_word = words[-2]
                if last_word in learned_words:
                    learned_words[last_word]["uses"] += 1
                else:
                    learned_words[last_word] = {"uses": 1}
                click.secho(
                    f"{last_word} has been used {learned_words[last_word]['uses']} times.",
                    fg="yellow",
                )
                if learned_words[last_word]["uses"] >= 3:
                    dictionary.append(last_word)
                    with open(pwl_path, "a") as pwl_file:
                        pwl_file.write(f"{last_word}\n")
                    click.secho(f"Added {last_word} to PWL", fg="blue")
            suggest_next(text)
        else:
            suggest_next(text)


def on_press(key):
    global gui_root, text1, text2, text3
    global letters, texts, learned_words

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
    # click.echo(text)
    texts[current_window_id] = text
    words_old = text.split(" ")
    if words_old:
        words = []
        for word in words_old:
            words.append(re.sub(r"[^A-Za-z0-9]", "", word))
        last_word = words[-1]
        if not last_word.isnumeric():
            if last_word.strip():
                last_word = last_word.strip()
                suggest(last_word, text, words)
            else:
                suggest(last_word, text, words)
        else:
            update_suggestions([last_word, "", ""])


def on_release(key):
    pass


def main():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
