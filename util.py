"""A utility module for helper functions"""
import pyxel

def center_text(text, page_width, y_coord, text_color, x_coord=0, char_width=pyxel.FONT_WIDTH): #pylint: disable=too-many-arguments
    """Helper function for calcuating the start x value for centered text."""

    lines = text.split("\n")
    line_lengths = [len(line) for line in lines]
    text_width = max(line_lengths) * char_width
    pyxel.text(x_coord+(page_width - text_width) // 2, y_coord, text, text_color)
