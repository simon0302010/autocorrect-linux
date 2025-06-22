![Hackatime](https://hackatime-badge.hackclub.com/U08HC7N4JJW/autocorrect-linux)

# autocorrect-linux

**autocorrect-linux** is a system-wide autocorrect tool for Linux desktops. It provides real-time spelling suggestions and corrections for any application, using a global keyboard listener and a floating GUI.

## Features

- Real-time autocorrect suggestions for any window
- Custom personal word list (PWL) support
- Words flagged as incorrect get added PWL after being used 3 times
- Always-on-top floating GUI (When activated)
- Fast next-word recommendations using Machine Learning (planned)

## Requirements

- Linux
- X11


## Installation

Install dependencies:

Arch Linux:
```bash
sudo pacman -S aspell-en
```

Debian/Ubuntu:
```bash
sudo apt install aspell-en
```

Install the package:
```bash
pip install .
```

## Usage

```bash
python -m autocorrect-liunx
```
The floating window will appear at your mouse cursor, showing suggestions as you type.