from tkinter import Frame, Button, Label

def animate_button(button: Button):
    original_color = button.cget("background")
    
    def on_enter(event):
        button.config(background="lightblue")
    
    def on_leave(event):
        button.config(background=original_color)
    
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

def fade_in(widget: Frame, duration: int = 500):
    widget.pack_forget()
    widget.pack()
    widget.update_idletasks()
    
    for i in range(0, 101, 5):
        widget.attributes("-alpha", i / 100)
        widget.after(duration // 20)

def fade_out(widget: Frame, duration: int = 500):
    for i in range(100, -1, -5):
        widget.attributes("-alpha", i / 100)
        widget.after(duration // 20)
    widget.pack_forget()