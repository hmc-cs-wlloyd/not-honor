"""A class representing the screen displaying an active simulation"""

import math
import pyxel
from const import ICON_WIDTH, ICON_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH, STAT_BAR_HEIGHT, STAT_BAR_SIDE_MARGIN, HALF_STAT_BAR_WIDTH
from util import center_text
from event import events

MAP_BOTTOM_MARGIN = 8 + ICON_HEIGHT*3
KEY_MARGIN=6

class SimulationScreen:
    """A class representing the simulation-in-progress screen"""
    def __init__(self, initial_map, events_from_simulation, maps_from_simulation, death_margins, stats_from_simulation):
        self.current_map = initial_map
        self.current_map.death_margins = death_margins
        print(death_margins)
        self.current_map.generate_visitors()
        self.current_event_index = 0
        self.events_from_simulation = events_from_simulation
        self.maps_from_simulation = maps_from_simulation
        self.stats_from_simulation = stats_from_simulation
        self.done = False
        self.show_visitors = False
        pyxel.playm(2,loop=True)

    def update(self, player):
        """Updates the simulation-in-progress screen"""
        if self.current_map.next_button.is_clicked():
            self.current_event_index += 1 #this will break stuff if the calling update() doesn't check and advance screen when appropriate
        if self.current_map.next_button.is_moused_over():
            self.current_map.next_button.button_color = pyxel.COLOR_LIGHTBLUE
        else:
            self.current_map.next_button.button_color = pyxel.COLOR_DARKBLUE

        if self.current_map.visitors_button.is_moused_over():
            self.show_visitors = True
            self.current_map.visitors_button.button_color = pyxel.COLOR_PEACH
        else:
            self.show_visitors = False
            self.current_map.visitors_button.button_color = pyxel.COLOR_ORANGE

        if self.current_event_index >= len(self.events_from_simulation):
            self.done = True
            return
        self.current_map.map = self.maps_from_simulation[self.current_event_index]
        self.current_map.update(player, is_simulation=True)

    def draw(self, player):
        """Draws the simulation-in-progress screen"""
        self.current_map.draw(player, is_simulation=True)

        stats_to_present = self.stats_from_simulation[self.current_event_index]
        for i in range(5):
            stat_to_present = stats_to_present[i]
            bar_label = ""
            if i == 0:
                bar_label = " Land Use"
            elif i == 1:
                bar_label = "  Visible"
            elif i == 2:
                bar_label = "Respectable"
            elif i == 3:
                bar_label = " Likeable"
            elif i == 4:
                bar_label = " Clarity"

            if stat_to_present >= 0: #positive stat
                #positive green
                pyxel.rect(((SCREEN_WIDTH//5)*i)+STAT_BAR_SIDE_MARGIN+HALF_STAT_BAR_WIDTH, SCREEN_HEIGHT-MAP_BOTTOM_MARGIN-6, math.ceil(stat_to_present*HALF_STAT_BAR_WIDTH), STAT_BAR_HEIGHT, pyxel.COLOR_GREEN)
                #remaining positive gray
                pyxel.rect(((SCREEN_WIDTH//5)*i)+STAT_BAR_SIDE_MARGIN+HALF_STAT_BAR_WIDTH+math.ceil(stat_to_present*HALF_STAT_BAR_WIDTH), SCREEN_HEIGHT-MAP_BOTTOM_MARGIN-6, HALF_STAT_BAR_WIDTH-(stat_to_present*HALF_STAT_BAR_WIDTH), STAT_BAR_HEIGHT, pyxel.COLOR_NAVY)
                #negative gray
                pyxel.rect(((SCREEN_WIDTH//5)*i)+STAT_BAR_SIDE_MARGIN, SCREEN_HEIGHT-MAP_BOTTOM_MARGIN-6, HALF_STAT_BAR_WIDTH, STAT_BAR_HEIGHT, pyxel.COLOR_NAVY)
                # yellow center line
                pyxel.line(((SCREEN_WIDTH//5)*i)+STAT_BAR_SIDE_MARGIN+HALF_STAT_BAR_WIDTH, SCREEN_HEIGHT-MAP_BOTTOM_MARGIN-6, ((SCREEN_WIDTH//5)*i)+STAT_BAR_SIDE_MARGIN+HALF_STAT_BAR_WIDTH, SCREEN_HEIGHT-MAP_BOTTOM_MARGIN-6+STAT_BAR_HEIGHT-1, pyxel.COLOR_YELLOW)
            else:#negative stat
                #negative red
                pyxel.rect(((SCREEN_WIDTH//5)*i)+STAT_BAR_SIDE_MARGIN+HALF_STAT_BAR_WIDTH+math.ceil(stat_to_present*HALF_STAT_BAR_WIDTH), SCREEN_HEIGHT-MAP_BOTTOM_MARGIN-6, -1*math.ceil(stat_to_present*HALF_STAT_BAR_WIDTH), STAT_BAR_HEIGHT, pyxel.COLOR_RED)
                #remaining negative gray
                pyxel.rect(((SCREEN_WIDTH//5)*i)+STAT_BAR_SIDE_MARGIN, SCREEN_HEIGHT-MAP_BOTTOM_MARGIN-6, HALF_STAT_BAR_WIDTH-(-1*math.ceil(stat_to_present*HALF_STAT_BAR_WIDTH)), STAT_BAR_HEIGHT, pyxel.COLOR_NAVY)
                #positive gray
                pyxel.rect(((SCREEN_WIDTH//5)*i)+STAT_BAR_SIDE_MARGIN+HALF_STAT_BAR_WIDTH, SCREEN_HEIGHT-MAP_BOTTOM_MARGIN-6, HALF_STAT_BAR_WIDTH, STAT_BAR_HEIGHT, pyxel.COLOR_NAVY)
                # yellow center line
                pyxel.line(((SCREEN_WIDTH//5)*i)+STAT_BAR_SIDE_MARGIN+HALF_STAT_BAR_WIDTH, SCREEN_HEIGHT-MAP_BOTTOM_MARGIN-6, ((SCREEN_WIDTH//5)*i)+STAT_BAR_SIDE_MARGIN+HALF_STAT_BAR_WIDTH, SCREEN_HEIGHT-MAP_BOTTOM_MARGIN-6+STAT_BAR_HEIGHT-1, pyxel.COLOR_YELLOW)

            pyxel.text(((SCREEN_WIDTH//5)*i)+STAT_BAR_SIDE_MARGIN, SCREEN_HEIGHT-MAP_BOTTOM_MARGIN-6+8, bar_label, pyxel.COLOR_GRAY)
        if self.events_from_simulation[self.current_event_index][1] != "null":
            event_message = str(self.events_from_simulation[self.current_event_index][0]) + ": " \
                                        + events[self.events_from_simulation[self.current_event_index][1]].description
            pyxel.blt(x=8,
                      y=SCREEN_HEIGHT-MAP_BOTTOM_MARGIN+ICON_HEIGHT//2+1,
                      img=events[self.events_from_simulation[self.current_event_index][1]].icon_image,
                      u=events[self.events_from_simulation[self.current_event_index][1]].icon_coords[0],
                      v=events[self.events_from_simulation[self.current_event_index][1]].icon_coords[1],
                      w=events[self.events_from_simulation[self.current_event_index][1]].icon_size[0],
                      h=events[self.events_from_simulation[self.current_event_index][1]].icon_size[1])
            center_text(event_message,
                        page_width=SCREEN_WIDTH-events[self.events_from_simulation[self.current_event_index][1]].icon_size[0],
                        x_coord=events[self.events_from_simulation[self.current_event_index][1]].icon_size[0],
                        y_coord = SCREEN_HEIGHT-MAP_BOTTOM_MARGIN+ICON_HEIGHT//2+1,
                        text_color=pyxel.COLOR_WHITE)
            #show explosion if you die
            if events[self.events_from_simulation[self.current_event_index][1]].fatal:
                pyxel.blt(SCREEN_WIDTH//2 -32, 80, 1, 72, 208, 64,48, 0)
            #lol cover up the visitors_button
            pyxel.rect(SCREEN_WIDTH-45, SCREEN_HEIGHT - 20, 45, 20, pyxel.COLOR_BLACK)
        else: #DRAW VISITOR KEY
            if self.show_visitors is True:
                #miner
                pyxel.blt(32, SCREEN_WIDTH-44, 0, 160, 32, ICON_WIDTH, ICON_HEIGHT)
                pyxel.text(32+ICON_WIDTH+8, SCREEN_WIDTH-36, "Miner", pyxel.COLOR_GRAY)

                #architect
                pyxel.blt(104, SCREEN_WIDTH-44, 0, 0, 32, ICON_WIDTH, ICON_HEIGHT)
                pyxel.text(104+4+ICON_WIDTH, SCREEN_WIDTH-36, "Archeologist", pyxel.COLOR_RED)

                #dam builder
                pyxel.blt(176, SCREEN_WIDTH-44, 0, 176, 32, ICON_WIDTH, ICON_HEIGHT)
                pyxel.text(176+8+ICON_WIDTH, SCREEN_WIDTH-36, "Dam Builder", pyxel.COLOR_BROWN)

                #teenager
                pyxel.blt(60, SCREEN_WIDTH-28, 0, 16, 0, ICON_WIDTH, ICON_HEIGHT)
                pyxel.text(56+4+ICON_WIDTH, SCREEN_WIDTH-20, "Teenager", pyxel.COLOR_DARKBLUE)

                #tunnel maker
                pyxel.blt(144, SCREEN_WIDTH-28, 0, 48, 0, ICON_WIDTH, ICON_HEIGHT)
                pyxel.text(144+4+ICON_WIDTH, SCREEN_WIDTH-20, "Billionaire", pyxel.COLOR_GREEN)
