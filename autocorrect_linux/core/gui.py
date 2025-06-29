import sys

import customtkinter
from pynput.mouse import Controller


def build_gui():
    mouse = Controller()
    root = customtkinter.CTk()

    width = 350
    height = 80

    x, y = mouse.position

    customtkinter.set_appearance_mode("System")

    root.geometry(f"{width}x{height}+{x - width // 2}+{y - height // 2}")
    root.overrideredirect(True)

    for i in range(4):
        root.columnconfigure(i, weight=1 if i < 3 else 0)
    root.rowconfigure(0, minsize=30)
    root.rowconfigure(1, weight=1)

    stats = customtkinter.CTkTextbox(root, border_width=0, height=30, text_color="gray")
    stats.grid(row=0, column=0, columnspan=3, sticky="nsew")
    stats.insert("1.0", "start typing for suggestions to appear")

    text1 = customtkinter.CTkTextbox(root, border_width=2)
    text1.grid(row=1, column=0, sticky="nsew")

    text2 = customtkinter.CTkTextbox(root, border_width=2)
    text2.grid(row=1, column=1, sticky="nsew")

    text3 = customtkinter.CTkTextbox(root, border_width=2)
    text3.grid(row=1, column=2, sticky="nsew")

    def close_all():
        sys.exit(0)

    close_button = customtkinter.CTkButton(
        root,
        text="X",
        command=close_all,
        fg_color="#ff1100",
        hover_color="#cf4d44",
        width=30,
        height=20,
    )
    close_button.place(x=width - 35, y=5)

    return root, (text1, text2, text3, stats)
