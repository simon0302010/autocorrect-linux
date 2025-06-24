# autocorrect-linux

**autocorrect-linux** is a system-wide word suggestion and prediction tool for Linux desktops.  
It provides real-time word suggestions and next-word predictions for any application, using a global keyboard listener and a floating GUI.  
**Note:** This tool does **not** automatically replace misspelled words—it only suggests possible corrections and predictions.

---

## Features

- Real-time word suggestions for any window
- Next-word prediction using Machine Learning
- Custom personal word list (PWL) support
- Words flagged as incorrect get added to PWL after being used 3 times
- Always-on-top floating GUI (when activated)
- Works system-wide on Linux/X11

---

## Requirements

- Linux (X11)
- Python 3.9 - 3.11
- **4GB free disk space required** (for model and data files)
- **8GB RAM recommended** (for smooth operation)

---

## Installation

**System dependencies:**

Arch Linux:
```bash
sudo pacman -S xorg-xprop
```

Debian/Ubuntu:
```bash
sudo apt install x11-utils
```

**Python package:**
```bash
pip install autocorrect_linux
```

---

## Usage

Start the tool with:
```bash
python -m autocorrect_linux
```

- The first startup may take **several seconds** as the language model and vocabulary are downloaded and loaded into memory.
- On subsequent runs, startup will be faster.

A floating window will appear at your mouse cursor, showing word suggestions and predictions as you type.  
You can click on suggestions to copy them, but the tool will **not** automatically replace words in your application.

### Hotkeys

- **Alt+C**: Pause/resume the suggestion window and prediction engine.

### Notes

- The tool works system-wide, but only on Linux/X11 desktops.
- The GUI is non-intrusive and does not allow editing.
- Suggestions are based on both a dictionary and a machine learning model.
- If you use a personal word list (PWL), words you use often will be suggested more quickly.

---

## Troubleshooting

- **Startup is slow:** The first run downloads and loads a large model (~400MB). Make sure you have a stable internet connection and enough disk space.
- **High RAM usage:** 8GB RAM is recommended, especially for large models.
- **No suggestions appear:** Make sure you are running under X11 (not Wayland) and that required system packages are installed.
- **Hotkey does not work:** Ensure no other application is using Alt+C as a global shortcut.

---

## License

GPL-3.0

---

## Author

[simon0302010](https://github.com/simon0302010/autocorrect-linux)