"""Main file for working title Not a Place of Honor, a game developed for itch.io's Historical Game Jam 3"""

from enum import Enum
import copy
import pyxel
import random
from simulation_screen import SimulationScreen
from util import center_text
from const import SCREEN_WIDTH, SCREEN_HEIGHT
from shop import Shop
from player import Player
from map import Map
import marker
import simulate
import button
import tips

YEARS_IN_PHASE=400
YEARS_TO_WIN=10000

class Screen(Enum):
    """An enum containing all possible screens in the game"""
    TITLE = "title"
    INTRO = "intro"
    DIRECTIONS = "directions"
    SHOP = "shop"
    MAP = "map"
    SIMULATION = "simulation"
    RESULTS = "results"
    TIP = "tip"

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
        self.map = Map({"mining":1, "archaeology":1, "dams":1, "teens":1, "tunnels":1})
        self.which_tip_index = None
        self.available_tips = list(range(19)) #19 possible tips to share with player
        self.continue_button = button.Button(
            x_coord=SCREEN_WIDTH/2-30,
            y_coord=180,
            width=60,
            height=20,
            text="CONTINUE",
            button_color=0
        )
        self.simulation_screen = None
        pyxel.load("justmessingaround.pyxres")
        pyxel.run(self.update, self.draw)


    def reset_game(self):
        """Resets state to the beginning of a new game"""
        self.player = Player()
        self.map = Map({"mining":1, "archaeology":1, "dams":1, "teens":1, "tunnels":1})
        self.available_tips = list(range(19)) #19 possible tips to share with player
        self.phase = 1
        self.simulations_run = 0
        self.latest_simulation_failed = False

    def update(self):
        """Updates game data each frame"""
        if self.screen == Screen.TITLE:
            self.update_title()
        if self.screen == Screen.INTRO:
            self.update_intro()
        if self.screen == Screen.DIRECTIONS:
            self.update_directions()
        if self.screen == Screen.SHOP:
            self.update_shop()
        if self.screen == Screen.MAP:
            self.update_map()
        if self.screen == Screen.SIMULATION:
            self.update_simulation()
        if self.screen == Screen.RESULTS:
            self.update_results()
        if self.screen == Screen.TIP:
            self.update_tip()

    def update_title(self):
        """Handles updates while the player is on the title screen"""
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.screen = Screen.INTRO

    def update_intro(self):
        """Handles updates while the player is on the title screen"""
        if self.continue_button.is_clicked():
            self.screen = Screen.DIRECTIONS

    def update_directions(self):
        if self.continue_button.is_clicked():
            self.screen = Screen.SHOP

    def update_shop(self):
        """Handles updates while the player is on the shop screen"""
        if self.shop is None:
            self.shop = Shop(self.marker_options, self.player)
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.shop.make_purchase(self.player)
            
        if self.shop.finish_button.is_clicked():
            self.screen = Screen.MAP
        if self.shop.finish_button.is_moused_over():
            self.shop.finish_button.button_color = pyxel.COLOR_LIME
        else: 
            self.shop.finish_button.button_color = pyxel.COLOR_GREEN

    def update_map(self):
        """Handles updates while the player is on the map screen"""
        self.map.update(self.player)

        if self.map.simulate_button.is_clicked():
            self.shop = None # Reset the shop
            print("Headed to simulation")
            self.screen = Screen.SIMULATION
            
        if self.map.simulate_button.is_moused_over():
            self.map.simulate_button.button_color = pyxel.COLOR_LIME
        else: 
            self.map.simulate_button.button_color = pyxel.COLOR_GREEN   

        if self.map.back_button.is_clicked():
            self.screen = Screen.SHOP
        if self.map.back_button.is_moused_over():
            self.map.back_button.button_color = pyxel.COLOR_LIGHTBLUE
        else: 
            self.map.back_button.button_color = pyxel.COLOR_DARKBLUE 


    def update_simulation(self):
        """Handles updates while the players is on the simulation screen"""
        if self.simulations_run < self.phase:
            self.latest_simulation_failed, event_log, map_log, death_margins = simulate.simulate(self.phase*YEARS_IN_PHASE,
                                                                                  self.map.map,
                                                                                  self.player.global_buffs)
            print(death_margins)
            Map(death_margins).cells = []
            self.simulations_run += 1
            self.simulation_screen = SimulationScreen(copy.deepcopy(self.map), event_log, map_log, death_margins)

        self.simulation_screen.update(self.player)
        if self.simulation_screen.done:
            self.screen = Screen.RESULTS

    def update_results(self):
        """Handles updates while the players is on the results screen"""
        if self.continue_button.is_clicked():
            if self.latest_simulation_failed or self.phase == YEARS_TO_WIN//YEARS_IN_PHASE:
                self.reset_game()
                self.screen = Screen.TITLE
            else:
                self.phase += 1
                self.player.add_funding(100000)
                self.screen = Screen.TIP

    def update_tip(self):
        if self.which_tip_index is None and len(self.available_tips) != 0: #make sure array of available tips isn't empty
            self.which_tip_index = random.randint(0,len(self.available_tips)-1) #select a random tip index

        if self.continue_button.is_clicked(): #remove the tip from the array of possible tips after it's been seen
            self.screen = Screen.SHOP
            if self.which_tip_index is not None:
                del self.available_tips[self.which_tip_index]
            self.which_tip_index = None
            #print("SIZE OF TIPS %d", len(self.available_tips))

    def draw(self):
        """Draws frame each frame"""
        if self.screen == Screen.TITLE:
            self.draw_title()
        elif self.screen == Screen.INTRO:
            self.draw_intro()
        elif self.screen == Screen.DIRECTIONS:
            self.draw_directions()
        elif self.screen == Screen.SHOP:
            self.draw_shop()
        elif self.screen == Screen.MAP:
            self.draw_map()
        elif self.screen == Screen.SIMULATION:
            self.draw_simulation()
        elif self.screen == Screen.RESULTS:
            self.draw_results()
        elif self.screen == Screen.TIP:
            self.draw_tip()

    def draw_title(self): #pylint: disable=no-self-use
        """Draws frames while the player is on the title screen"""
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.mouse(visible=False)
        pyxel.blt(0, 0, 2, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        center_text("Not a Place of Honor", page_width=SCREEN_WIDTH, y_coord=66, text_color=pyxel.COLOR_WHITE)
        center_text("- PRESS ENTER TO START -", page_width=SCREEN_WIDTH, y_coord=126, text_color=pyxel.COLOR_WHITE)

    def draw_intro(self): 
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.mouse(visible=True)
        center_text("Doctor!  I\'m glad you\'re here!", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        self.continue_button.draw()

    def draw_directions(self): 
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.mouse(visible=True)
        center_text("To start, we\'ll give you a budget of $X.", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        self.continue_button.draw()


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
        self.simulation_screen.draw(self.player)

    def draw_results(self):
        """Draws frames while the player is on the results screen"""
        pyxel.cls(pyxel.COLOR_BLACK)

        pyxel.mouse(visible=True)
        if self.simulations_run < self.phase:
            center_text("Simulating...", SCREEN_WIDTH, SCREEN_HEIGHT//2, pyxel.COLOR_WHITE)
        elif self.latest_simulation_failed:
            center_text("Waste Repository Breached. Game Over.", SCREEN_WIDTH, SCREEN_HEIGHT//2, pyxel.COLOR_WHITE)
            self.continue_button.draw()
        else:
            if self.phase == YEARS_TO_WIN//YEARS_IN_PHASE:
                center_text("YOU WIN!", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
                center_text("Your facility went 10,000 years undisturbed", SCREEN_WIDTH,
                            SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
                self.continue_button.draw()
            else:
                center_text("Your facility went " + str(self.phase*YEARS_IN_PHASE) + " years undisturbed",
                            SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
                center_text("You are awarded a larger budget to try and last " + \
                            str((self.phase+1)*YEARS_IN_PHASE) + " years",
                            SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
                self.continue_button.draw()
    
    def draw_tip(self):
        pyxel.cls(pyxel.COLOR_BLACK)

        if self.which_tip_index is not None:
            chosen_tip = self.available_tips[self.which_tip_index]
            tips.draw_chosen_tip(chosen_tip)
            self.continue_button.draw()
        else: self.screen = Screen.SHOP


App()
