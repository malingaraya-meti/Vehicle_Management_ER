from tkinter import Button, Entry, Frame, Label, StringVar, ttk

class AnimatedButton(Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.default_background = self.cget("background")
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.config(background="lightblue")

    def on_leave(self, event):
        self.config(background=self.default_background)

class LabeledEntry(Frame):
    def __init__(self, master=None, label_text="", **kwargs):
        super().__init__(master, **kwargs)
        self.label = Label(self, text=label_text)
        self.label.pack(side="left")
        self.entry = Entry(self)
        self.entry.pack(side="right", fill="x", expand=True)

    def get_value(self):
        return self.entry.get()

    def set_value(self, value):
        self.entry.delete(0, 'end')
        self.entry.insert(0, value)

class CustomComboBox(ttk.Combobox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<<ComboboxSelected>>", self.on_select)

    def on_select(self, event):
        print(f"Selected: {self.get()}")