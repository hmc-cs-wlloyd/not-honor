"""Defines the map class representing the terrain around the waste site"""

import random
import pyxel
import button
import marker
from const import SCREEN_WIDTH, SCREEN_HEIGHT, ICON_WIDTH, ICON_HEIGHT, INVENTORY_BOX_BORDER_THICKNESS, NUM_INVENTORY_BOXES, NUM_SOCIETAL_BOXES
from util import center_text

MAP_BOTTOM_OFFSET=20
MAP_INVENTORY_BOTTOM_MARGIN = 8 + ICON_HEIGHT*3
SOCIETAL_MODIFIER_WIDTH=80
INVENTORY_WIDTH=SCREEN_WIDTH-SOCIETAL_MODIFIER_WIDTH
CENTER_POINT_OF_CORE_X=112
CENTER_POINT_OF_CORE_Y=96

class Map: #pylint: disable=too-many-instance-attributes
    """A class representing the map of the waste site, including the placement of markers"""
    def __init__(self):
        global cells
        cells = []
        self.selected_col = None
        self.selected_row = None
        self.selected_inventory_item = None
        self.clicked_inven = None

        self.map = [
        ["null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null"],
        ["null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null"],
        ["null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null"],
        ["null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null"],
        ["null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null"],
        ["null", "null", "null", "null", "null", "null", "null", "site", "site", "null", "null", "null", "null", "null", "null", "null"],
        ["null", "null", "null", "null", "null", "null", "null", "site", "site", "null", "null", "null", "null", "null", "null", "null"],
        ["null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null"],
        ["null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null"],
        ["null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null"],
        ["null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null"],
        ["null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null", "null"]
        ]

        self.simulate_button = button.Button(
            x_coord=SCREEN_WIDTH - 45,
            y_coord=SCREEN_HEIGHT - MAP_BOTTOM_OFFSET,
            width=40,
            height=9*MAP_BOTTOM_OFFSET/10,
            text="Simulate",
            button_color=None
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
            button_color=None
        )
        #CREATE VISITORS AND A ROGUE THAT SPAWNS FROM THE WEST
        for _ in range(10): #generate n cells
            visitor = Cell(x=random.randrange(0,1),
                           y=random.randrange(0, SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-16),
                           direction_spawned_from="W",
                           allowable_core_distance=128)
            cells.append(visitor)
        rogue_visitor = Cell(x=random.randrange(0,1),
                             y=random.randrange(0, SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-16),
                             direction_spawned_from="W",
                             allowable_core_distance = 0)#add one rogue that can travel all the way to center
        cells.append(rogue_visitor)

        #CREATE SOME THAT SPAWN FROM THE NORTH
        for _ in range(10):
            visitor = Cell(x=random.randrange(0, SCREEN_WIDTH-4), y=random.randrange(0,1), direction_spawned_from="N", allowable_core_distance=128)
            cells.append(visitor)
        rogue_visitor = Cell(x=random.randrange(0, SCREEN_WIDTH-4),
                             y=random.randrange(0,1),
                             direction_spawned_from="N",
                             allowable_core_distance=0)#add one rogue that can travel all the way to center
        cells.append(rogue_visitor)

        #CREATE SOME THAT SPAWN FROM THE EAST
        for _ in range(10):
            visitor = Cell(x=random.randrange(SCREEN_WIDTH-5, SCREEN_WIDTH-4),
                           y=random.randrange(0, SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-16),
                           direction_spawned_from="E",
                           allowable_core_distance=128)
            cells.append(visitor)
        rogue_visitor = Cell(x=random.randrange(SCREEN_WIDTH-5, SCREEN_WIDTH-4),
                             y=random.randrange(0, SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-16),
                             direction_spawned_from="E",
                             allowable_core_distance=0)#add one rogue that can travel all the way to center
        cells.append(rogue_visitor)

        #CREATE SOME THAT SPAWN FROM THE SOUTH
        for _ in range(10):
            visitor = Cell(x=random.randrange(0, SCREEN_WIDTH-4),
                           y=random.randrange(SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-17,SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-16),
                           direction_spawned_from="S",
                           allowable_core_distance=128)
            cells.append(visitor)
        rogue_visitor = Cell(x=random.randrange(0, SCREEN_WIDTH-4),
                             y=random.randrange(SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-17,SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-16),
                             direction_spawned_from="S",
                             allowable_core_distance=0)#add one rogue that can travel all the way to center
        cells.append(rogue_visitor)

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
                            if pyxel.mouse_x >= 5 + (i*(ICON_WIDTH + 2*INVENTORY_BOX_BORDER_THICKNESS)) and \
                                            pyxel.mouse_x < 5 + ((i+1)*(ICON_WIDTH + 2*INVENTORY_BOX_BORDER_THICKNESS)):
                                self.selected_inventory_item = player.inventory[i]
                                player.inventory.remove(self.selected_inventory_item)
                                print("SELECTED " + str(self.selected_inventory_item))
                                self.clicked_inven = True
                else: #holding a defense
                    if pyxel.mouse_y < inventory_y_coord: #player in map
                        self.clicked_inven = False

                if self.selected_col is not None and self.selected_row is not None: #on square selection...
                    if self.clicked_inven is False: #place defense if possible on map
                        if self.map[self.selected_row][self.selected_col] == "site" and \
                           self.selected_inventory_item is not None:
                            pyxel.play(0,4,loop=False)
                        elif self.selected_inventory_item not in player.inventory and \
                           self.selected_inventory_item is not None:

                            self.map[self.selected_row][self.selected_col] = self.selected_inventory_item #update self.map

                            self.clicked_inven = None
                            self.selected_inventory_item = None
        else:
            ###VISITOR SIMULATION DATA
            for i in cells:
                i.wander()

    def draw(self, player, is_simulation=False):
        """Draws map to the screen"""
        pyxel.bltm(0, 0, 7, 0, 232, 32, 24)
        for row in range(12): #draw the terrain
            for col in range(16):
                if self.map[row][col] != "null" and self.map[row][col] != "site":
                    pyxel.blt(col*16, row*16, marker.markers[self.map[row][col]].icon_image,
                              marker.markers[self.map[row][col]].icon_coords[0],
                              marker.markers[self.map[row][col]].icon_coords[1], ICON_WIDTH, ICON_HEIGHT)

        if not is_simulation:
            self.simulate_button.draw()
            self.back_button.draw()

            #draw the inventory
            inventory_y_coord = SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN
            center_text("Inventory",
                    page_width=INVENTORY_WIDTH,
                    x_coord=0,
                    y_coord=inventory_y_coord,
                    text_color=pyxel.COLOR_WHITE)
            for i in range(0,NUM_INVENTORY_BOXES): #draw the inventory with a border around each box
                pyxel.rectb(5+(i*(ICON_WIDTH+(2*INVENTORY_BOX_BORDER_THICKNESS))),
                            inventory_y_coord + ICON_HEIGHT - INVENTORY_BOX_BORDER_THICKNESS,
                            ICON_WIDTH+(INVENTORY_BOX_BORDER_THICKNESS*2),
                            ICON_HEIGHT+(INVENTORY_BOX_BORDER_THICKNESS*2),
                            pyxel.COLOR_LIGHTBLUE)
            player.draw_inventory(5+INVENTORY_BOX_BORDER_THICKNESS, inventory_y_coord, SCREEN_WIDTH, ICON_HEIGHT)
            
            #draw the societal features
            center_text("Societal Features", 
                    page_width=SOCIETAL_MODIFIER_WIDTH,
                    x_coord=INVENTORY_WIDTH,
                    y_coord=inventory_y_coord,
                    text_color=pyxel.COLOR_WHITE)
            inventory_width = (NUM_INVENTORY_BOXES*ICON_WIDTH) + 64 #draw the societal factors with a border around each box, 64 is margin between this and societal boxes
            for i in range(0,NUM_SOCIETAL_BOXES): #draw the societal features with a border around each box
                pyxel.rectb(inventory_width + (i*(ICON_WIDTH+(2*INVENTORY_BOX_BORDER_THICKNESS))), inventory_y_coord + ICON_HEIGHT - INVENTORY_BOX_BORDER_THICKNESS, ICON_WIDTH+(INVENTORY_BOX_BORDER_THICKNESS*2), ICON_HEIGHT+(INVENTORY_BOX_BORDER_THICKNESS*2), pyxel.COLOR_LIGHTBLUE)
            player.draw_global_buffs(inventory_width + INVENTORY_BOX_BORDER_THICKNESS, inventory_y_coord, SCREEN_WIDTH, SCREEN_HEIGHT)

            if self.selected_inventory_item is not None: #selected defense follows mouse
                selected_item_icon_x = marker.markers[self.selected_inventory_item].icon_coords[0]
                selected_item_icon_y = marker.markers[self.selected_inventory_item].icon_coords[1]
                pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 0, selected_item_icon_x, selected_item_icon_y, ICON_WIDTH,
                          ICON_HEIGHT)

        else:
            self.next_button.draw()
            ###DRAW VISITORS###
            for i in cells:
                i.draw()

class Cell:
    """A class representing a square that random-walks around the map to represent visitors approaching the site in the
    simulation"""
    def __init__(self, x, y, direction_spawned_from, allowable_core_distance):
        self.directions_name = ("S","SW","W","NW","N","NE","E","SE") #possible directions
        self.x_coord = x
        self.y_coord = y
        self.direction_spawned_from = direction_spawned_from
        self.speed = random.randrange(2,3) #cell speed
        self.direction = random.choice(self.directions_name) #movement direction
        self.allowable_core_distance = allowable_core_distance

    def draw(self):
        """Draw the cell to the screen"""
        if self.allowable_core_distance > 0:
            pyxel.rect(self.x_coord,self.y_coord,4,4,pyxel.COLOR_RED) #draw the cell
        else:
            pyxel.rect(self.x_coord,self.y_coord,4,4,pyxel.COLOR_GREEN) #draw the rogue

    def wander(self):
        """Move the cell along its path"""
        move = [0,0]
        smallOffset = random.random() #prevent visitors from bunching up with random floating-point number between 0 and 1 ("Tiny number")
        directions = {"S":((-1,2),(1,self.speed)),"SW":((-self.speed,-1),(1,self.speed)),"W":((-self.speed,-1),(-1,2)),
                      "NW":((-self.speed,-1),(-self.speed,-1)),"N":((-1,2),(-self.speed,-1)),
                      "NE":((1,self.speed),(-self.speed,-1)),"E":((1,self.speed),(-1,2)),
                      "SE":((1,self.speed),(1,self.speed))} #((min x, max x)(min y, max y))
        if random.randrange(0,5) == 2: #change direction about once every 5 frames
            direction_idx = self.directions_name.index(self.direction) #get the index of direction in directions list
            new_direction_idx = random.randrange(direction_idx-1,direction_idx+2) #set the direction to be the same, or one next to the current direction
            new_direction_idx = new_direction_idx % len(self.directions_name) #if direction index is outside the list, wrap around to the other side
            self.direction = self.directions_name[new_direction_idx]
        move[0] = random.randrange(directions[self.direction][0][0],directions[self.direction][0][1]) + smallOffset #change relative x to a random number between min x and max x
        move[1] = random.randrange(directions[self.direction][1][0],directions[self.direction][1][1]) + smallOffset #change relative y to a random number between min y and max y

        new_x_coord = self.x_coord + move[0]
        new_y_coord = self.y_coord + move[1]
        x_square_to_move_to = int((new_x_coord)/16)
        y_square_to_move_to = int((new_y_coord)/16)

        #remove visitor if it moves off screen and respawn the same visitor somewhere else
        if new_x_coord < 0 or new_x_coord >= SCREEN_WIDTH or new_y_coord < 0 or \
           new_y_coord > SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-13:
      
            new_visitor_allowable_distance = self.allowable_core_distance #respawn a visitor with the same allowable core distance
            cells.remove(self)
            rand_direction = random.choice(("N","E","S","W")) 
            x = 0
            y = 0
            if rand_direction == "N":
                x=random.randrange(0, SCREEN_WIDTH-4)
                y=random.randrange(0,1)
            elif rand_direction == "E":
                x=random.randrange(SCREEN_WIDTH-5, SCREEN_WIDTH-4)
                y=random.randrange(0, SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-16)
            elif rand_direction == "S":
                x=random.randrange(0, SCREEN_WIDTH-4)
                y=random.randrange(SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-17,SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-16)
            elif rand_direction == "W":
                x=random.randrange(0,1)
                y=random.randrange(0, SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-16)

            visitor = Cell(x, y, direction_spawned_from=rand_direction, allowable_core_distance=new_visitor_allowable_distance)
            cells.append(visitor)

        #turn around if about to move into unpermitted area
        elif abs(new_x_coord-CENTER_POINT_OF_CORE_X) + abs(new_y_coord-CENTER_POINT_OF_CORE_Y) < self.allowable_core_distance:
            self.direction = self.direction_spawned_from #turn around in the direction spawned from
            move[0] = random.randrange(directions[self.direction][0][0],directions[self.direction][0][1]) + smallOffset #change relative x to a random number between min x and max x
            move[1] = random.randrange(directions[self.direction][1][0],directions[self.direction][1][1]) + smallOffset #change relative x to a random number between min x and max x
        self.x_coord += move[0]
        self.y_coord += move[1]
