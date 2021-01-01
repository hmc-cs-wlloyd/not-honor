"""Defines a button class for clickable buttons with text"""

import pyxel

class Button: #pylint: disable=too-many-instance-attributes
    """A class representing physical buttons with text upon them"""
    def __init__(self, x_coord, y_coord, width, height, text, button_color, #pylint: disable=too-many-arguments
             border_color=pyxel.COLOR_WHITE, text_color=pyxel.COLOR_WHITE):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.width = width
        self.height = height
        self.text = text
        self.button_color = button_color
        self.border_color = border_color
        self.text_color = text_color

    def is_moused_over(self):
        """Returns true if the mouse is currently above the button"""
        return pyxel.mouse_x > self.x_coord and \
                pyxel.mouse_x < self.x_coord + self.width and \
                pyxel.mouse_y > self.y_coord and \
                pyxel.mouse_y < self.y_coord + self.height

    def is_clicked(self):
        """Returns true if the button is clicked in the current frame"""
        return pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON, hold=2, period=16) and self.is_moused_over()

    def draw(self):
        """Draws the button to the screen"""
        pyxel.rect(self.x_coord, self.y_coord, self.width, self.height, self.button_color)
        pyxel.rectb(self.x_coord, self.y_coord, self.width, self.height, self.border_color)
        text_width = len(self.text) * pyxel.FONT_WIDTH
        pyxel.text(self.x_coord + (self.width - text_width)/2, self.y_coord + (self.height - pyxel.FONT_HEIGHT)/2,
            self.text, self.text_color)
