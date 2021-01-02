"""Defines the map class representing the terrain around the waste site"""

import random
import pyxel
import button
import marker
from const import SCREEN_WIDTH, SCREEN_HEIGHT, ICON_WIDTH, ICON_HEIGHT, INVENTORY_BOX_BORDER_THICKNESS, NUM_INVENTORY_BOXES, NUM_SOCIETAL_BOXES
from util import center_text

MAP_BOTTOM_OFFSET=20
MAP_INVENTORY_BOTTOM_MARGIN = ICON_HEIGHT*4
SOCIETAL_MODIFIER_WIDTH=80
INVENTORY_WIDTH=SCREEN_WIDTH-SOCIETAL_MODIFIER_WIDTH
CENTER_POINT_OF_CORE_X=112
CENTER_POINT_OF_CORE_Y=96

class Map: #pylint: disable=too-many-instance-attributes
    """A class representing the map of the waste site, including the placement of markers"""
    def __init__(self, death_margins):
        global cells
        cells = []
        self.selected_col = None
        self.selected_row = None
        self.selected_inventory_item = None
        self.clicked_inven = None
        self.death_margins = death_margins
        self.coords_for_bonuses = [] #hold a tuple - x coord, y coord, and color for border
        self.show_directions = False

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
            y_coord=SCREEN_HEIGHT - MAP_BOTTOM_OFFSET + 8,
            width=40,
            height=6*MAP_BOTTOM_OFFSET/10,
            text="Simulate",
            button_color=None
        )

        self.directions_button = button.Button(
            x_coord=SCREEN_WIDTH-100,
            y_coord=SCREEN_HEIGHT - MAP_BOTTOM_OFFSET + 8,
            width=50,
            height=6*MAP_BOTTOM_OFFSET/10,
            text="Directions",
            button_color=pyxel.COLOR_PURPLE
        )

        self.next_button = button.Button(
            x_coord=(SCREEN_WIDTH-30) // 2,
            y_coord=SCREEN_HEIGHT - MAP_BOTTOM_OFFSET + 8,
            width=30,
            height=6*MAP_BOTTOM_OFFSET/10,
            text="Next",
            button_color=pyxel.COLOR_DARKBLUE
        )

        self.visitors_button = button.Button(
            x_coord=SCREEN_WIDTH-45,
            y_coord=SCREEN_HEIGHT - MAP_BOTTOM_OFFSET + 8,
            width=45,
            height=6*MAP_BOTTOM_OFFSET/10,
            text="Visitors",
            button_color=pyxel.COLOR_ORANGE
        )

        self.back_button = button.Button(
            x_coord=5,
            y_coord=SCREEN_HEIGHT - MAP_BOTTOM_OFFSET + 8,
            width=30,
            height=6*MAP_BOTTOM_OFFSET/10,
            text="Back",
            button_color=None
        )

        self.generate_visitors()

    def generate_visitors(self):
        #print("death margins: " + str(self.death_margins))
        #calculate radius for various dot types
        if self.death_margins["mining"] == 0:
            mine_radius = 0
        else:
            mine_radius = self.death_margins["mining"]*128 + 50
        if self.death_margins["archaeology"] == 0:
            arch_radius = 0
        else:
            arch_radius = self.death_margins["archaeology"]*128 + 50
        if self.death_margins["dams"] == 0:
            dam_radius = 0
        else:
            dam_radius = self.death_margins["dams"]*128 + 50
        if self.death_margins["teens"] == 0:
            teen_radius = 0
        else:
            teen_radius = self.death_margins["teens"]*128 + 50
        if self.death_margins["tunnels"] == 0:
            tunnel_radius = 0
        else:
            tunnel_radius = self.death_margins["tunnels"]*128 + 50

        #set colors for intruder types
        mine_color = pyxel.COLOR_GRAY
        arch_color = pyxel.COLOR_RED
        dam_color = pyxel.COLOR_GREEN
        teen_color = pyxel.COLOR_DARKBLUE
        tunnel_color = pyxel.COLOR_BROWN

        #lists for iterating over when making visitors
        visitor_type_list = ["arch", "arch", "mine", "mine", "dam", "dam", "teen", "teen", "tunnel", "tunnel"]
        visitor_color_list = [arch_color, arch_color, mine_color, mine_color, dam_color, dam_color,
                              teen_color, teen_color, tunnel_color, tunnel_color]
        visitor_radius_list = [arch_radius, arch_radius, mine_radius, mine_radius, dam_radius, dam_radius,
                               teen_radius, teen_radius, tunnel_radius, tunnel_radius]


        #CREATE VISITORSFROM THE WEST
        for j in range(10): #generate n cells
            visitor = Cell(x=random.randrange(0,1),
                           y=random.randrange(0, SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-8),
                           direction_spawned_from="W",
                           intruder_type= visitor_type_list[j],
                           intruder_color = visitor_color_list[j],
                           allowable_core_distance= visitor_radius_list[j])
            cells.append(visitor)

        #CREATE SOME THAT SPAWN FROM THE NORTH
        for j in range(10):
            visitor = Cell(x=random.randrange(0, SCREEN_WIDTH-4), y=random.randrange(0,1),
                           direction_spawned_from="N",
                           intruder_type= visitor_type_list[j],
                           intruder_color = visitor_color_list[j],
                           allowable_core_distance= visitor_radius_list[j])
            cells.append(visitor)


        #CREATE SOME THAT SPAWN FROM THE EAST
        for j in range(10):
            visitor = Cell(x=random.randrange(SCREEN_WIDTH-5, SCREEN_WIDTH-4),
                           y=random.randrange(0, SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-8),
                           direction_spawned_from="E",
                           intruder_type= visitor_type_list[j],
                           intruder_color = visitor_color_list[j],
                           allowable_core_distance= visitor_radius_list[j])
            cells.append(visitor)


        #CREATE SOME THAT SPAWN FROM THE SOUTH
        for j in range(10):
            visitor = Cell(x=random.randrange(0, SCREEN_WIDTH-4),
                           y=random.randrange(SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-9,SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-8),
                           direction_spawned_from="S",
                           intruder_type= visitor_type_list[j],
                           intruder_color = visitor_color_list[j],
                           allowable_core_distance= visitor_radius_list[j])
            cells.append(visitor)

    def update(self, player, is_simulation=False):
        """Updates the map state"""
        if not is_simulation: #pylint: disable=too-many-nested-blocks
            if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON): #get the selected square
                self.selected_col = int(pyxel.mouse_x/16)
                self.selected_row = int(pyxel.mouse_y/16)

                inventory_y_coord = SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN
                if self.selected_inventory_item is None:
                    if pyxel.mouse_y > inventory_y_coord + 16 and pyxel.mouse_y < inventory_y_coord + 16 + ICON_HEIGHT + 2*INVENTORY_BOX_BORDER_THICKNESS: #player in inventory
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

                            ###ADJACENCY BONUSES!!!!!!!!!!
                            for row in range (-1,2):
                                for col in range(-1,2):
                                    #check for out of bounds
                                    if self.selected_col+col < 16 and self.selected_col+col > -1 and self.selected_row+row < 12 and self.selected_row+row > -1 and ((row==0 and col==0) is False): 
                                        #check that there's a defense adjacent to current item
                                        if self.map[self.selected_row+row][self.selected_col+col] != "null" and self.map[self.selected_row+row][self.selected_col+col] != "site":
                                            #RED border for SPOOKY
                                            if "spooky" in marker.markers[self.selected_inventory_item].tags and "spooky" in marker.markers[self.map[self.selected_row+row][self.selected_col+col]].tags:
                                                self.coords_for_bonuses.append([self.selected_col*ICON_WIDTH, self.selected_row*ICON_HEIGHT, pyxel.COLOR_RED])
                                                self.coords_for_bonuses.append([(self.selected_col+col)*ICON_WIDTH, (self.selected_row+row)*ICON_HEIGHT, pyxel.COLOR_RED])
                                            #GREEN border for placing "pro-educational" things next to "educational" things
                                            if ("pro-educational" in marker.markers[self.selected_inventory_item].tags and "educational" in marker.markers[self.map[self.selected_row+row][self.selected_col+col]].tags) \
                                            or ("educational" in marker.markers[self.selected_inventory_item].tags and "pro-educational" in marker.markers[self.map[self.selected_row+row][self.selected_col+col]].tags):
                                                self.coords_for_bonuses.append([self.selected_col*ICON_WIDTH, self.selected_row*ICON_HEIGHT, pyxel.COLOR_GREEN])
                                                self.coords_for_bonuses.append([(self.selected_col+col)*ICON_WIDTH, (self.selected_row+row)*ICON_HEIGHT, pyxel.COLOR_GREEN])
                                            #ORANGE border for danger signs and disgust faces next to each other
                                            if self.selected_inventory_item=="danger-sign" and self.map[self.selected_row+row][self.selected_col+col]=="disgust-faces" \
                                            or self.selected_inventory_item=="disgust-faces" and self.map[self.selected_row+row][self.selected_col+col]=="danger-sign":
                                                self.coords_for_bonuses.append([self.selected_col*ICON_WIDTH, self.selected_row*ICON_HEIGHT, pyxel.COLOR_ORANGE])
                                                self.coords_for_bonuses.append([(self.selected_col+col)*ICON_WIDTH, (self.selected_row+row)*ICON_HEIGHT, pyxel.COLOR_ORANGE])
                                            #PURPLE border for the same terraforming objects
                                            if "terraforming" in marker.markers[self.selected_inventory_item].tags and "terraforming" in marker.markers[self.map[self.selected_row+row][self.selected_col+col]].tags \
                                            and self.map[self.selected_row+row][self.selected_col+col] == self.selected_inventory_item:
                                                self.coords_for_bonuses.append([self.selected_col*ICON_WIDTH, self.selected_row*ICON_HEIGHT, pyxel.COLOR_PURPLE])
                                                self.coords_for_bonuses.append([(self.selected_col+col)*ICON_WIDTH, (self.selected_row+row)*ICON_HEIGHT, pyxel.COLOR_PURPLE])
                                            #LIGHTBLUE border for monoliths
                                            if "monolith" in marker.markers[self.selected_inventory_item].tags and "monolith" in marker.markers[self.map[self.selected_row+row][self.selected_col+col]].tags:
                                                self.coords_for_bonuses.append([self.selected_col*ICON_WIDTH, self.selected_row*ICON_HEIGHT, pyxel.COLOR_LIGHTBLUE])
                                                self.coords_for_bonuses.append([(self.selected_col+col)*ICON_WIDTH, (self.selected_row+row)*ICON_HEIGHT, pyxel.COLOR_LIGHTBLUE])
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
                              marker.markers[self.map[row][col]].icon_coords[1], ICON_WIDTH, ICON_HEIGHT, 0)

        if not is_simulation:
            self.simulate_button.draw()
            self.back_button.draw()
            self.directions_button.draw()

            #draw the inventory
            inventory_y_coord = SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN + 8
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
                pyxel.blt(pyxel.mouse_x-8, pyxel.mouse_y-8, 0, selected_item_icon_x, selected_item_icon_y, ICON_WIDTH, ICON_HEIGHT,0)
            
            #show directions
            if self.show_directions is True:
                #background
                border_margin = 2
                pyxel.rect(16-border_margin, 16-border_margin, (SCREEN_WIDTH-16*2)+(border_margin*2), (SCREEN_HEIGHT-16*3.5-4)+(border_margin*2), pyxel.COLOR_NAVY)
                pyxel.rect(16, 16, SCREEN_WIDTH-16*2, SCREEN_HEIGHT-16*3.5-4, pyxel.COLOR_PEACH)
      
                text_margin = 8
                pyxel.text(16+text_margin, 16+text_margin, "DIRECTIONS", pyxel.COLOR_PURPLE)
                pyxel.text(16+text_margin, (16*2), "Place defenses from your inventory onto the map to \nprevent visitors from messing with the nuclear site!", pyxel.COLOR_NAVY)
                pyxel.text(16+text_margin, (16*3)+4, "BONUSES", pyxel.COLOR_PURPLE)
                pyxel.text(16+text_margin, (16*4)-4, "Place certain defenses next to each other!", pyxel.COLOR_CYAN)               
                pyxel.text(16+text_margin, (16*4)+text_margin, "SPOOKY defenses enhance\neach other\'s respectability\nbonus and likability\npenalty", pyxel.COLOR_NAVY)
                i=0 #show all spooky defenses
                for elem in marker.markers: #for simplicity don't show the ruined things 
                    if "spooky" in marker.markers[elem].tags and not "ruined" in marker.markers[elem].tags:
                        pyxel.blt(16+text_margin+(i*19), (16*6)+2, 0, marker.markers[elem].icon_coords[0], marker.markers[elem].icon_coords[1], ICON_WIDTH, ICON_HEIGHT)
                        i+=1
                
                pyxel.text(16+text_margin+112, (16*4)+text_margin, "VISITOR\'S CENTERS enhance\nthe effectiveness of\nEDUCATIONAL defenses", pyxel.COLOR_NAVY)
                pyxel.blt(16+text_margin+112, (16*5)+text_margin+4, 0, marker.markers["visitor-center"].icon_coords[0], marker.markers["visitor-center"].icon_coords[1], ICON_WIDTH, ICON_HEIGHT)
                pyxel.text(16+text_margin+18+112, (16*5)+(text_margin*2-2)+4, "+", pyxel.COLOR_NAVY)
                i=0 #show all educational defenses
                for elem in marker.markers:
                    if "educational" in marker.markers[elem].tags:
                        pyxel.blt((16+text_margin)+16+text_margin+(i*19)+112, (16*5)+text_margin+4, 0, marker.markers[elem].icon_coords[0], marker.markers[elem].icon_coords[1], ICON_WIDTH, ICON_HEIGHT)
                        i+=1

                pyxel.text(16+text_margin, (16*7)+text_margin, "DANGER SIGNS and DISGUSTED\nFACES enhance each\nother\'s effectiveness", pyxel.COLOR_NAVY)
                pyxel.blt(16+text_margin, (16*8)+text_margin+4, 0, marker.markers["danger-sign"].icon_coords[0], marker.markers["danger-sign"].icon_coords[1], ICON_WIDTH, ICON_HEIGHT)
                pyxel.blt(16+text_margin+19, (16*8)+text_margin+4, 0, marker.markers["disgust-faces"].icon_coords[0], marker.markers["disgust-faces"].icon_coords[1], ICON_WIDTH, ICON_HEIGHT)

                pyxel.text(16+text_margin+112, (16*7)+text_margin, "TERRAFORMING defenses of\nthe same name have\nrespectability bonuses\nand land use penalties", pyxel.COLOR_NAVY)
                i=0 #show all terraforming defenses
                for elem in marker.markers:
                    if "terraforming" in marker.markers[elem].tags:
                        pyxel.blt(16+text_margin+(i*19)+112, (16*8)+(text_margin*2)+2, 0, marker.markers[elem].icon_coords[0], marker.markers[elem].icon_coords[1], ICON_WIDTH, ICON_HEIGHT)
                        i+=1

                pyxel.text(16+text_margin, (16*10)+text_margin, "MONOLITHS boost each other\'s\nrespectability bonuses\nand usability penalties", pyxel.COLOR_NAVY)
                i=0 #show all monolith defenses 
                for elem in marker.markers: #for simplicity don't show the ruined ones
                    if "monolith" in marker.markers[elem].tags and not "ruined" in marker.markers[elem].tags:
                        pyxel.blt(16+text_margin+(i*19), (16*11)+text_margin+4, 0, marker.markers[elem].icon_coords[0], marker.markers[elem].icon_coords[1], ICON_WIDTH, ICON_HEIGHT)
                        i+=1


        else: #showing the simulation
            self.next_button.draw() 
            self.visitors_button.draw()
            ###DRAW VISITORS###
            for i in cells:
                i.draw()

        #DRAW BORDERS TO SHOW ADJACENCY BONUSES
        for elem in self.coords_for_bonuses: 
            pyxel.rectb(elem[0], elem[1], ICON_WIDTH, ICON_HEIGHT, elem[2])

class Cell:
    """A class representing a square that random-walks around the map to represent visitors approaching the site in the
    simulation"""
    def __init__(self, x, y, direction_spawned_from, allowable_core_distance, intruder_type, intruder_color):
        self.directions_name = ("S","SW","W","NW","N","NE","E","SE") #possible directions
        self.x_coord = x
        self.y_coord = y
        self.direction_spawned_from = direction_spawned_from
        self.speed = random.randrange(2,3) #cell speed
        self.direction = random.choice(self.directions_name) #movement direction
        self.allowable_core_distance = allowable_core_distance
        self.intruder_type = intruder_type
        self.intruder_color = intruder_color

    def draw(self):
        """Draw the cell to the screen"""
        pyxel.rect(self.x_coord,self.y_coord,4,4,self.intruder_color) #draw the cell


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
           new_y_coord > SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-5:
      
            new_visitor_allowable_distance = self.allowable_core_distance #respawn a visitor with the same stats
            new_intruder_type = self.intruder_type
            new_intruder_color = self.intruder_color
            
            cells.remove(self)
            rand_direction = random.choice(("N","E","S","W"))
            x = 0
            y = 0
            if rand_direction == "N":
                x=random.randrange(0, SCREEN_WIDTH-4)
                y=random.randrange(0,1)
            elif rand_direction == "E":
                x=random.randrange(SCREEN_WIDTH-5, SCREEN_WIDTH-4)
                y=random.randrange(0, SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-8)
            elif rand_direction == "S":
                x=random.randrange(0, SCREEN_WIDTH-4)
                y=random.randrange(SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-9,SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-8)
            elif rand_direction == "W":
                x=random.randrange(0,1)
                y=random.randrange(0, SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN-8)

            visitor = Cell(x, y, direction_spawned_from=rand_direction, allowable_core_distance=new_visitor_allowable_distance,
                           intruder_color=new_intruder_color, intruder_type=new_intruder_type)
            cells.append(visitor)

        #turn around if about to move into unpermitted area
        elif abs(new_x_coord-CENTER_POINT_OF_CORE_X) + abs(new_y_coord-CENTER_POINT_OF_CORE_Y) < self.allowable_core_distance:
            move = [0,0]
        self.x_coord += move[0]
        self.y_coord += move[1]
