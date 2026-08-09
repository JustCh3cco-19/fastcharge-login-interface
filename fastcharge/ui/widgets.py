"""Widget Tkinter riutilizzabili e responsive."""

import tkinter as tk
from tkinter import font as tkfont

from fastcharge.ui.styles import (
    STYLE_BUTTON_BG,
    STYLE_BUTTON_FG,
    STYLE_BUTTON_HOVER,
)


class RoundedEntry(tk.Entry):
    """Campo di testo minimale con evidenziazione al passaggio del mouse."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(relief="flat", bd=0, highlightthickness=0)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, _event):
        self.configure(highlightthickness=2, highlightbackground="#4a90e2")

    def on_leave(self, _event):
        self.configure(highlightthickness=0)


class RoundedButton(tk.Canvas):
    """Pulsante Canvas arrotondato, utilizzabile con mouse e tastiera."""

    def __init__(self, master=None, **kwargs):
        self.command = kwargs.pop("command", None)
        text = kwargs.pop("text", "")
        font = kwargs.pop("font", None)
        self.button_bg = kwargs.pop("bg", STYLE_BUTTON_BG)
        self.button_fg = kwargs.pop("fg", STYLE_BUTTON_FG)
        self.hover_bg = kwargs.pop("hover_bg", STYLE_BUTTON_HOVER)
        self.border_color = kwargs.pop("border_color", self.button_bg)
        requested_width = kwargs.pop("width", 300)
        kwargs.pop("padx", None)
        kwargs.pop("pady", None)
        requested_pixels = requested_width * 12 if requested_width <= 50 else requested_width
        resolved_font = font if isinstance(font, tkfont.Font) else tkfont.Font(font=font)
        width = max(requested_pixels, resolved_font.measure(text) + 72)
        height = kwargs.pop("height", 66)
        super().__init__(
            master,
            width=width,
            height=height,
            bg=master.cget("bg"),
            bd=0,
            highlightthickness=2,
            highlightbackground=master.cget("bg"),
            highlightcolor=STYLE_BUTTON_BG,
            cursor="hand2",
            takefocus=True,
            **kwargs,
        )
        self._width = width
        self._height = height
        self._base_width = width
        self._base_height = height
        self._base_font_size = abs(resolved_font.cget("size"))
        self._font_weight = resolved_font.cget("weight")
        self._text = text
        self._radius = 18
        self._shape = None
        self._draw(self.button_bg, text, resolved_font)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self._invoke)
        self.bind("<Return>", self._invoke)
        self.bind("<space>", self._invoke)
        self.bind("<FocusIn>", lambda _event: self.configure(highlightbackground=STYLE_BUTTON_BG))
        self.bind(
            "<FocusOut>",
            lambda _event: self.configure(highlightbackground=self.master.cget("bg")),
        )

    def _rounded_points(self):
        width, height, radius = self._width, self._height, self._radius
        return [
            radius, 2, width - radius, 2, width - 2, 2, width - 2, radius,
            width - 2, height - radius, width - 2, height - 2,
            width - radius, height - 2, radius, height - 2, 2, height - 2,
            2, height - radius, 2, radius, 2, 2,
        ]

    def _draw(self, color, text, font):
        self._shape = self.create_polygon(
            self._rounded_points(),
            smooth=True,
            splinesteps=24,
            fill=color,
            outline=self.border_color,
            width=2,
        )
        self.create_text(
            self._width / 2,
            self._height / 2,
            text=text,
            fill=self.button_fg,
            font=font,
        )

    def _set_color(self, color):
        self.itemconfigure(self._shape, fill=color)

    def apply_scale(self, scale):
        """Ridimensiona geometria e testo mantenendo le proporzioni originali."""
        self._width = max(210, round(self._base_width * scale))
        self._height = max(48, round(self._base_height * scale))
        self._radius = max(12, round(18 * scale))
        scaled_font = tkfont.Font(
            family="FiraSans",
            size=max(12, round(self._base_font_size * scale)),
            weight=self._font_weight,
        )
        self.configure(width=self._width, height=self._height)
        self.delete("all")
        self._draw(self.button_bg, self._text, scaled_font)

    def _invoke(self, _event=None):
        self.focus_set()
        if self.command:
            self.command()

    def on_enter(self, _event):
        self._set_color(self.hover_bg)

    def on_leave(self, _event):
        self._set_color(self.button_bg)
