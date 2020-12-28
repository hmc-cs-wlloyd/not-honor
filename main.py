"""Main function for working title Not a Place of Honor, a game developed for itch.io's Historical Game Jam 3"""

from enum import Enum
import pyxel

SCREEN_WIDTH = 120
SCREEN_HEIGHT = 160

SHOP_COLUMNS = 2
SHOP_ROWS = 4

class Screen(Enum):
    """An enum containing all possible screens in the game"""
    TITLE = "title"
    SHOP = "shop"
    MAP = "map"


class App:
    """Class to run the game itself"""
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Not a Place of Honor")
        self.player_funding = 1000000
        self.screen = Screen.TITLE

        pyxel.run(self.update, self.draw)

    def update(self):
        """Updates game data each frame"""
        if self.screen == Screen.TITLE:
            self.update_title()

    def draw(self):
        """Draws frame each frame"""
        if self.screen == Screen.TITLE:
            self.draw_title()
        elif self.screen == Screen.SHOP:
            self.draw_shop()

    def update_title(self):
        """Handles updates while the player is on the title screen"""
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.screen = Screen.SHOP

    def draw_title(self):
        """Draws frames while the player is on the title screen"""
        self.center_text("Not a Place of Honor", page_width=SCREEN_WIDTH, y_coord=66, text_color=7)
        self.center_text("- PRESS ENTER TO START -", page_width=SCREEN_WIDTH, y_coord=126, text_color=7)

    def draw_shop(self):
        """Draws frames while the player is on the shop screen"""
        pyxel.cls(0)
        pyxel.mouse(visible=True)
        self.center_text("Remaining Budget: $" + str(self.player_funding), page_width=SCREEN_WIDTH, y_coord=10, text_color=7)

        for i in range(SHOP_ROWS):
            for j in range(SHOP_COLUMNS):
                pyxel.rectb(SCREEN_WIDTH/SHOP_COLUMNS * j,
                            20 + (SCREEN_HEIGHT-20)/SHOP_ROWS*i,
                            SCREEN_WIDTH/SHOP_COLUMNS,
                            (SCREEN_HEIGHT-20)/SHOP_ROWS,
                            13)

    @staticmethod
    def center_text(text, page_width, y_coord, text_color, char_width=pyxel.FONT_WIDTH):
        """Helper function for calcuating the start x value for centered text."""

        text_width = len(text) * char_width
        pyxel.text((page_width - text_width) // 2, y_coord, text, text_color)

App()
