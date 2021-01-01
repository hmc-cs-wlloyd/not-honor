"""This module defines the Shop class, representing the in-game shop"""

from random import shuffle
from dataclasses import dataclass
import pyxel
from util import center_text
from const import ICON_WIDTH, ICON_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, INVENTORY_BOX_BORDER_THICKNESS, NUM_INVENTORY_BOXES, NUM_SOCIETAL_BOXES
from map import MAP_INVENTORY_BOTTOM_MARGIN, INVENTORY_WIDTH, SOCIETAL_MODIFIER_WIDTH
import marker
import button

SHOP_COLUMNS = 3
SHOP_ROWS = 2

SHOP_TOP_OFFSET=20
SHOP_BOTTOM_OFFSET=80

@dataclass
class Shelf:
    """A class representing a shelf in the shop. Shelves contain markers for sale and their current prices"""
    x_coord: int
    y_coord: int
    width: int
    height: int
    marker_on_shelf: str
    sticker_price: int
    is_sold: bool=False
    hover_on_item = False

    def is_mouse_on_shelf(self):
        """Returns true if the mouse is currently on the shelf"""
        return pyxel.mouse_x > self.x_coord and \
                pyxel.mouse_x < self.x_coord + self.width and \
                pyxel.mouse_y > self.y_coord and \
                pyxel.mouse_y < self.y_coord + self.height
    def draw(self):
        """Draws the shelf and its contents to the screen"""
        center_text(text=marker.markers[self.marker_on_shelf].name,
                page_width=self.width,
                y_coord=self.y_coord+3,
                text_color=pyxel.COLOR_WHITE,
                x_coord=self.x_coord)
        center_text(text="Price: $" + str(self.sticker_price),
                page_width=self.width,
                y_coord=self.y_coord+self.height-7,
                text_color=pyxel.COLOR_WHITE,
                x_coord=self.x_coord)
        pyxel.blt(self.x_coord + self.width // 2 - ICON_WIDTH // 2,
                self.y_coord + self.height // 2 - ICON_HEIGHT // 2,
                0,
                marker.markers[self.marker_on_shelf].icon_coords[0],
                marker.markers[self.marker_on_shelf].icon_coords[1],
                ICON_WIDTH,
                ICON_HEIGHT
        )
        if self.hover_on_item is False:
            pyxel.rectb(self.x_coord, self.y_coord, self.width, self.height, pyxel.COLOR_GRAY)
        elif self.hover_on_item is True:
            pyxel.rectb(self.x_coord, self.y_coord, self.width, self.height, pyxel.COLOR_GREEN)
        
        if self.is_mouse_on_shelf():
            '''pyxel.text(0,
                    SCREEN_HEIGHT-SHOP_BOTTOM_OFFSET-16,
                    marker.markers[self.marker_on_shelf].description,
                    pyxel.COLOR_WHITE)'''
            center_text(marker.markers[self.marker_on_shelf].description, SCREEN_WIDTH, SCREEN_HEIGHT-SHOP_BOTTOM_OFFSET-16, pyxel.COLOR_WHITE)

            self.hover_on_item = True
        else: 
            self.hover_on_item = False

        if self.is_sold:
            banner_padding = 2
            pyxel.rect(self.x_coord, (self.y_coord+self.height/2)-(banner_padding/2), self.width, pyxel.FONT_HEIGHT+banner_padding, pyxel.COLOR_WHITE)
            center_text(text="Sold",
                page_width=self.width,
                y_coord=self.y_coord+self.height/2,
                text_color=pyxel.COLOR_RED,
                x_coord=self.x_coord)

class Shop:
    """A class representing an instance of the shop. Consists of a list of shelves with markers for sale on them"""
    def __init__(self, marker_options, player):
        self.shelves = []
        self.finish_button = button.Button(
            x_coord=SCREEN_WIDTH - 35,
            y_coord=SHOP_TOP_OFFSET/10,
            width=30,
            height=9*SHOP_TOP_OFFSET/10,
            text="Finish",
            button_color=None
        )
        """self.inventory_button = button.Button(
            x_coord=5,
            y_coord=SHOP_TOP_OFFSET/10,
            width=45,
            height=9*SHOP_TOP_OFFSET/10,
            text="Inventory",
            button_color=pyxel.COLOR_GRAY
        )"""
        purchasable_marker_options = [marker_option for marker_option in marker_options if marker.markers[marker_option].is_purchasable()]
        available_marker_options = [marker_option for marker_option in purchasable_marker_options if marker_option not in player.global_buffs]
        print(available_marker_options)
        shuffle(available_marker_options)
        marker_index = 0 #use this to move through the available options and put them in the shop
        for i in range(SHOP_ROWS):
            for j in range(SHOP_COLUMNS):
                if 2*i+j < len(available_marker_options):
                    self.shelves.append(Shelf(x_coord=(SCREEN_WIDTH//SHOP_COLUMNS * j) + (4),
                        y_coord=((SHOP_TOP_OFFSET + ((SCREEN_HEIGHT-SHOP_TOP_OFFSET-SHOP_BOTTOM_OFFSET)//(SHOP_ROWS+1))*i)+(16*i)) + 8,
                        width=(SCREEN_WIDTH//SHOP_COLUMNS)-8,
                        height=(SCREEN_HEIGHT-SHOP_TOP_OFFSET-SHOP_BOTTOM_OFFSET)//(SHOP_ROWS+1),
                        marker_on_shelf=available_marker_options[marker_index],
                        sticker_price=marker.markers[available_marker_options[marker_index]].base_cost
                    ))
                    marker_index+=1

        pyxel.playm(1,loop=True)

    def draw(self, player):
        """Draws the shop to the screen"""
        center_text("Remaining Budget: $" + str(player.funding),
                page_width=SCREEN_WIDTH,
                y_coord=10,
                text_color=pyxel.COLOR_WHITE)
        #self.inventory_button.draw()
        self.finish_button.draw()

        inventory_y_coord = SCREEN_HEIGHT-MAP_INVENTORY_BOTTOM_MARGIN
        center_text("Inventory", #draw the inventory
                    page_width=INVENTORY_WIDTH,
                    x_coord=0,
                    y_coord=inventory_y_coord,
                    text_color=pyxel.COLOR_WHITE)
        for i in range(0,NUM_INVENTORY_BOXES): #draw the inventory with a border around each box
            pyxel.rectb(5 + (i*(ICON_WIDTH+(2*INVENTORY_BOX_BORDER_THICKNESS))), inventory_y_coord + ICON_HEIGHT - INVENTORY_BOX_BORDER_THICKNESS, ICON_WIDTH+(INVENTORY_BOX_BORDER_THICKNESS*2), ICON_HEIGHT+(INVENTORY_BOX_BORDER_THICKNESS*2), pyxel.COLOR_LIGHTBLUE)
        player.draw_inventory(5 + INVENTORY_BOX_BORDER_THICKNESS, inventory_y_coord, SCREEN_WIDTH, ICON_HEIGHT)
        
        center_text("Societal Features", #draw the inventory
                    page_width=SOCIETAL_MODIFIER_WIDTH,
                    x_coord=INVENTORY_WIDTH,
                    y_coord=inventory_y_coord,
                    text_color=pyxel.COLOR_WHITE)
        inventory_width = (NUM_INVENTORY_BOXES*ICON_WIDTH) + 64 #draw the societal factors with a border around each box, 64 is margin between this and societal boxes
        for i in range(0,NUM_SOCIETAL_BOXES): #draw the inventory with a border around each box
            pyxel.rectb(inventory_width + (i*(ICON_WIDTH+(2*INVENTORY_BOX_BORDER_THICKNESS))), inventory_y_coord + ICON_HEIGHT - INVENTORY_BOX_BORDER_THICKNESS, ICON_WIDTH+(INVENTORY_BOX_BORDER_THICKNESS*2), ICON_HEIGHT+(INVENTORY_BOX_BORDER_THICKNESS*2), pyxel.COLOR_LIGHTBLUE)
        player.draw_global_buffs(inventory_width + INVENTORY_BOX_BORDER_THICKNESS, inventory_y_coord, SCREEN_WIDTH, ICON_HEIGHT)

        for shelf in self.shelves:
            shelf.draw()


    def make_purchase(self, player):
        """Purchases for the player whatever is currently under their mouse"""
        for shelf in self.shelves:
            if (not shelf.is_sold) and player.funding >= shelf.sticker_price and shelf.is_mouse_on_shelf():
                shelf.is_sold = True
                pyxel.play(0,5,loop=False)
                player.add_funding(-1*shelf.sticker_price)
                if marker.markers[shelf.marker_on_shelf].is_global():
                    player.add_global_buffs([shelf.marker_on_shelf])
                else:
                    player.add_inventory([shelf.marker_on_shelf])
                return shelf.sticker_price
            if (shelf.is_sold or player.funding<shelf.sticker_price) and shelf.is_mouse_on_shelf():
                pyxel.play(0,4,loop=False)
        return 0
