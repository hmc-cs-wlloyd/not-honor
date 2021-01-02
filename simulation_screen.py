"""A class representing the screen displaying an active simulation"""

import pyxel
from const import ICON_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH
from util import center_text
from event import events

MAP_BOTTOM_MARGIN = 8 + ICON_HEIGHT*3
KEY_MARGIN=6

class SimulationScreen:
    """A class representing the simulation-in-progress screen"""
    def __init__(self, initial_map, events_from_simulation, maps_from_simulation, death_margins):
        self.current_map = initial_map
        self.current_event_index = 0
        self.events_from_simulation = events_from_simulation
        self.maps_from_simulation = maps_from_simulation
        self.death_margins = death_margins
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

        center_text(" Simulating...",
                    page_width=SCREEN_WIDTH,
                    y_coord=SCREEN_HEIGHT-MAP_BOTTOM_MARGIN,
                    text_color=pyxel.COLOR_WHITE)

        if self.events_from_simulation[self.current_event_index][1] != "null":
            event_message = str(self.events_from_simulation[self.current_event_index][0]) + ": " \
                                        + events[self.events_from_simulation[self.current_event_index][1]].description
            pyxel.blt(x=0,
                      y=SCREEN_HEIGHT-(MAP_BOTTOM_MARGIN-ICON_HEIGHT//2),
                      img=events[self.events_from_simulation[self.current_event_index][1]].icon_image,
                      u=events[self.events_from_simulation[self.current_event_index][1]].icon_coords[0],
                      v=events[self.events_from_simulation[self.current_event_index][1]].icon_coords[1],
                      w=events[self.events_from_simulation[self.current_event_index][1]].icon_size[0],
                      h=events[self.events_from_simulation[self.current_event_index][1]].icon_size[1])
            center_text(event_message,
                        page_width=SCREEN_WIDTH-events[self.events_from_simulation[self.current_event_index][1]].icon_size[0],
                        x_coord=events[self.events_from_simulation[self.current_event_index][1]].icon_size[0],
                        y_coord = SCREEN_HEIGHT-(MAP_BOTTOM_MARGIN-ICON_HEIGHT//2),
                        text_color=pyxel.COLOR_WHITE)
        else: #DRAW VISITOR KEY
            if self.show_visitors is True:
                #miner
                pyxel.rect(32,SCREEN_WIDTH-44,4,4,pyxel.COLOR_GRAY)
                pyxel.text(32+8, SCREEN_WIDTH-44, "Miner", pyxel.COLOR_WHITE)

                #architect
                pyxel.rect(104,SCREEN_WIDTH-44,4,4,pyxel.COLOR_RED)
                pyxel.text(104+8, SCREEN_WIDTH-44, "Architect", pyxel.COLOR_WHITE)

                #dam builder
                pyxel.rect(176,SCREEN_WIDTH-44,4,4,pyxel.COLOR_GREEN)
                pyxel.text(176+8, SCREEN_WIDTH-44, "Dam Builder", pyxel.COLOR_WHITE)

                #teenager
                pyxel.rect(64,SCREEN_WIDTH-32,4,4,pyxel.COLOR_DARKBLUE)
                pyxel.text(64+8, SCREEN_WIDTH-32, "Teenager", pyxel.COLOR_WHITE)

                #teenager
                pyxel.rect(128,SCREEN_WIDTH-32,4,4,pyxel.COLOR_BROWN)
                pyxel.text(128+8, SCREEN_WIDTH-32, "Transit Tunnel Maker", pyxel.COLOR_WHITE)
