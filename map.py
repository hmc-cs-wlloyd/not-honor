"""Defines the map class representing the terrain around the waste site"""

import pyxel
import random
import button
import marker
from const import SCREEN_WIDTH, SCREEN_HEIGHT, ICON_WIDTH, ICON_HEIGHT
from util import center_text

MAP_BOTTOM_OFFSET=20
MAP_INVENTORY_BOTTOM_MARGIN = 8 + ICON_HEIGHT*3
SOCIETAL_MODIFIER_WIDTH=80
INVENTORY_WIDTH=SCREEN_WIDTH-SOCIETAL_MODIFIER_WIDTH

class Map:
    """A class representing the map of the waste site, including the placement of markers"""
    def __init__(self):
        self.selected_col = None
        self.selected_row = None
        self.selected_inventory_item = None
        self.clicked_inven = None

        self.map = [
        ["grass", "grass", "grass", "shadow", "sand", "shadow", "sand", "shadow", "sand", "sand", "marbled-smoke", "fire", "fire", "fire", "fire", "fire"],
        ["grass", "grass", "sand", "sand", "sand", "sand", "shadow", "sand", "sand", "sand", "marbled-smoke", "marbled-smoke", "fire", "fire", "fire", "marbled-smoke"],
        ["grass", "grass", "grass", "grass", "sand", "shadow", "sand", "shadow", "sand", "sand", "sand", "marbled-smoke", "fire", "fire", "marbled-smoke", "marbled-smoke"],
        ["grass", "grass", "grass", "sand", "sand", "sand", "sand", "sand", "sand", "sand", "pink-candles", "fire", "fire", "marbled-smoke", "marbled-smoke", "marbled-smoke"],

        ["grass", "grass", "sand", "sand", "sand", "sand", "sand", "shadow", "sand", "pink-candles", "yellow-candles", "shadow", "fire", "marbled-smoke", "marbled-smoke", "sand"],
        ["grass", "grass", "sand", "sand", "sand", "sand", "shadow", "concrete", "sand", "colorful-stone", "yellow-candles", "pink-candles", "yellow-candles", "colorful-stone", "sand", "concrete"],
        ["grass", "grass", "sand", "shadow", "shadow", "sand", "sand", "shadow", "grass", "colorful-stone", "colorful-stone", "colorful-stone", "colorful-stone", "colorful-stone", "grass", "sand"],
        ["grass", "grass", "shadow", "shadow", "sand", "sand", "sand", "sand", "grass", "colorful-stone", "colorful-stone", "shadow", "colorful-stone", "colorful-stone", "grass", "sand"],
        
        ["grass", "grass", "sand", "sand", "sand", "sand", "sand", "shadow", "grass", "grass", "colorful-stone", "shadow", "colorful-stone", "grass", "grass", "sand"],
        ["grass", "grass", "sand", "sand", "shadow", "sand", "sand", "sand", "grass", "grass", "marbled-tile", "marbled-tile", "marbled-tile", "grass", "grass", "sand"],
        ["grass", "grass", "sand", "sand", "sand", "sand", "sand", "concrete", "sand", "sand", "marbled-tile", "marbled-tile", "marbled-tile", "sand", "sand", "concrete"],
        ["grass", "grass", "grass", "sand", "sand", "sand", "shadow", "sand", "sand", "sand", "marbled-tile", "marbled-tile", "marbled-tile", "sand", "sand", "sand"]
        ]

        self.results_button = button.Button(
            x_coord=SCREEN_WIDTH - 35,
            y_coord=SCREEN_HEIGHT - MAP_BOTTOM_OFFSET,
            width=30,
            height=9*MAP_BOTTOM_OFFSET/10,
            text="Results",
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
        for i in range(10): #generate n cells
            visitor = cell()
            visitor.unsafe_distance = 0
            self.cells.append(visitor)
        rogue_visitor = cell()
        rogue_visitor.will_travel_n_squares_in = 10
        self.cells.append(rogue_visitor) #add one rogue that can travel 10 squares in

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

        ###VISITOR SIMULATION DATA

    def draw(self, player):
        """Draws map to the screen"""
        self.results_button.draw()
        self.back_button.draw()

        for row in range(12): #draw the terrain
            for col in range(16):
                pyxel.blt(col*16, row*16, 1, marker.markers[self.map[row][col]].icon_coords[0],
                          marker.markers[self.map[row][col]].icon_coords[1], ICON_WIDTH, ICON_HEIGHT)

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

        ###DRAW VISITORS###
        for i in self.cells:
            i.wander()
            i.draw()


class cell:
    def __init__(self):
        self.will_travel_n_squares_in = 0
        self.x = random.randrange(0, 1 ) #x position starts on left side
        self.y = random.randrange(0, SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-16) #y position starts on left side
        self.speed = random.randrange(2,3) #cell speed
        self.move = [None, None] #realtive x and y coordinates to move to
        self.direction = None #movement direction

    def draw(self):
        if self.will_travel_n_squares_in == 0:
            pyxel.rect(self.x,self.y,4,4,pyxel.COLOR_RED) #draw the cell
        else:
            pyxel.rect(self.x,self.y,4,4,pyxel.COLOR_WHITE) #draw the cell

    def wander(self):
        turn_around = False
        directions = {"S":((-1,2),(1,self.speed)),"SW":((-self.speed,-1),(1,self.speed)),"W":((-self.speed,-1),(-1,2)),"NW":((-self.speed,-1),(-self.speed,-1)),"N":((-1,2),(-self.speed,-1)),"NE":((1,self.speed),(-self.speed,-1)),"E":((1,self.speed),(-1,2)),"SE":((1,self.speed),(1,self.speed))} #((min x, max x)(min y, max y))
        directionsName = ("S","SW","W","NW","N","NE","E","SE") #possible directions
        if random.randrange(0,5) == 2: #move about once every 5 frames
            if self.direction == None: #if no direction is set, set a random one
                self.direction = random.choice(directionsName)
            else:
                a = directionsName.index(self.direction) #get the index of direction in directions list
                b = random.randrange(a-1,a+2) #set the direction to be the same, or one next to the current direction
                if b > len(directionsName)-1: #if direction index is outside the list, move back to the start
                    b = 0
                self.direction = directionsName[b]
            self.move[0] = random.randrange(directions[self.direction][0][0],directions[self.direction][0][1]) #change relative x to a random number between min x and max x
            self.move[1] = random.randrange(directions[self.direction][1][0],directions[self.direction][1][1]) #change relative y to a random number between min y and max y
        
            x_square_to_move_to = int((self.x+self.move[0])/16)
            y_square_to_move_to = int((self.y+self.move[1])/16)

            our_map = Map()
            if (our_map.map[x_square_to_move_to][y_square_to_move_to] != "grass" and self.will_travel_n_squares_in == 0) or (x_square_to_move_to >= self.will_travel_n_squares_in):
                turn_around = True

        #if cell is near the border of the screen or about to move into unsafe area,change direction
        if self.x < 1 or self.x > SCREEN_WIDTH - 1 or self.y < 1 or self.y > SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-13 or turn_around is True: 
            if self.x < 1:
                self.direction = "E"
            elif self.x > SCREEN_WIDTH - 1:
                self.direction = "W"
            elif self.y < 1:
                self.direction = "S"
            elif self.y > SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-13:
                self.direction = "N"
            elif turn_around is True: 
                self.direction = "W" #THIS IS ONLY FOR VISITORS SPAWNING FORM THE LEFT
            self.move[0] = random.randrange(directions[self.direction][0][0],directions[self.direction][0][1]) #change relative x to a random number between min x and max x
            self.move[1] = random.randrange(directions[self.direction][1][0],directions[self.direction][1][1]) #change relative x to a random number between min x and max x
        if self.move[0] != None: #add the relative coordinates to the cells coordinates
            self.x += self.move[0]
            self.y += self.move[1]












