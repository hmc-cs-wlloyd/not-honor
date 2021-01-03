"""moving tip screen info to new file..."""

import pyxel
from const import SCREEN_WIDTH, SCREEN_HEIGHT
from util import center_text

def draw_chosen_tip(chosen_tip):
    sci_1_x = 0
    sci_1_y = 32
    sci_2_x = 32
    sci_2_y = 32
    sci_3_x = 48
    sci_3_y = 32
    sci_4_x = 64
    sci_4_y = 32
    sci_5_x = 64
    sci_5_y = 48

    
        
    if chosen_tip == 0:
        pyxel.blt((SCREEN_WIDTH/2)-20, 50, 1, 208, 200, 40, 56)
        pyxel.blt((SCREEN_WIDTH/2)-4, 58, 0, 112, 0, 16, 16)
        center_text("Have you heard the good news about RAY CATS?", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text('We\'ll genetically engineer all cats on earth', SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("to glow in the presence of radiation!", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2), pyxel.COLOR_WHITE)
        center_text("Then we plant the seeds of warning", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*3), pyxel.COLOR_WHITE)
        center_text("in various folklore that feline ancestry", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*4), pyxel.COLOR_WHITE)
        center_text("would glow amidst unspeakable dangers.", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*5), pyxel.COLOR_WHITE)
        center_text("As long as humankind continues to worship the cats. . . !", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*6), pyxel.COLOR_WHITE)

    elif chosen_tip == 1:
        pyxel.blt((SCREEN_WIDTH/2)-8, 100, 0, sci_2_x, sci_2_y, 16,16)
        pyxel.blt((SCREEN_WIDTH/2)-8, 56, 1, 208, 200, 40, 40)
        pyxel.blt((SCREEN_WIDTH/2)+8, 64, 0, 160, 32, 16, 16)
        center_text("Oh... hi... ", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("Sorry, people don\'t talk to us mathematicians much.", SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("Want to talk about math? I wrote the part of the", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2), pyxel.COLOR_WHITE)
        center_text("simulation that models MINERS.", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*3), pyxel.COLOR_WHITE)
        center_text('They\'re attracted to high value land,', SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*4), pyxel.COLOR_WHITE)
        center_text("and they\'re scared off by respectable-looking stuff.", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*5), pyxel.COLOR_WHITE)

    elif chosen_tip == 2:
        pyxel.blt((SCREEN_WIDTH/2)-24, 50, 0, 208, 152, 48, 32)
        pyxel.blt((SCREEN_WIDTH/2)-8, 100, 0, sci_1_x, sci_1_y, 16,16)
        center_text("Hey! Check out my SPIKE FIELD!", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text('Isn\'t it intimidating?', SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("I sure wouldn\'t want to hang out here!", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2), pyxel.COLOR_WHITE)

    elif chosen_tip == 3:
        pyxel.blt((SCREEN_WIDTH/2)-24, 40, 0, 144, 184, 56, 56)
        pyxel.blt((SCREEN_WIDTH/2)-8, 48, 0, 240, 0, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)+8, 48, 0, 240, 16, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2), 64, 0, 224, 16, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)-8, 100, 0, sci_3_x, sci_3_y, 16,16)
        center_text("You know, you can\'t go wrong with a MONOLITH.", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text('We\'re making them out of all sorts of stuff now too!', SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("Who knows how long they might last!", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2), pyxel.COLOR_WHITE)

    elif chosen_tip == 4:
        pyxel.blt((SCREEN_WIDTH/2)-16, 56, 1, 149, 200, 56, 40)
        pyxel.blt((SCREEN_WIDTH/2)-5, 64, 0, 176, 0, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)+11, 64, 0, 176, 16, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)-8, 100, 0, sci_4_x, sci_4_y, 16,16)
        center_text('Sounds crazy, but I\'m really into CULTS.', SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("I think if we built the right one,", SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("an Atomic Priesthood could rise that would protect", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2), pyxel.COLOR_WHITE)
        center_text("the knowledge of nuclear physics for all eternity!", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*3), pyxel.COLOR_WHITE)
        center_text("Hey, where are you going?", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*4), pyxel.COLOR_WHITE)

    elif chosen_tip == 5:
        pyxel.blt((SCREEN_WIDTH/2)-16, 56, 1, 149, 200, 56, 40)
        pyxel.blt((SCREEN_WIDTH/2)-5, 64, 0, 160, 16, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)+11, 64, 0, 144, 16, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)-8, 100, 0, sci_5_x, sci_5_y, 16,16)
        center_text("I think we should stick to the basics.", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("It\'s easy to understand a DANGER SIGN or a DISGUSTED FACE.", SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("As long as you speak our language... ", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2), pyxel.COLOR_WHITE)
        center_text("or have a human face yourself...", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*3), pyxel.COLOR_WHITE)

    elif chosen_tip == 6:
        pyxel.blt((SCREEN_WIDTH/2)-24, 40, 0, 144, 184, 56, 56)
        pyxel.blt((SCREEN_WIDTH/2)-8, 48, 0, 192, 0, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)+8, 48, 0, 128, 16, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)-8, 64, 0, 80, 16, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)+8, 64, 0, 208, 16, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)-8, 100, 0, sci_2_x, sci_2_y, 16,16)
        center_text("As a professor, I am a fan of educational initiatives.", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("A PERIODIC TABLE, a STAR MAP, a WALK ON MAP...", SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("They would be well complemented by a VISITORS CENTER!", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2), pyxel.COLOR_WHITE)

    elif chosen_tip == 7:
        pyxel.blt((SCREEN_WIDTH/2)-16, 56, 1, 149, 200, 56, 40)
        pyxel.blt((SCREEN_WIDTH/2)-5, 64, 0, 160, 0, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)+11, 64, 0, 224, 0, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)-8, 100, 0, sci_3_x, sci_3_y, 16,16)
        center_text("I think we should try to scare people away from the site.", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("A CEMETERY or DEATH SCULPTURE would be quite frightening,", SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("as well as respectable!", SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2), pyxel.COLOR_WHITE)

    elif chosen_tip == 8:
        pyxel.blt((SCREEN_WIDTH/2)-8, 56, 1, 208, 200, 40, 40)
        pyxel.blt((SCREEN_WIDTH/2)+8, 64, 0, 128, 0, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)-8, 100, 0, sci_4_x, sci_4_y, 16,16)
        center_text("Why am I, a botanist, on this team?", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("To make ATOMIC FLOWERS, of course! We will encode precise", SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text('information about the site\'s dangers into their DNA. As', SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2), pyxel.COLOR_WHITE)
        center_text('long as you can read the genes, it\'s foolproof!', SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*3), pyxel.COLOR_WHITE)

    elif chosen_tip == 9:
        pyxel.blt((SCREEN_WIDTH/2)-16, 56, 1, 149, 200, 56, 40)
        pyxel.blt((SCREEN_WIDTH/2)-5, 64, 0, 208, 0, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)+11, 64, 0, 192, 16, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)-8, 100, 0, sci_1_x, sci_1_y, 16,16)
        center_text("How can we make the land difficult for invaders to use?", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("Maybe we should install a BLACK HOLE or a RUBBLE FIELD.", SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)

    elif chosen_tip == 10:        
        pyxel.blt((SCREEN_WIDTH/2)-8, 56, 1, 208, 200, 40, 40)
        pyxel.blt((SCREEN_WIDTH/2)-8, 100, 0, sci_2_x, sci_2_y, 16,16)
        pyxel.blt((SCREEN_WIDTH/2)+8, 64, 0, 64, 16, 16, 16)
        center_text("Underground is the safest place to put our warnings!", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("We must include BURIED MESSAGES in our final design! ", SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text('Sure, you can\'t see them now, but they\'ll last forever!', SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2), pyxel.COLOR_WHITE)
        
    elif chosen_tip == 11:
        pyxel.blt((SCREEN_WIDTH/2)-8, 56, 1, 208, 200, 40, 40)
        pyxel.blt((SCREEN_WIDTH/2)-8, 100, 0, sci_3_x, sci_3_y, 16,16)
        pyxel.blt((SCREEN_WIDTH/2)+8, 64, 0, 16, 0, 16, 16)
        center_text("Modeling the behavior of TEENS in the simulation was hard.", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("The\'re just so random and destructive, you know?", SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text(' Dang kids!', SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2), pyxel.COLOR_WHITE)
        
    elif chosen_tip == 12:
        pyxel.blt((SCREEN_WIDTH/2)-8, 56, 1, 208, 200, 40, 40)
        pyxel.blt((SCREEN_WIDTH/2)+8, 64, 0, 0, 16, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)-8, 100, 0, sci_4_x, sci_4_y, 16,16)
        center_text("As an ARCHAEOLOGIST, I\'m a bit offended by the simulation.", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("I wouldn\'t be scared off just because", SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text('something seems \"spooky\"', SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2), pyxel.COLOR_WHITE)

    elif chosen_tip == 13:
        pyxel.blt((SCREEN_WIDTH/2)-8, 56, 1, 208, 200, 40, 40)
        pyxel.blt((SCREEN_WIDTH/2)+8, 64, 0, 48, 0, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)-8, 100, 0, sci_5_x, sci_5_y, 16,16)
        center_text("We\'re always updating the simulation to model new threats.", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("Just recently, we added TRANSIT TUNNELS as a potential ", SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text('intrusion, like the one proposed by famous entrepreneur', SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2), pyxel.COLOR_WHITE)
        center_text('Stretch Beaver.', SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*3), pyxel.COLOR_WHITE)
        
    elif chosen_tip == 14:
        pyxel.blt((SCREEN_WIDTH/2)-8, 56, 1, 208, 200, 40, 40)
        pyxel.blt((SCREEN_WIDTH/2)+8, 64, 0, 176, 32, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)-8, 100, 0, sci_2_x, sci_2_y, 16,16)        
        center_text("You might not think DAMS would be a big threat", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("in the desert, but we\'re modeling them all the same.", SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text('As long as the land utility remains low,', SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*2), pyxel.COLOR_WHITE)
        center_text('you should be safe.', SCREEN_WIDTH, SCREEN_HEIGHT//2+(pyxel.FONT_HEIGHT*3), pyxel.COLOR_WHITE)

    elif chosen_tip == 15:
        pyxel.blt((SCREEN_WIDTH/2)-8, 56, 1, 208, 200, 40, 40)
        pyxel.blt((SCREEN_WIDTH/2)+8, 64, 0, 32, 0, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)-8, 100, 0, sci_3_x, sci_3_y, 16,16)
        center_text("Some say we should plan for a potential ALIEN invasion...", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("I don\'t buy it.", SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)

    elif chosen_tip == 16:
        pyxel.blt((SCREEN_WIDTH/2)-16, 56, 1, 149, 200, 56, 40)
        pyxel.blt((SCREEN_WIDTH/2)-5, 64, 0, 144, 48, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)+11, 64, 0, 128,48, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)-8, 100, 0, sci_4_x, sci_4_y, 16,16)
        center_text("As a geologist, I\'m modeling changes in the site itself.", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("Watch out for EARTHQUAKES and FAULTLINES!", SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)

    elif chosen_tip == 17:
        pyxel.blt((SCREEN_WIDTH/2)-8, 56, 1, 208, 200, 40, 40)
        pyxel.blt((SCREEN_WIDTH/2)+8, 64, 0, 48, 16, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)-8, 100, 0, sci_1_x, sci_1_y, 16,16)
        center_text("As a sociologist, I\m helping model cultural shifts.", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("VIKINGS, GOTHS, KLINGONS... who knows what could be ahead!", SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)

    elif chosen_tip == 18:
        pyxel.blt((SCREEN_WIDTH/2)-8, 56, 1, 208, 200, 40, 40)
        pyxel.blt((SCREEN_WIDTH/2)+8, 64, 0, 112,48, 16, 16)
        pyxel.blt((SCREEN_WIDTH/2)-8, 100, 0, sci_2_x, sci_2_y, 16,16)
        center_text("As a meteorologist, I'm forecasting far-future weather. ", SCREEN_WIDTH, SCREEN_HEIGHT//2-pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)
        center_text("SMOG or FLOODS anyone?", SCREEN_WIDTH, SCREEN_HEIGHT//2+pyxel.FONT_HEIGHT, pyxel.COLOR_WHITE)

    


