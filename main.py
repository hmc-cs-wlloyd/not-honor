"""Main file for working title Not a Place of Honor, a game developed for itch.io's Historical Game Jam 3"""

from enum import Enum
import pyxel
from util import center_text
from const import SCREEN_WIDTH, SCREEN_HEIGHT
from shop import Shop
from player import Player
from map import Map
import marker
import simulate

YEARS_IN_PHASE=400
YEARS_TO_WIN=10000

class Screen(Enum):
    """An enum containing all possible screens in the game"""
    TITLE = "title"
    SHOP = "shop"
    MAP = "map"
    SIMULATION = "simulation"
    RESULTS = "results"

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
        self.map = Map()
        pyxel.load("justmessingaround.pyxres")
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        """Resets state to the beginning of a new game"""
        self.player = Player()
        self.map = Map()
        self.phase = 1
        self.simulations_run = 0
        self.latest_simulation_failed = False

    def update(self):
        """Updates game data each frame"""
        if self.screen == Screen.TITLE:
            self.update_title()
        if self.screen == Screen.SHOP:
            self.update_shop()
        if self.screen == Screen.MAP:
            self.update_map()
        if self.screen == Screen.SIMULATION:
            self.update_simulation()
        if self.screen == Screen.RESULTS:
            self.update_results()

    def update_title(self):
        """Handles updates while the player is on the title screen"""
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.screen = Screen.SHOP

    def update_shop(self):
        """Handles updates while the player is on the shop screen"""
        if self.shop is None:
            self.shop = Shop(self.marker_options, self.player)
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.shop.make_purchase(self.player)
        if self.shop.finish_button.is_clicked():
            self.screen = Screen.MAP

    def update_map(self):
        """Handles updates while the player is on the map screen"""
        self.map.update(self.player)
        if self.map.simulate_button.is_clicked():
            self.shop = None # Reset the shop
            print("Headed to simulation")
            self.screen = Screen.SIMULATION
        if self.map.back_button.is_clicked():
            self.screen = Screen.SHOP

    def update_simulation(self):
        """Handles updates while the players is on the simulation screen"""
        self.map.update(self.player, is_simulation=True)
        if self.map.next_button.is_clicked():
            print("Headed to results")
            self.screen = Screen.RESULTS

    def update_results(self):
        """Handles updates while the players is on the results screen"""
        if self.simulations_run < self.phase:
            self.latest_simulation_failed, simulation_log = simulate.simulate(self.phase*YEARS_IN_PHASE,
                                                                              self.map.map,
                                                                              self.player.global_buffs)
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

    def draw(self):
        """Draws frame each frame"""
        if self.screen == Screen.TITLE:
            self.draw_title()
        elif self.screen == Screen.SHOP:
            self.draw_shop()
        elif self.screen == Screen.MAP:
            self.draw_map()
        elif self.screen == Screen.SIMULATION:
            self.draw_simulation()
        elif self.screen == Screen.RESULTS:
            self.draw_results()

    def draw_title(self): #pylint: disable=no-self-use
        """Draws frames while the player is on the title screen"""
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.mouse(visible=False)
        pyxel.blt(0, 0, 2, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
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
        pyxel.mouse(visible=True)
        self.map.draw(self.player)

    def draw_simulation(self):
        """Draws frames while the player is on the simulation screen"""
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.mouse(visible=True)
        self.map.draw(self.player, is_simulation=True)

    def draw_results(self):
        """Draws frames while the player is on the results screen"""
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

App()
