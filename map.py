"""Defines the map class representing the terrain around the waste site"""

import pyxel
import button
import marker
from const import SCREEN_WIDTH, SCREEN_HEIGHT, ICON_WIDTH, ICON_HEIGHT
from util import center_text

MAP_BOTTOM_OFFSET=20
MAP_INVENTORY_BOTTOM_MARGIN = 16*3

class Map:
    """A class representing the map of the waste site, including the placement of markers"""
    def __init__(self):
        self.selected_col = None
        self.selected_row = None
        self.selected_inventory_item = None
        self.clicked_inven = None

        self.map = [
        ["temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain"],
        ["temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain"],
        ["temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain"],
        ["temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain"],
        ["temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain"],
        ["temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain"],
        ["temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain"],
        ["temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain"],
        ["temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain"],
        ["temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain"],
        ["temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain"],
        ["temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain", "temp-terrain",
         "temp-terrain", "temp-terrain"]
        ]

        self.results_button = button.Button(
            x_coord=SCREEN_WIDTH - 35,
            y_coord=SCREEN_HEIGHT - MAP_BOTTOM_OFFSET,
            width=30,
            height=9*MAP_BOTTOM_OFFSET/10,
            text="Results",
            button_color=pyxel.COLOR_GRAY
        )

    def update(self, player):
        """Updates the map state"""
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON): #get the selected square
            self.selected_col = int(pyxel.mouse_x/16)
            self.selected_row = int(pyxel.mouse_y/16)

            inventory_y_coord = SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN
            if self.selected_inventory_item is None:
                if pyxel.mouse_y > inventory_y_coord + 16: #player in inventory
                    for i in range(len(player.inventory)): #BAD ASSUMPTION THAT INVENTORY IS ONLY 1 ROW
                        if pyxel.mouse_x >= i*16 and pyxel.mouse_x < (i*16)+16:
                            self.selected_inventory_item = player.inventory[i]
                            player.inventory.remove(self.selected_inventory_item)
                            print("SELECTED " + str(self.selected_inventory_item))
                            self.clicked_inven = True
            else: #holding a defense
                if pyxel.mouse_y < inventory_y_coord: #player in map
                    self.clicked_inven = False

        if self.selected_col is not None and self.selected_row is not None: #on square selection...
            if self.clicked_inven is False: #place defense if possible on map
                if self.selected_inventory_item not in player.inventory and \
                   self.selected_inventory_item is not None:

                    pyxel.blt(self.selected_col*16, self.selected_row*16, 0,
                              marker.markers[self.selected_inventory_item].icon_coords[0],
                              marker.markers[self.selected_inventory_item].icon_coords[1],
                              ICON_WIDTH, ICON_HEIGHT)
                    self.map[self.selected_row][self.selected_col] = self.selected_inventory_item #update self.map

                    self.clicked_inven = None
                    self.selected_inventory_item = None
    def draw(self, player):
        """Draws map to the screen"""
        self.results_button.draw()

        for row in range(12): #draw the terrain
            for col in range(16):
                pyxel.blt(col*16, row*16, 0, marker.markers[self.map[row][col]].icon_coords[0],
                          marker.markers[self.map[row][col]].icon_coords[1], ICON_WIDTH, ICON_HEIGHT)

        inventory_y_coord = SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN
        center_text("Inventory", #draw the inventory
                page_width=SCREEN_WIDTH,
                y_coord=inventory_y_coord,
                text_color=pyxel.COLOR_WHITE)
        player.draw_inventory(0, inventory_y_coord, SCREEN_WIDTH, ICON_HEIGHT) #BAD ASSUMPTION THAT INVENTORY IS ONLY 1 ROW


        if self.selected_inventory_item is not None: #selected defense follows mouse
            selected_item_icon_x = marker.markers[self.selected_inventory_item].icon_coords[0]
            selected_item_icon_y = marker.markers[self.selected_inventory_item].icon_coords[1]
            pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 0, selected_item_icon_x, selected_item_icon_y, ICON_WIDTH,
                      ICON_HEIGHT)
