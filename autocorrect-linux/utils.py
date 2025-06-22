import os
import click
import requests
from subprocess import PIPE, Popen

data_dir = os.path.expanduser("~/.local/share/autocorrect-linux")
os.makedirs(data_dir, exist_ok=True)

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

def load_dictionary(pwl_path=None):
    dict_path = os.path.join(data_dir, "words_alpha.txt")
    try:
        if not os.path.exists(dict_path):
            click.echo("Downloading dictionary...")
            response = requests.get("https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt")
            if response.status_code == 200:
                with open(dict_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
            else:
                click.echo(f"Failed to download dictionary: {response.status_code}")
                return []
        click.echo("Loading dictionary...")
        words = []
        if pwl_path and os.path.exists(pwl_path):
            with open(pwl_path, 'r', encoding='utf-8') as pwl_file:
                words.extend(line.strip() for line in pwl_file if line.strip())
        with open(dict_path, 'r', encoding='utf-8') as f:
            words.extend(line.strip() for line in f if line.strip())
        words = sorted(set(words))
        return words
    except requests.RequestException as e:
        click.echo(f"Error loading dictionary: {e}")
        return []