from tkinter import font as tkfont

# Colors
STYLE_BG = '#f4f4f4'
STYLE_FG = '#000000'
STYLE_ENTRY_BG = '#e0d7d8'
STYLE_ENTRY_FG = '#000000'
STYLE_BUTTON_BG = '#ed9227'
STYLE_BUTTON_FG = '#000000'
STYLE_BUTTON_HOVER = '#d97d0f'
STYLE_SECONDARY_BG = '#ffffff'
STYLE_SECONDARY_HOVER = '#f1f1f1'
STYLE_PANEL_BG = '#f7f7f7'
STYLE_PANEL_BORDER = '#dedede'
STYLE_CREDITS_BG = '#f4f4f4'
STYLE_CREDITS_FG = '#000000'

def get_font(size=12, weight="normal"):
    """
    Carica il font custom con dimensione e peso specificati.
    """
    return tkfont.Font(family="FiraSans", size=size, weight=weight)
