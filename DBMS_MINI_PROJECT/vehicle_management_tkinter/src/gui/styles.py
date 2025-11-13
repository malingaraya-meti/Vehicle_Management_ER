from tkinter import font

# Define styles and themes for the application
class Styles:
    # Colors
    PRIMARY_COLOR = "#3498db"
    SECONDARY_COLOR = "#2ecc71"
    ACCENT_COLOR = "#e74c3c"
    BACKGROUND_COLOR = "#ecf0f1"
    TEXT_COLOR = "#2c3e50"

    # Fonts
    TITLE_FONT = ("Helvetica", 16, "bold")
    HEADER_FONT = ("Helvetica", 14, "bold")
    BODY_FONT = ("Helvetica", 12)

    # Button styles
    BUTTON_STYLE = {
        "bg": PRIMARY_COLOR,
        "fg": "white",
        "font": BODY_FONT,
        "activebackground": SECONDARY_COLOR,
        "activeforeground": "white",
        "borderwidth": 2,
        "relief": "raised"
    }

    # Entry styles
    ENTRY_STYLE = {
        "font": BODY_FONT,
        "bg": "white",
        "fg": TEXT_COLOR,
        "borderwidth": 2,
        "relief": "sunken"
    }

    # Label styles
    LABEL_STYLE = {
        "font": BODY_FONT,
        "bg": BACKGROUND_COLOR,
        "fg": TEXT_COLOR
    }

    # Treeview styles
    TREEVIEW_STYLE = {
        "background": "white",
        "foreground": TEXT_COLOR,
        "font": BODY_FONT,
        "rowheight": 25
    }

    @staticmethod
    def apply_button_style(button):
        button.config(**Styles.BUTTON_STYLE)

    @staticmethod
    def apply_entry_style(entry):
        entry.config(**Styles.ENTRY_STYLE)

    @staticmethod
    def apply_label_style(label):
        label.config(**Styles.LABEL_STYLE)

    @staticmethod
    def apply_treeview_style(treeview):
        treeview.config(**Styles.TREEVIEW_STYLE)