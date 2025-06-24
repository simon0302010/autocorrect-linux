# autocorrect-linux

**autocorrect-linux** is a system-wide word suggestion and prediction tool for Linux desktops.  
It provides real-time word suggestions and next-word predictions for any application, using a global keyboard listener and a floating GUI.  
**Note:** This tool does **not** automatically replace misspelled words—it only suggests possible corrections and predictions.

## Features

- Real-time word suggestions for any window
- Next-word prediction using Machine Learning
- Custom personal word list (PWL) support
- Words flagged as incorrect get added to PWL after being used 3 times
- Always-on-top floating GUI (when activated)
- Works system-wide on Linux/X11

## Requirements

- Linux
- X11

## Installation

Install dependencies:

Arch Linux:
```bash
sudo pacman -S xorg-xprop
```

Debian/Ubuntu:
```bash
sudo apt install x11-utils
```

Install the package:
```bash
pip install autocorrect_linux
```

## Usage

```bash
python -m autocorrect_linux
```
A floating window will appear at your mouse cursor, showing word suggestions and predictions as you type.  
You can click on suggestions to copy them, but the tool will **not** automatically replace words in your