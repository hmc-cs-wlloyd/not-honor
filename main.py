"""Main file for working title Not a Place of Honor, a game developed for itch.io's Historical Game Jam 3"""

from enum import Enum
from dataclasses import dataclass
from random import shuffle
import pyxel
import marker
import button
import simulate

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

ICON_WIDTH = 16
ICON_HEIGHT = 16

SHOP_COLUMNS = 2
SHOP_ROWS = 3
SHOP_TOP_OFFSET=20
SHOP_BOTTOM_OFFSET=80

YEARS_IN_PHASE=400
YEARS_TO_WIN=10000

class Screen(Enum):
    """An enum containing all possible screens in the game"""
    TITLE = "title"
    SHOP = "shop"
    SIMULATION = "simulation"

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
        pyxel.blt(self.x_coord + self.width // 2 - ICON_WIDTH // 2,
                self.y_coord + self.height // 2 - ICON_HEIGHT // 2,
                0,
                marker.markers[self.marker_on_shelf].icon_coords[0],
                marker.markers[self.marker_on_shelf].icon_coords[1],
                ICON_WIDTH,
                ICON_HEIGHT
        )
        if self.is_mouse_on_shelf():
            pyxel.text(0,
                    SCREEN_HEIGHT-SHOP_BOTTOM_OFFSET,
                    marker.markers[self.marker_on_shelf].description,
                    pyxel.COLOR_WHITE)
        if self.is_sold:
            center_text(text="Sold",
                page_width=self.width,
                y_coord=self.y_coord+self.height/2,
                text_color=pyxel.COLOR_RED,
                x_coord=self.x_coord)

class Shop:
    """A class representing an instance of the shop. Consists of a list of shelves with markers for sale on them"""
    def __init__(self, marker_options, player_inventory):
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
        available_marker_options = [marker for marker in marker_options if marker not in player_inventory]
        shuffle(available_marker_options)
        for i in range(SHOP_ROWS):
            for j in range(SHOP_COLUMNS):
                if 2*i+j < len(available_marker_options):
                    self.shelves.append(Shelf(x_coord=SCREEN_WIDTH//SHOP_COLUMNS * j,
                        y_coord=SHOP_TOP_OFFSET + ((SCREEN_HEIGHT-SHOP_TOP_OFFSET-SHOP_BOTTOM_OFFSET)//SHOP_ROWS)*i,
                        width=SCREEN_WIDTH//SHOP_COLUMNS,
                        height=(SCREEN_HEIGHT-SHOP_TOP_OFFSET-SHOP_BOTTOM_OFFSET)//SHOP_ROWS,
                        marker_on_shelf=available_marker_options[2*i+j],
                        sticker_price=marker.markers[available_marker_options[2*i+j]].base_cost
                    ))

    def draw(self, player):
        """Draws the shop to the screen"""
        center_text("Remaining Budget: $" + str(player.funding),
                page_width=SCREEN_WIDTH,
                y_coord=10,
                text_color=pyxel.COLOR_WHITE)
        self.inventory_button.draw()
        self.finish_button.draw()
        if self.inventory_button.is_moused_over():
            player.draw_inventory(0, SCREEN_HEIGHT-SHOP_BOTTOM_OFFSET, SCREEN_WIDTH, SHOP_BOTTOM_OFFSET)
        for shelf in self.shelves:
            shelf.draw()


    def make_purchase(self, available_funds):
        """Purchases for the player whatever is currently under their mouse"""
        for shelf in self.shelves:
            if (not shelf.is_sold) and available_funds >= shelf.sticker_price and shelf.is_mouse_on_shelf():
                shelf.is_sold = True
                return shelf.sticker_price
        return 0

class Player:
    """A class representing the player character"""
    def __init__(self):
        self.funding = 100000
        self.inventory = []

    def add_funding(self, funding_to_add):
        """Adds to the player's available funding"""
        self.funding += funding_to_add

    def add_inventory(self, new_markers):
        """Adds a list of markers to the player's inventory"""
        self.inventory += new_markers

    def draw_inventory(self, x_coord, y_coord, width, height):
        """Draws the icons of each item in the player's inventory to the screen starting at x, y in a region of
        width x length"""
        row_count = 0
        for i in range(len(self.inventory)):
            if i*ICON_WIDTH-row_count*(width//ICON_WIDTH) > width:
                row_count += i
            if (row_count+1)*ICON_HEIGHT > height:
                break
            pyxel.blt(x_coord+(i*ICON_WIDTH), y_coord+(row_count+ICON_HEIGHT), 0,
                      marker.markers[self.inventory[i]].icon_coords[0],
                      marker.markers[self.inventory[i]].icon_coords[1], ICON_WIDTH, ICON_HEIGHT)

class App: #pylint: disable=too-many-instance-attributes
    """Class to run the game itself"""
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Not a Place of Honor")
        self.screen = Screen.TITLE
        self.shop = None
        self.marker_options = marker.get_marker_keys()
        self.phase = 1
        self.simulations_run = 0
        self.latest_simulation_failed = False
        self.player = Player()

        pyxel.load("justmessingaround.pyxres")
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        """Resets state to the beginning of a new game"""
        self.player = Player()
        self.phase = 1
        self.simulations_run = 0
        self.latest_simulation_failed = False

    def update(self):
        """Updates game data each frame"""
        if self.screen == Screen.TITLE:
            self.update_title()
        if self.screen == Screen.SHOP:
            self.update_shop()
        if self.screen == Screen.SIMULATION:
            self.update_simulation()

    def draw(self):
        """Draws frame each frame"""
        if self.screen == Screen.TITLE:
            self.draw_title()
        elif self.screen == Screen.SHOP:
            self.draw_shop()
        elif self.screen == Screen.SIMULATION:
            self.draw_map()

    def update_title(self):
        """Handles updates while the player is on the title screen"""
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.screen = Screen.SHOP

    def update_shop(self):
        """Handles updates while the player is on the shop screen"""
        if self.shop is None:
            self.shop = Shop(self.marker_options, self.player.inventory)
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.player.add_funding(-1*self.shop.make_purchase(self.player.funding))
        if self.shop.finish_button.is_clicked():
            self.player.add_inventory([shelf.marker_on_shelf for shelf in self.shop.shelves if shelf.is_sold])
            self.shop = None
            self.screen = Screen.SIMULATION

    def update_simulation(self):
        """Handles updates while the players is on the simulation screen"""
        if self.simulations_run < self.phase:
            self.latest_simulation_failed, simulation_log = simulate.simulate(self.phase*YEARS_IN_PHASE,
                                                                              self.player.inventory)
            print(simulation_log)
            self.simulations_run += 1
        if pyxel.btnp(pyxel.KEY_ENTER):
            if self.latest_simulation_failed or self.phase == YEARS_TO_WIN//YEARS_IN_PHASE:
                self.reset_game()
                self.screen = Screen.TITLE
            else:
                self.phase += 1
                self.player.add_funding(100000)
                self.screen = Screen.SHOP


    def draw_title(self): #pylint: disable=no-self-use
        """Draws frames while the player is on the title screen"""
        pyxel.cls(pyxel.COLOR_BLACK)
        center_text("Not a Place of Honor", page_width=SCREEN_WIDTH, y_coord=66, text_color=pyxel.COLOR_WHITE)
        center_text("- PRESS ENTER TO START -", page_width=SCREEN_WIDTH, y_coord=126, text_color=pyxel.COLOR_WHITE)

    def draw_shop(self):
        """Draws frames while the player is on the shop screen"""
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.mouse(visible=True)

        if self.shop is not None:
            self.shop.draw(self.player)

    def draw_map(self):
        """Draws frames while the player is on the map screen"""
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.mouse(visible=False)
        if self.simulations_run < self.phase:
            center_text("Simulating...", SCREEN_WIDTH, SCREEN_HEIGHT//2, pyxel.COLOR_WHITE)
        elif self.latest_simulation_failed:
            center_text("Waste Repository Breached. Game Over.", SCREEN_WIDTH, SCREEN_HEIGHT//2, pyxel.COLOR_WHITE)
            center_text("- PRESS ENTER TO CONTINUE -", page_width=SCREEN_WIDTH, y_coord=3*SCREEN_HEIGHT//4,
                        text_color=pyxel.COLOR_WHITE)
        else:
            if self.phase == YEARS_TO_WIN//YEARS_IN_PHASE:
                center_text("YOU WIN!", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
                center_text("Your facility went 10,000 years undisturbed", SCREEN_WIDTH,
                            SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
                center_text("- PRESS ENTER TO CONTINUE -", page_width=SCREEN_WIDTH, y_coord=3*SCREEN_HEIGHT//4,
                            text_color=pyxel.COLOR_WHITE)
            else:
                center_text("Your facility went " + str(self.phase*YEARS_IN_PHASE) + " years undisturbed",
                            SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
                center_text("You are awarded a larger budget to try and last " + \
                            str((self.phase+1)*YEARS_IN_PHASE) + " years",
                            SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
                center_text("- PRESS ENTER TO CONTINUE -", page_width=SCREEN_WIDTH, y_coord=3*SCREEN_HEIGHT//4,
                            text_color=pyxel.COLOR_WHITE)

def center_text(text, page_width, y_coord, text_color, x_coord=0, char_width=pyxel.FONT_WIDTH): #pylint: disable=too-many-arguments
    """Helper function for calcuating the start x value for centered text."""

    text_width = len(text) * char_width
    pyxel.text(x_coord+(page_width - text_width) // 2, y_coord, text, text_color)

App()
