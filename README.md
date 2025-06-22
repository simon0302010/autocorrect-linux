![Hackatime](https://hackatime-badge.hackclub.com/U08HC7N4JJW/autocorrect-linux)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/simon0302010/autocorrect-linux/.github%2Fworkflows%2Fpython-package.yml)
![PyPI - Version](https://img.shields.io/pypi/v/autocorrect-linux)


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
sudo pacman -S xorg-xprop
```

Debian/Ubuntu:
```bash
sudo apt install x11-utils
```

Install the package:
```bash
pip install autocorrect-linux
```

## Usage

```bash
python -m autocorrect-liunx
```
The floating window will appear at your mouse cursor, showing suggestions as you type.