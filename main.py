"""Main file for working title Not a Place of Honor, a game developed for itch.io's Historical Game Jam 3"""

from enum import Enum
import copy
import random
import pyxel
from simulation_screen import SimulationScreen
from util import center_text
from const import SCREEN_WIDTH, SCREEN_HEIGHT
from shop import Shop, STAT_BAR_SIDE_MARGIN, STAT_BAR_HEIGHT, HALF_STAT_BAR_WIDTH
from player import Player
from map import Map
import marker
import simulate
import button
import tips

YEARS_IN_PHASE=400
YEARS_TO_WIN=10000
not_playing_result_music = True
not_playing_title_music = True

class Screen(Enum):
    """An enum containing all possible screens in the game"""
    TITLE = "title"
    INTRO_1 = "intro_1"
    INTRO_2 = "intro_2"
    INTRO_3 = "intro_3"
    DIRECTIONS_1 = "directions_1"
    DIRECTIONS_2 = "directions_2"
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
        global not_playing_title_music 
        not_playing_title_music = True
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
        if self.screen == Screen.INTRO_1:
            self.update_intro_1()
        if self.screen == Screen.INTRO_2:
            self.update_intro_2()
        if self.screen == Screen.INTRO_3:
            self.update_intro_3()
        if self.screen == Screen.DIRECTIONS_1:
            self.update_directions_1()
        if self.screen == Screen.DIRECTIONS_2:
            self.update_directions_2()
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
        global not_playing_title_music
        if not_playing_title_music:
                    pyxel.playm(0, loop=True)
                    not_playing_title_music= False
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.screen = Screen.INTRO_1

    def update_intro_1(self):
        """Handles updates while the player is on the title screen"""
        if self.continue_button.is_clicked():
            self.screen = Screen.INTRO_2
        if self.continue_button.is_moused_over():
            self.continue_button.button_color = pyxel.COLOR_LIGHTBLUE
        else: 
            self.continue_button.button_color = pyxel.COLOR_DARKBLUE

    def update_intro_2(self):
        if self.continue_button.is_clicked():
            self.screen = Screen.INTRO_3
        if self.continue_button.is_moused_over():
            self.continue_button.button_color = pyxel.COLOR_LIGHTBLUE
        else: 
            self.continue_button.button_color = pyxel.COLOR_DARKBLUE

    def update_intro_3(self):
        if self.continue_button.is_clicked():
            self.screen = Screen.DIRECTIONS_1
        if self.continue_button.is_moused_over():
            self.continue_button.button_color = pyxel.COLOR_LIGHTBLUE
        else: 
            self.continue_button.button_color = pyxel.COLOR_DARKBLUE

    def update_directions_1(self):
        if self.continue_button.is_clicked():
            self.screen = Screen.DIRECTIONS_2
        if self.continue_button.is_moused_over():
            self.continue_button.button_color = pyxel.COLOR_LIGHTBLUE
        else: 
            self.continue_button.button_color = pyxel.COLOR_DARKBLUE

    def update_directions_2(self):
        if self.continue_button.is_clicked():
            self.screen = Screen.SHOP
            not_playing_title_music = True
        if self.continue_button.is_moused_over():
            self.continue_button.button_color = pyxel.COLOR_LIGHTBLUE
        else: 
            self.continue_button.button_color = pyxel.COLOR_DARKBLUE

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

        if self.map.directions_button.is_moused_over():
            self.map.show_directions = True
            self.map.directions_button.button_color = pyxel.COLOR_PEACH
        else: 
            self.map.show_directions = False
            self.map.directions_button.button_color = pyxel.COLOR_ORANGE   


    def update_simulation(self):
        """Handles updates while the players is on the simulation screen"""
        if self.simulations_run < self.phase:
            self.latest_simulation_failed, event_log, map_log, death_margins, stats_list = simulate.simulate(self.phase*YEARS_IN_PHASE,
                                                                                            self.map.map,
                                                                                            self.player.global_buffs)
            print(death_margins)
            Map(death_margins).cells = []
            self.simulations_run += 1
            self.simulation_screen = SimulationScreen(copy.deepcopy(self.map), event_log, map_log, death_margins, stats_list)

        self.simulation_screen.update(self.player)
        if self.simulation_screen.done:
            self.screen = Screen.RESULTS

    def update_results(self):
        """Handles updates while the players is on the results screen"""
        global not_playing_result_music
        if self.continue_button.is_clicked():
            if self.latest_simulation_failed or self.phase == YEARS_TO_WIN//YEARS_IN_PHASE:
                not_playing_result_music = True
                self.reset_game()
                self.screen = Screen.TITLE
            else:
                not_playing_result_music = True
                self.phase += 1
                self.player.add_funding(100000)
                self.screen = Screen.TIP
        if self.continue_button.is_moused_over():
            self.continue_button.button_color = pyxel.COLOR_LIGHTBLUE
        else: 
            self.continue_button.button_color = pyxel.COLOR_DARKBLUE

    def update_tip(self):
        if self.which_tip_index is None and len(self.available_tips) != 0: #make sure array of available tips isn't empty
            self.which_tip_index = random.randint(0,len(self.available_tips)-1) #select a random tip index

        if self.continue_button.is_clicked(): #remove the tip from the array of possible tips after it's been seen
            self.screen = Screen.SHOP
            if self.which_tip_index is not None:
                del self.available_tips[self.which_tip_index]
            self.which_tip_index = None
            #print("SIZE OF TIPS %d", len(self.available_tips))
        if self.continue_button.is_moused_over():
            self.continue_button.button_color = pyxel.COLOR_LIGHTBLUE
        else: 
            self.continue_button.button_color = pyxel.COLOR_DARKBLUE

    def draw(self):
        """Draws frame each frame"""
        if self.screen == Screen.TITLE:
            self.draw_title()
        elif self.screen == Screen.INTRO_1:
            self.draw_intro_1()
        elif self.screen == Screen.INTRO_2:
            self.draw_intro_2()
        elif self.screen == Screen.INTRO_3:
            self.draw_intro_3()
        elif self.screen == Screen.DIRECTIONS_1:
            self.draw_directions_1()
        elif self.screen == Screen.DIRECTIONS_2:
            self.draw_directions_2()
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
        center_text("Not a Place of Honor", page_width=SCREEN_WIDTH-2, y_coord=85, text_color=pyxel.COLOR_WHITE)
        center_text("Not a Place of Honor", page_width=SCREEN_WIDTH, y_coord=86, text_color=pyxel.COLOR_BLACK)
        center_text("- PRESS ENTER TO START -", page_width=SCREEN_WIDTH, y_coord=160, text_color=pyxel.COLOR_BLACK)

    def draw_intro_1(self): 
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.mouse(visible=True)
        center_text("Doctor!  I\'m glad you\'re here!", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text('Thanks for coming all this way to meet with the team for', SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("the Waste Isolation Pilot Plant. We\'re simulating how to", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2), pyxel.COLOR_WHITE)
        center_text("keep future generations of humans (who may not understand", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*3), pyxel.COLOR_WHITE)
        center_text("English) away from nuclear waste sites and", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*4), pyxel.COLOR_WHITE)
        center_text("we need your advice!", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*5), pyxel.COLOR_WHITE)
        self.continue_button.draw()

    def draw_intro_2(self): 
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.mouse(visible=True)
        center_text("Our scientists have found that humans behave differently", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT-16, pyxel.COLOR_WHITE)
        center_text('towards a place based on five observable aspects', SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT-20, pyxel.COLOR_WHITE)
        pyxel.text(8,SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2)-8, "Land Usability - ", pyxel.COLOR_YELLOW)
        pyxel.text(78, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2)-8, "How usable the site appears to be", pyxel.COLOR_WHITE)
        pyxel.text(8, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*3)-8, "Visibility - ", pyxel.COLOR_YELLOW)
        pyxel.text(62, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*3)-8, "How visually noticeable the site is", pyxel.COLOR_WHITE)
        pyxel.text(8, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*4)-8, "Respectability - ", pyxel.COLOR_YELLOW)
        pyxel.text(78, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*4)-8, "How likely visitors are to preserve the site", pyxel.COLOR_WHITE)
        pyxel.text(8, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*5)-8, "Likability - ", pyxel.COLOR_YELLOW)
        pyxel.text(62, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*5)-8, "How charming the site is", pyxel.COLOR_WHITE)
        pyxel.text(8, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*6)-8, "Message Clarity - ", pyxel.COLOR_YELLOW)
        pyxel.text(78, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*6)-8, "How well the site is communicating to\nstay away", pyxel.COLOR_WHITE)
        self.continue_button.draw()

    def draw_intro_3(self): 
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.mouse(visible=True)
        center_text("You\'ll also find that there are different types of humans", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT-64, pyxel.COLOR_WHITE)
        center_text('who will visit the simulated nuclear site. They have', SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT-60, pyxel.COLOR_WHITE)
        center_text("different interests in regard to the five aspects,", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2)-60, pyxel.COLOR_WHITE)
        center_text("so you\'ll have to put up the right defenses to keep", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*3)-60, pyxel.COLOR_WHITE)
        center_text("them all away!", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*4)-60, pyxel.COLOR_WHITE)
        center_text("For example...", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*4)-44, pyxel.COLOR_WHITE)

        pyxel.blt((SCREEN_WIDTH/2)-(16*3)-8, SCREEN_HEIGHT//2-4, 0, 0, 32, 16, 16)
        pyxel.blt(SCREEN_WIDTH/2-8, SCREEN_HEIGHT//2-4, 0, 0, 32, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)+(16*3)-8, SCREEN_HEIGHT//2-4, 0, 0, 32, 16, 16)

        pyxel.text(16, SCREEN_HEIGHT//2+22, "Archaeologists", pyxel.COLOR_YELLOW)
        pyxel.text(16+44, SCREEN_HEIGHT//2+22, "    like to dig up open spaces", pyxel.COLOR_WHITE) 
        center_text("but will preserve spaces with high respectability", SCREEN_WIDTH, SCREEN_HEIGHT//2+22+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)

        self.continue_button.draw()

    def draw_directions_1(self): 
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.mouse(visible=True)
        center_text("Remaining Budget: $" + str(self.player.funding),
                page_width=SCREEN_WIDTH,
                y_coord=10,
                text_color=pyxel.COLOR_YELLOW)
        center_text("To start, we\'ll give you a budget of $100 million.", SCREEN_WIDTH, SCREEN_HEIGHT//2-72, pyxel.COLOR_WHITE)
        center_text('On the next page, you\'ll be able to buy items', SCREEN_WIDTH, SCREEN_HEIGHT//2-48, pyxel.COLOR_WHITE)
        center_text("to affect your simulation. Some items need to be placed", SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT-48, pyxel.COLOR_WHITE)
        center_text("and others will be applied as global social factors.", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2)-48, pyxel.COLOR_WHITE)

        #FOR AN EXAMPLE OF THE STAT BARS so they don't look scary the first time you see them
        for i in range(5): #keep plain gray bars on the screen outside of hover
            stat_to_present = 5
            if i == 0:
                stat_to_present = 5
                bar_label = " Land Use"
            elif i == 1: 
                stat_to_present = -3
                bar_label = "  Visible"
            elif i == 2: 
                stat_to_present = -8
                bar_label = "Respectable"
            elif i == 3: 
                stat_to_present = 9
                bar_label = " Likeable"
            elif i == 4: 
                stat_to_present = 4
                bar_label = " Clarity"

            if stat_to_present >= 0: #positive stat
                pyxel.rect(((SCREEN_WIDTH/5)*i)+STAT_BAR_SIDE_MARGIN+HALF_STAT_BAR_WIDTH, SCREEN_HEIGHT/2-12, stat_to_present*2, STAT_BAR_HEIGHT, pyxel.COLOR_GREEN)
                pyxel.rect(((SCREEN_WIDTH/5)*i)+STAT_BAR_SIDE_MARGIN+HALF_STAT_BAR_WIDTH+stat_to_present*2, SCREEN_HEIGHT/2-12, HALF_STAT_BAR_WIDTH-(stat_to_present*2), STAT_BAR_HEIGHT, pyxel.COLOR_NAVY)
                pyxel.rect(((SCREEN_WIDTH/5)*i)+STAT_BAR_SIDE_MARGIN, SCREEN_HEIGHT/2-12, HALF_STAT_BAR_WIDTH, STAT_BAR_HEIGHT, pyxel.COLOR_NAVY)
                pyxel.line(((SCREEN_WIDTH/5)*i)+STAT_BAR_SIDE_MARGIN+HALF_STAT_BAR_WIDTH, SCREEN_HEIGHT/2-12, ((SCREEN_WIDTH/5)*i)+STAT_BAR_SIDE_MARGIN+HALF_STAT_BAR_WIDTH, SCREEN_HEIGHT/2-12+8-1, pyxel.COLOR_YELLOW)
            else:#negative stat
                pyxel.rect(((SCREEN_WIDTH/5)*i)+STAT_BAR_SIDE_MARGIN+HALF_STAT_BAR_WIDTH+stat_to_present*2, SCREEN_HEIGHT/2-12, stat_to_present*-2, STAT_BAR_HEIGHT, pyxel.COLOR_RED)
                pyxel.rect(((SCREEN_WIDTH/5)*i)+STAT_BAR_SIDE_MARGIN, SCREEN_HEIGHT/2-12, HALF_STAT_BAR_WIDTH-(stat_to_present*-2), STAT_BAR_HEIGHT, pyxel.COLOR_NAVY)
                pyxel.rect(((SCREEN_WIDTH/5)*i)+STAT_BAR_SIDE_MARGIN+HALF_STAT_BAR_WIDTH, SCREEN_HEIGHT/2-12, HALF_STAT_BAR_WIDTH, STAT_BAR_HEIGHT, pyxel.COLOR_NAVY)
            pyxel.line(((SCREEN_WIDTH/5)*i)+STAT_BAR_SIDE_MARGIN+HALF_STAT_BAR_WIDTH, SCREEN_HEIGHT/2-12, ((SCREEN_WIDTH/5)*i)+STAT_BAR_SIDE_MARGIN+HALF_STAT_BAR_WIDTH, SCREEN_HEIGHT/2-12+8-1, pyxel.COLOR_YELLOW)
            pyxel.text(((SCREEN_WIDTH/5)*i)+STAT_BAR_SIDE_MARGIN, SCREEN_HEIGHT/2-12+8, bar_label, pyxel.COLOR_GRAY)
        
        center_text("Each item have different land usability, visibility,", SCREEN_WIDTH, SCREEN_HEIGHT//2+16, pyxel.COLOR_WHITE)
        center_text("respectability, likability and message clarity,", SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT+16, pyxel.COLOR_WHITE)
        center_text("so keep those in mind as you pick your strategy!", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2)+16, pyxel.COLOR_WHITE)

        self.continue_button.draw()

    def draw_directions_2(self): 
        pyxel.cls(pyxel.COLOR_BLACK)
        pyxel.mouse(visible=True)
        center_text("GOOD LUCK!", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_GREEN)
        center_text('After placing your purchased items, we\'ll begin', SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("the simulation! Let\'s make sure your design withstands", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2), pyxel.COLOR_WHITE)
        center_text("human intrusion for 400 years, then we\'ll try for", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*3), pyxel.COLOR_WHITE)
        center_text("longer and longer time spans! Also, I\'m sure some of", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*4), pyxel.COLOR_WHITE)
        center_text("the other scientists will want to talk to you...", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*5), pyxel.COLOR_WHITE)
        center_text("I\'ll let you know if I see anyone!", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*6), pyxel.COLOR_WHITE)
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
        global not_playing_result_music
        pyxel.mouse(visible=True)
        if self.simulations_run < self.phase:
            center_text("Simulating...", SCREEN_WIDTH, SCREEN_HEIGHT//2, pyxel.COLOR_WHITE)
        elif self.latest_simulation_failed:
            center_text("Waste Repository Breached. Game Over.", SCREEN_WIDTH, SCREEN_HEIGHT//2, pyxel.COLOR_WHITE)
            self.continue_button.draw()
            if not_playing_result_music:
                    pyxel.playm(4, loop=False)
                    not_playing_result_music= False
        else:
            if self.phase == YEARS_TO_WIN//YEARS_IN_PHASE:
                center_text("YOU WIN!", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
                center_text("Your facility went 10,000 years undisturbed", SCREEN_WIDTH,
                            SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
                self.continue_button.draw()
                if not_playing_result_music:
                    pyxel.playm(3, loop=False)
                    not_playing_result_music= False
                
            else:
                center_text("Your facility went " + str(self.phase*YEARS_IN_PHASE) + " years undisturbed",
                            SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
                center_text("You are awarded a larger budget to try and last " + \
                            str((self.phase+1)*YEARS_IN_PHASE) + " years",
                            SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
                self.continue_button.draw()
                if not_playing_result_music:
                    pyxel.playm(3, loop=False)
                    not_playing_result_music= False
    
    def draw_tip(self):
        pyxel.cls(pyxel.COLOR_BLACK)

        if self.which_tip_index is not None:
            chosen_tip = self.available_tips[self.which_tip_index]
            tips.draw_chosen_tip(chosen_tip)
            self.continue_button.draw()
        else: self.screen = Screen.SHOP


App()
