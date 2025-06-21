import tkinter as tk
from pynput.mouse import Controller

mouse = Controller()
root = tk.Tk()

width = 300
height = 120

x, y = mouse.position

# Setting some window properties
root.configure(background="white")
root.geometry(f"{width}x{height}+{x - width // 2}+{y - height // 2}")
root.overrideredirect(True)

close_button = tk.Button(root, text="X", command=root.destroy, bd=0, bg="red", fg="white")
close_button.place(x=width-40, y=5)

root.mainloop()