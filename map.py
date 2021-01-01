"""Defines the map class representing the terrain around the waste site"""

import random
import pyxel
import button
import marker
from const import SCREEN_WIDTH, SCREEN_HEIGHT, ICON_WIDTH, ICON_HEIGHT
from util import center_text

MAP_BOTTOM_OFFSET=20
MAP_INVENTORY_BOTTOM_MARGIN = 8 + ICON_HEIGHT*3
SOCIETAL_MODIFIER_WIDTH=80
INVENTORY_WIDTH=SCREEN_WIDTH-SOCIETAL_MODIFIER_WIDTH

class Map: #pylint: disable=too-many-instance-attributes
    """A class representing the map of the waste site, including the placement of markers"""
    def __init__(self):
        self.selected_col = None
        self.selected_row = None
        self.selected_inventory_item = None
        self.clicked_inven = None

        self.map = [
        ["dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "sand", "light-sand"],
        ["dark-sand", "dark-sand", "dark-sand", "dark-sand", "sand", "sand", "sand", "sand", "sand", "sand", "sand", "sand", "dark-sand", "sand", "sand", "sand"],
        ["dark-sand", "dark-sand", "sand", "sand", "sand", "light-sand", "light-sand", "light-sand", "light-sand", "light-sand", "light-sand", "sand", "sand", "sand", "sand", "dark-sand"],
        ["dark-sand", "sand", "sand", "light-sand", "light-sand", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "light-sand", "light-sand", "sand", "dark-sand", "dark-sand"],

        ["dark-sand", "sand", "light-sand", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "light-sand", "sand", "sand", "dark-sand"],
        ["dark-sand", "sand", "light-sand", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "core-top-left", "core-top-right", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "light-sand", "sand", "dark-sand"],
        ["dark-sand", "sand", "light-sand", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "core-bottom-left", "core-bottom-right", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "light-sand", "sand", "dark-sand"],
        ["dark-sand", "sand", "light-sand", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "light-sand", "sand", "sand", "dark-sand"],
        
        ["dark-sand", "sand", "sand", "light-sand", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "marbled-tile", "light-sand", "light-sand", "light-sand", "light-sand", "sand", "dark-sand", "dark-sand"],
        ["dark-sand", "dark-sand", "sand", "sand", "light-sand", "light-sand", "light-sand", "light-sand", "light-sand", "sand", "sand", "sand", "sand", "sand", "dark-sand", "dark-sand"],
        ["dark-sand", "dark-sand", "sand", "sand", "sand", "sand", "sand", "sand", "sand", "sand", "dark-sand", "dark-sand", "sand", "dark-sand", "dark-sand", "dark-sand"],
        ["dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand", "dark-sand"]
        ]

        self.simulate_button = button.Button(
            x_coord=SCREEN_WIDTH - 45,
            y_coord=SCREEN_HEIGHT - MAP_BOTTOM_OFFSET,
            width=40,
            height=9*MAP_BOTTOM_OFFSET/10,
            text="Simulate",
            button_color=pyxel.COLOR_GRAY
        )

        self.next_button = button.Button(
            x_coord=(SCREEN_WIDTH-30) // 2,
            y_coord=SCREEN_HEIGHT - MAP_BOTTOM_OFFSET,
            width=30,
            height=9*MAP_BOTTOM_OFFSET/10,
            text="Next",
            button_color=pyxel.COLOR_GRAY
        )

        self.back_button = button.Button(
            x_coord=5,
            y_coord=SCREEN_HEIGHT - MAP_BOTTOM_OFFSET,
            width=30,
            height=9*MAP_BOTTOM_OFFSET/10,
            text="Back",
            button_color=pyxel.COLOR_GRAY
        )
        self.cells =[]
        #CREATE VISITORS AND A ROGUE THAT SPAWNS FROM THE WEST
        for _ in range(10): #generate n cells
            visitor = Cell(x=random.randrange(0,1),
                           y=random.randrange(0, SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-16),
                           direction_spawned_from="W")
            self.cells.append(visitor)
        rogue_visitor = Cell(x=random.randrange(0,1),
                             y=random.randrange(0, SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-16),
                             direction_spawned_from="W",
                             will_travel_n_squares_in=5)#add one rogue that can travel 5 squares in
        self.cells.append(rogue_visitor)

        #CREATE SOME THAT SPAWN FROM THE NORTH
        for _ in range(10):
            visitor = Cell(x=random.randrange(0, SCREEN_WIDTH-4), y=random.randrange(0,1), direction_spawned_from="N")
            self.cells.append(visitor)
        rogue_visitor = Cell(x=random.randrange(0, SCREEN_WIDTH-4),
                             y=random.randrange(0,1),
                             direction_spawned_from="N",
                             will_travel_n_squares_in=5)#add one rogue that can travel 5 squares in
        self.cells.append(rogue_visitor)

    def update(self, player, is_simulation=False):
        """Updates the map state"""
        if not is_simulation: #pylint: disable=too-many-nested-blocks
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

                        pyxel.blt(self.selected_col*16, self.selected_row*16,
                                  marker.markers[self.selected_inventory_item].icon_image,
                                  marker.markers[self.selected_inventory_item].icon_coords[0],
                                  marker.markers[self.selected_inventory_item].icon_coords[1],
                                  ICON_WIDTH, ICON_HEIGHT)
                        self.map[self.selected_row][self.selected_col] = self.selected_inventory_item #update self.map

                        self.clicked_inven = None
                        self.selected_inventory_item = None

        else:
            ###VISITOR SIMULATION DATA
            for i in self.cells:
                i.wander()

    def draw(self, player, is_simulation=False):
        """Draws map to the screen"""
        for row in range(12): #draw the terrain
            for col in range(16):
                pyxel.blt(col*16, row*16, marker.markers[self.map[row][col]].icon_image,
                          marker.markers[self.map[row][col]].icon_coords[0],
                          marker.markers[self.map[row][col]].icon_coords[1], ICON_WIDTH, ICON_HEIGHT)

        if not is_simulation:
            self.simulate_button.draw()
            self.back_button.draw()

            inventory_y_coord = SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN
            center_text("Inventory", #draw the inventory
                    page_width=INVENTORY_WIDTH,
                    x_coord=0,
                    y_coord=inventory_y_coord,
                    text_color=pyxel.COLOR_WHITE)
            player.draw_inventory(0, inventory_y_coord, INVENTORY_WIDTH, ICON_HEIGHT) #BAD ASSUMPTION THAT INVENTORY IS ONLY 1 ROW

            center_text("Societal Features", #draw the inventory
                    page_width=SOCIETAL_MODIFIER_WIDTH,
                    x_coord=INVENTORY_WIDTH,
                    y_coord=inventory_y_coord,
                    text_color=pyxel.COLOR_WHITE)
            player.draw_global_buffs(INVENTORY_WIDTH, inventory_y_coord, SOCIETAL_MODIFIER_WIDTH, ICON_HEIGHT)


            if self.selected_inventory_item is not None: #selected defense follows mouse
                selected_item_icon_x = marker.markers[self.selected_inventory_item].icon_coords[0]
                selected_item_icon_y = marker.markers[self.selected_inventory_item].icon_coords[1]
                pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 0, selected_item_icon_x, selected_item_icon_y, ICON_WIDTH,
                          ICON_HEIGHT)

        else:
            self.next_button.draw()
            ###DRAW VISITORS###
            for i in self.cells:
                i.draw()

class Cell:
    """A class representing a square that random-walks around the map to represent visitors approaching the site in the
    simulation"""
    def __init__(self, x, y, direction_spawned_from, will_travel_n_squares_in=0):
        self.directions_name = ("S","SW","W","NW","N","NE","E","SE") #possible directions
        self.x_coord = x
        self.y_coord = y
        self.will_travel_n_squares_in = will_travel_n_squares_in
        self.direction_spawned_from = direction_spawned_from
        self.speed = random.randrange(2,3) #cell speed
        self.direction = random.choice(self.directions_name) #movement direction

    def draw(self):
        """Draw the cell to the screen"""
        if self.will_travel_n_squares_in == 0:
            pyxel.rect(self.x_coord,self.y_coord,4,4,pyxel.COLOR_RED) #draw the cell
        else:
            pyxel.rect(self.x_coord,self.y_coord,4,4,pyxel.COLOR_GREEN) #draw the cell

    def wander(self):
        """Move the cell along its path"""
        move = [0,0]
        directions = {"S":((-1,2),(1,self.speed)),"SW":((-self.speed,-1),(1,self.speed)),"W":((-self.speed,-1),(-1,2)),
                      "NW":((-self.speed,-1),(-self.speed,-1)),"N":((-1,2),(-self.speed,-1)),
                      "NE":((1,self.speed),(-self.speed,-1)),"E":((1,self.speed),(-1,2)),
                      "SE":((1,self.speed),(1,self.speed))} #((min x, max x)(min y, max y))
        if random.randrange(0,5) == 2: #change direction about once every 5 frames
            direction_idx = self.directions_name.index(self.direction) #get the index of direction in directions list
            new_direction_idx = random.randrange(direction_idx-1,direction_idx+2) #set the direction to be the same, or one next to the current direction
            new_direction_idx = new_direction_idx % len(self.directions_name) #if direction index is outside the list, wrap around to the other side
            self.direction = self.directions_name[new_direction_idx]
        move[0] = random.randrange(directions[self.direction][0][0],directions[self.direction][0][1]) #change relative x to a random number between min x and max x
        move[1] = random.randrange(directions[self.direction][1][0],directions[self.direction][1][1]) #change relative y to a random number between min y and max y

        new_x_coord = self.x_coord + move[0]
        new_y_coord = self.y_coord + move[1]
        x_square_to_move_to = int((new_x_coord)/16)
        y_square_to_move_to = int((new_y_coord)/16)

        our_map = Map()

        #if cell is near the border of the screen or about to move into unsafe area,change direction
        if new_x_coord < 0 or new_x_coord >= SCREEN_WIDTH or new_y_coord < 0 or \
           new_y_coord > SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-13:
            if new_x_coord < 1:
                self.direction = "E"
            elif new_x_coord >= SCREEN_WIDTH - 1:
                self.direction = "W"
            elif new_y_coord < 1:
                self.direction = "S"
            elif new_y_coord > SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-13:
                self.direction = "N"
            move[0] = random.randrange(directions[self.direction][0][0],directions[self.direction][0][1]) #change relative x to a random number between min x and max x
            move[1] = random.randrange(directions[self.direction][1][0],directions[self.direction][1][1]) #change relative x to a random number between min x and max x
        elif (our_map.map[y_square_to_move_to][x_square_to_move_to]!="dark-sand" and \
            our_map.map[y_square_to_move_to][x_square_to_move_to]!="sand" and \
            our_map.map[y_square_to_move_to][x_square_to_move_to]!="light-sand" and \
            self.will_travel_n_squares_in == 0): # or (x_square_to_move_to >= self.will_travel_n_squares_in + 3)

            self.direction = self.direction_spawned_from #turn around in the direction spawned from
            move[0] = random.randrange(directions[self.direction][0][0],directions[self.direction][0][1]) #change relative x to a random number between min x and max x
            move[1] = random.randrange(directions[self.direction][1][0],directions[self.direction][1][1]) #change relative x to a random number between min x and max x
        self.x_coord += move[0]
        self.y_coord += move[1]
