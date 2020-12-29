"""Main file for working title Not a Place of Honor, a game developed for itch.io's Historical Game Jam 3"""

from enum import Enum
from dataclasses import dataclass
from random import shuffle
import pyxel
import marker
import button

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

SHOP_COLUMNS = 2
SHOP_ROWS = 3
SHOP_TOP_OFFSET=20
SHOP_BOTTOM_OFFSET=80

class Screen(Enum):
    """An enum containing all possible screens in the game"""
    TITLE = "title"
    SHOP = "shop"
    MAP = "map"

@dataclass
class Shelf:
    """A class representing a shelf in the shop. Shelves contain markers for sale and their current prices"""
    x_coord: int
    y_coord: int
    width: int
    height: int
    marker_on_shelf: str
    sticker_price: int
    is_sold: bool=False

    def is_mouse_on_shelf(self):
        """Returns true if the mouse is currently on the shelf"""
        return pyxel.mouse_x > self.x_coord and \
                pyxel.mouse_x < self.x_coord + self.width and \
                pyxel.mouse_y > self.y_coord and \
                pyxel.mouse_y < self.y_coord + self.height
    def draw(self):
        """Draws the shelf and its contents to the screen"""
        pyxel.rectb(self.x_coord, self.y_coord, self.width, self.height, pyxel.COLOR_GRAY)
        center_text(text=marker.markers[self.marker_on_shelf].name,
                page_width=self.width,
                y_coord=self.y_coord+3,
                text_color=pyxel.COLOR_WHITE,
                x_coord=self.x_coord)
        center_text(text="Price: $" + str(self.sticker_price),
                page_width=self.width,
                y_coord=self.y_coord+self.height-7,
                text_color=pyxel.COLOR_WHITE,
                x_coord=self.x_coord)
        if self.is_mouse_on_shelf():
            pyxel.text(0,
                    SCREEN_HEIGHT-SHOP_BOTTOM_OFFSET,
                    marker.markers[self.marker_on_shelf].description,
                    pyxel.COLOR_WHITE)
        if self.is_sold:
            center_text(text="Sold",
                page_width=self.width,
                y_coord=self.y_coord+self.height/2,
                text_color=pyxel.COLOR_WHITE,
                x_coord=self.x_coord)

class Shop:
    """A class representing an instance of the shop. Consists of a list of shelves with markers for sale on them"""
    def __init__(self, marker_options):
        self.shelves = []
        self.finish_button = button.Button(
            x_coord=SCREEN_WIDTH - 35,
            y_coord=SHOP_TOP_OFFSET/10,
            width=30,
            height=9*SHOP_TOP_OFFSET/10,
            text="Finish",
            button_color=pyxel.COLOR_GRAY
        )
        self.inventory_button = button.Button(
            x_coord=5,
            y_coord=SHOP_TOP_OFFSET/10,
            width=45,
            height=9*SHOP_TOP_OFFSET/10,
            text="Inventory",
            button_color=pyxel.COLOR_GRAY
        )
        shuffle(marker_options)
        for i in range(SHOP_ROWS):
            for j in range(SHOP_COLUMNS):
                if 2*i+j < len(marker_options):
                    self.shelves.append(Shelf(x_coord=SCREEN_WIDTH/SHOP_COLUMNS * j,
                        y_coord=SHOP_TOP_OFFSET + ((SCREEN_HEIGHT-SHOP_TOP_OFFSET-SHOP_BOTTOM_OFFSET)/SHOP_ROWS)*i,
                        width=SCREEN_WIDTH/SHOP_COLUMNS,
                        height=(SCREEN_HEIGHT-SHOP_TOP_OFFSET-SHOP_BOTTOM_OFFSET)/SHOP_ROWS,
                        marker_on_shelf=marker_options[2*i+j],
                        sticker_price=marker.markers[marker_options[2*i+j]].base_cost
                    ))

    def draw(self, player_funding):
        """Draws the shop to the screen"""
        center_text("Remaining Budget: $" + str(player_funding),
                page_width=SCREEN_WIDTH,
                y_coord=10,
                text_color=pyxel.COLOR_WHITE)
        self.inventory_button.draw()
        self.finish_button.draw()
        for shelf in self.shelves:
            shelf.draw()

    def make_purchase(self, available_funds):
        """Purchases for the player whatever is currently under their mouse"""
        for shelf in self.shelves:
            if (not shelf.is_sold) and available_funds >= shelf.sticker_price and shelf.is_mouse_on_shelf():
                shelf.is_sold = True
                return shelf.sticker_price
        return 0

class App:
    """Class to run the game itself"""
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Not a Place of Honor")
        self.player_funding = 1000000
        self.screen = Screen.TITLE
        self.shop = None
        self.marker_options = marker.get_marker_keys()
        self.player_inventory = []

        pyxel.run(self.update, self.draw)

    def update(self):
        """Updates game data each frame"""
        if self.screen == Screen.TITLE:
            self.update_title()
        if self.screen == Screen.SHOP:
            self.update_shop()

    def draw(self):
        """Draws frame each frame"""
        if self.screen == Screen.TITLE:
            self.draw_title()
        elif self.screen == Screen.SHOP:
            self.draw_shop()
        elif self.screen == Screen.MAP:
            self.draw_map()

    def update_title(self):
        """Handles updates while the player is on the title screen"""
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.screen = Screen.SHOP

    def update_shop(self):
        """Handles updates while the player is on the shop screen"""
        if self.shop is None:
            self.shop = Shop(self.marker_options)
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.player_funding -= self.shop.make_purchase(self.player_funding)
        if self.shop.finish_button.is_clicked():
            self.player_inventory += [shelf.marker_on_shelf for shelf in self.shop.shelves if shelf.is_sold]
            self.shop = None
            self.screen = Screen.MAP

    def draw_title(self): #pylint: disable=no-self-use
        """Draws frames while the player is on the title screen"""
        center_text("Not a Place of Honor", page_width=SCREEN_WIDTH, y_coord=66, text_color=pyxel.COLOR_WHITE)
        center_text("- PRESS ENTER TO START -", page_width=SCREEN_WIDTH, y_coord=126, text_color=pyxel.COLOR_WHITE)

    def draw_shop(self):
        """Draws frames while the player is on the shop screen"""
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.mouse(visible=True)

        self.shop.draw(self.player_funding)

    def draw_map(self):
        """Draws frames while the player is on the map screen"""
        print(self.player_inventory)
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.mouse(visible=False)

def center_text(text, page_width, y_coord, text_color, x_coord=0, char_width=pyxel.FONT_WIDTH): #pylint: disable=too-many-arguments
    """Helper function for calcuating the start x value for centered text."""

    text_width = len(text) * char_width
    pyxel.text(x_coord+(page_width - text_width) // 2, y_coord, text, text_color)

App()
