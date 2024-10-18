from tkinter import font as tkfont
import os

# Colors
STYLE_BG = '#f4f4f4'
STYLE_FG = '#000000'
STYLE_ENTRY_BG = '#e0d7d8'
STYLE_ENTRY_FG = '#000000'
STYLE_BUTTON_BG = '#ed9227'
STYLE_BUTTON_FG = '#000000'
STYLE_CREDITS_BG = '#f4f4f4'
STYLE_CREDITS_FG = '#000000'

# Font
FONT_PATH = "resources/fonts/FiraSans-Regular.ttf"

def get_font(size=12, weight="normal"):
    """
    Carica il font custom con dimensione e peso specificati.
    """
    return tkfont.Font(family="FiraSans", size=size, weight=weight)
