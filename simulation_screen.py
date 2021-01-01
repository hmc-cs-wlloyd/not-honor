"""A class representing the screen displaying an active simulation"""

import pyxel
from const import ICON_HEIGHT, SCREEN_HEIGHT, SCREEN_WIDTH
from util import center_text

MAP_BOTTOM_MARGIN = 8 + ICON_HEIGHT*3

class SimulationScreen:
    """A class representing the simulation-in-progress screen"""
    def __init__(self, initial_map, events_from_simulation, maps_from_simulation):
        self.current_map = initial_map
        self.current_event_index = 0
        self.events_from_simulation = events_from_simulation
        self.maps_from_simulation = maps_from_simulation
        self.done = False

    def update(self, player):
        """Updates the simulation-in-progress screen"""
        if self.current_map.next_button.is_clicked():
            self.current_event_index += 1 #this will break stuff if the calling update() doesn't check and advance screen when appropriate
        if self.current_event_index >= len(self.events_from_simulation):
            self.done = True
            return
        self.current_map.map = self.maps_from_simulation[self.current_event_index]
        self.current_map.update(player, is_simulation=True)

    def draw(self, player):
        """Draws the simulation-in-progress screen"""
        self.current_map.draw(player, is_simulation=True)

        center_text("Simulating...",
                    page_width=SCREEN_WIDTH,
                    y_coord=SCREEN_HEIGHT-MAP_BOTTOM_MARGIN,
                    text_color=pyxel.COLOR_WHITE)

        event_message = str(self.events_from_simulation[self.current_event_index][0]) + ": " \
                                               + self.events_from_simulation[self.current_event_index][1]
        center_text(event_message,
                    page_width=SCREEN_WIDTH,
                    y_coord = SCREEN_HEIGHT-(MAP_BOTTOM_MARGIN-ICON_HEIGHT),
                    text_color=pyxel.COLOR_WHITE)
