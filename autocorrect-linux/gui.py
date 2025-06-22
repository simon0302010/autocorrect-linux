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

    root.rowconfigure(0, minsize=30)

    text1 = customtkinter.CTkTextbox(root, border_width=1)
    text1.grid(row=1, column=0, sticky='nsew')
    text1.insert('1.0', 'Test 1')

    text2 = customtkinter.CTkTextbox(root, border_width=1)
    text2.grid(row=1, column=1, sticky='nsew')
    text2.insert('1.0', 'Test 2')

    text3 = customtkinter.CTkTextbox(root, border_width=1)
    text3.grid(row=1, column=2, sticky='nsew')
    text3.insert('1.0', 'Test 3')

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.rowconfigure(1, weight=1)

    close_button = customtkinter.CTkButton(
        root,
        text="X",
        command=root.destroy,
        fg_color="#ff1100",
        hover_color="#cf4d44",
        width=30,
        height=20
    )
    close_button.place(x=width-35, y=5)

    return root, (text1, text2, text3)