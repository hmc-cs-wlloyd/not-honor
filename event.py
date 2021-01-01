"""This module defines the event class, used for displaying event outcomes"""

from dataclasses import dataclass

@dataclass
class Event: #pylint: disable=too-many-instance-attributes,too-few-public-methods
    """A data-only class representing an event"""
    name: str
    description: str
    icon_coords: tuple
    icon_size: tuple #width and height
    icon_image: int
    fatal: bool
    
events = {
    "aliens": Event(
        name="Alien Invasion",
        description="An alien spaceship has crashed directly into the \n \
        storage site! Containment is instantly breached.",
        icon_coords=(1,97),
        icon_size = (61,45),
        icon_image = 0,
        fatal = True
    ),
    "goths": Event(
        name="Rise of the Neo-Goths",
        description="A band of 'new Visigoths' has taken over the \n \
        American Southewest. They're relatively harmless, but they find \n\
        your spooky monuments enjoyable.",
        icon_coords=(1,49), #not done yet
        icon_size = (61,45),
        icon_image = 0,
        fatal = False
    ),
    "vikings": Event(
        name="Viking Raid",
        description="Desert vikings have pillaged the site! \n \
        They devote their attention to your prettiest monuments, tearing \n\
        them all down.",
        icon_coords=(1,145),
        icon_size = (61,45),
        icon_image = 0,
        fatal = False
    ),
    "earthquake": Event(
        name="Earthquake!",
        description="The ground under the site shakes violently. \n\
        All monoliths are reduced to rubble.",
        icon_coords=(1,49), #not done yet
        icon_size = (61,45),
        icon_image = 0,
        fatal = False
    ),
    "cult-dig": Event(
        name="A New Goal",
        description="Your cult of dubious quality has decided that they \n\
        are in fact the chosen ones, and that the buried waste is a holy \n\
        weapon. They dig up the site, puncturing the cansiters.",
        icon_coords=(1,49), #not done yet
        icon_size = (61,45),
        icon_image = 0,
        fatal = True
    ),
    "faultline": Event(
        name="Spontaneous Faultline",
        description="A new faultline emerges underneath the site. \n\
        All monoliths are reduced to rubble, and buried markers are now \n\
        visible to the naked eye.",
        icon_coords=(1,49), #not done yet
        icon_size = (61,45),
        icon_image = 0,
        fatal = False
    ),
    "cat-holics": Event(
        name="The Cat-Holic Church?",
        description="When Ray Cats move in with the dubious cult, everyone \n\
        wants to see them. People seem to have forgotten the cats' intent, \n\
        so they are seen as signs from god.",
        icon_coords=(16,16), #not done yet
        icon_size = (16,16),
        icon_image = 0,
        fatal = False
    ),
    "stonehenge": Event(
        name="Stonehenge 2.0",
        description="You seem to have inadvertently placed your monoliths to\n\
        line up with a solar eclipse. People flock to see the beauty of the site.",
        icon_coords=(1,49), #not done yet
        icon_size = (61,45),
        icon_image = 0,
        fatal = False
    ),
    "flood": Event(
        name="Biblical Flood",
        description="A historic flood washes over the site. Once it recedes,\n\
        the soil has been reinvigorated with nutrients and moisture, making \n\
        farming look promising.",
        icon_coords=(80,0),
        icon_size = (16,16),
        icon_image = 0,
        fatal = False
    ),
    "smog": Event(
        name="Great Smog Cloud",
        description="A great cloud of smog drifts in from Los Angeles and hovers \n\
        over the region for centuries, reducing visibility.",
        icon_coords=(1,49), #not done yet
        icon_size = (61,45),
        icon_image = 0,
        fatal = False
    ),
    "klingon": Event(
        name="tlhIngan Hol qajatlh",
        description="A Star Trek fanatic is elected president, and she makes it\n\
        illegal to speak any language other than Klingon within the US.",
        icon_coords=(1,49), #not done yet
        icon_size = (61,45),
        icon_image = 0,
        fatal = False
    ),
    "turtle": Event(
        name="Turtle Invasion",
        description="An accident with genetic technology has created a race of \n\
        super-turtles. They’re really not that different from us, but they don’t\n\
        speak English well and they don’t understand our drawings.",
        icon_coords=(1,49), #not done yet
        icon_size = (61,45),
        icon_image = 0,
        fatal = False
    ),
    "park": Event(
        name="National Park Designation",
        description="A future society finds your site markers impressive, and they \n\
        designate the area as a protected national park.",
        icon_coords=(1,49), #not done yet
        icon_size = (61,45),
        icon_image = 0,
        fatal = False
    ),
    "miners": Event(
        name="Miners",
        description="Miners breach the site!",
        icon_coords=(1,49), #not done yet
        icon_size = (61,45),
        icon_image = 0,
        fatal = True
    ),
    "archaeologists": Event(
        name="Archaeologists",
        description="Archaeologists breach the site!",
        icon_coords=(0,16),
        icon_size = (16,16),
        icon_image = 0,
        fatal = True
    ),
    "dams": Event(
        name="Dams",
        description="Dam builders breach the site!",
        icon_coords=(1,49), #not done yet
        icon_size = (61,45),
        icon_image = 0,
        fatal = True
    ),
    "teens": Event(
        name="Teenagers",
        description="Teenagers breach the site!",
        icon_coords=(16,0),
        icon_size = (16,16),
        icon_image = 0,
        fatal = True
    ),
    "tunnel": Event(
        name="Tunnels",
        description="Transit tunnel builders breach the site!",
        icon_coords=(48,0),
        icon_size = (16,16)
        icon_image = 0,
        fatal = True
    )    
}

def get_event_keys():
    """Returns the keys of the event dictionary as a list"""
    return list(events) # Casting a dictionary to a list returns the keys as a list
