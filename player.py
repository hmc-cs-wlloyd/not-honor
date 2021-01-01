"""Defines the player class"""

import pyxel
from const import ICON_WIDTH, ICON_HEIGHT
from shop import INVENTORY_BOX_BORDER_THICKNESS
import marker

class Player:
    """A class representing the player character"""
    def __init__(self):
        self.funding = 100000
        self.inventory = []
        self.global_buffs = []

    def add_funding(self, funding_to_add):
        """Adds to the player's available funding"""
        self.funding += funding_to_add

    def add_inventory(self, new_markers):
        """Adds a list of markers to the player's inventory"""
        self.inventory += new_markers

    def add_global_buffs(self, global_buffs):
        """Takes in a list of global buffs and adds them to the player's global buffs"""
        self.global_buffs += global_buffs

    def draw_inventory(self, x_coord, y_coord, width, height):
        """Draws the icons of each item in the player's inventory to the screen starting at x, y in a region of
        width x length"""
        row_count = 0
        for i in range(len(self.inventory)):
            if i*ICON_WIDTH-row_count*(width//ICON_WIDTH) > width:
                row_count += i
            if (row_count+1)*ICON_HEIGHT > height:
                break
            pyxel.blt(x_coord+(i*ICON_WIDTH)+(i*2*INVENTORY_BOX_BORDER_THICKNESS), y_coord+(row_count+ICON_HEIGHT), 0,
                      marker.markers[self.inventory[i]].icon_coords[0],
                      marker.markers[self.inventory[i]].icon_coords[1], ICON_WIDTH, ICON_HEIGHT)

    def draw_global_buffs(self, x_coord, y_coord, width, height):
        """Draws the icons of each item in the player's inventory to the screen starting at x, y in a region of
        width x length"""
        row_count = 0
        for i in range(len(self.global_buffs)):
            if i*ICON_WIDTH-row_count*(width//ICON_WIDTH) > width:
                row_count += i
            if (row_count+1)*ICON_HEIGHT > height:
                break
            pyxel.blt(x_coord+(i*ICON_WIDTH)+(i*2*INVENTORY_BOX_BORDER_THICKNESS), y_coord+(row_count+ICON_HEIGHT), 0,
                      marker.markers[self.global_buffs[i]].icon_coords[0],
                      marker.markers[self.global_buffs[i]].icon_coords[1], ICON_WIDTH, ICON_HEIGHT)
