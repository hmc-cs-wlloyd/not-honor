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

class Map:
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
        #CREATE VISITORS AND A ROGUE THAT SPAWNS FROM THE WEST
        for i in range(10): #generate n cells
            visitor = cell()
            visitor.unsafe_distance = 0
            visitor.direction_spawned_from = "W"
            visitor.x = random.randrange(0,1) #x position starts on left side
            visitor.y = random.randrange(0, SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-16) #y position starts on left side
            self.cells.append(visitor)
        rogue_visitor = cell()#add one rogue that can travel 5 squares in
        rogue_visitor.will_travel_n_squares_in = 5
        rogue_visitor.direction_spawned_from = "W"
        rogue_visitor.x = random.randrange(0,1)
        rogue_visitor.y = random.randrange(0, SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-16)
        self.cells.append(rogue_visitor)

        #CREATE SOME THAT SPAWN FROM THE NORTH
        for i in range(10):
            visitor = cell()
            visitor.unsafe_distance = 0
            visitor.direction_spawned_from = "N"
            visitor.x = random.randrange(0, SCREEN_WIDTH-4)
            visitor.y = random.randrange(0,1)
            self.cells.append(visitor)
        rogue_visitor = cell()#add one rogue that can travel 5 squares in
        rogue_visitor.will_travel_n_squares_in = 5
        rogue_visitor.direction_spawned_from = "N"
        rogue_visitor.x = random.randrange(0, SCREEN_WIDTH-4)
        rogue_visitor.y = random.randrange(0,1)
        self.cells.append(rogue_visitor)

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

                    pyxel.blt(self.selected_col*16, self.selected_row*16,
                              marker.markers[self.selected_inventory_item].icon_image,
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
                pyxel.blt(col*16, row*16, marker.markers[self.map[row][col]].icon_image,
                          marker.markers[self.map[row][col]].icon_coords[0],
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
        self.direction_spawned_from = None
        self.x = None
        self.y = None
        self.speed = random.randrange(2,3) #cell speed
        self.move = [None, None] #realtive x and y coordinates to move to
        self.direction = None #movement direction

    def draw(self):
        if self.will_travel_n_squares_in == 0:
            pyxel.rect(self.x,self.y,4,4,pyxel.COLOR_RED) #draw the cell
        else:
            pyxel.rect(self.x,self.y,4,4,pyxel.COLOR_GREEN) #draw the cell

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
                b = b % len(directionsName) #if direction index is outside the list, wrap around to the other side
                self.direction = directionsName[b]
            self.move[0] = random.randrange(directions[self.direction][0][0],directions[self.direction][0][1]) #change relative x to a random number between min x and max x
            self.move[1] = random.randrange(directions[self.direction][1][0],directions[self.direction][1][1]) #change relative y to a random number between min y and max y
        
            x_square_to_move_to = int((self.x+self.move[0])/16)
            y_square_to_move_to = int((self.y+self.move[1])/16)

            #print("%d, %d" % (y_square_to_move_to, x_square_to_move_to))

            our_map = Map() 
            #if deflected visitor is about to move into a non-sand square, turn around
            #if non-deflected visitor is about to move farther than they should, turn around
            if x_square_to_move_to < 16 or y_square_to_move_to < 13:
                if (our_map.map[y_square_to_move_to][x_square_to_move_to]!="dark-sand" and our_map.map[y_square_to_move_to][x_square_to_move_to]!="sand" and our_map.map[y_square_to_move_to][x_square_to_move_to]!="light-sand" and self.will_travel_n_squares_in == 0) or (x_square_to_move_to >= self.will_travel_n_squares_in + 3):
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
                self.direction = self.direction_spawned_from #turn around in the direction spawned from
            self.move[0] = random.randrange(directions[self.direction][0][0],directions[self.direction][0][1]) #change relative x to a random number between min x and max x
            self.move[1] = random.randrange(directions[self.direction][1][0],directions[self.direction][1][1]) #change relative x to a random number between min x and max x
        if self.move[0] != None: #add the relative coordinates to the cells coordinates
            self.x += self.move[0]
            self.y += self.move[1]
