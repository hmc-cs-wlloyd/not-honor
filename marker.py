"""This module defines the marker class, representing markers to deter intrusion at a nuclear waste
isolation site, and defines the various markers available in the game"""

from dataclasses import dataclass

@dataclass
class Marker: #pylint: disable=too-many-instance-attributes,too-few-public-methods
    """A data-only class representing a marker effecting the waste isolation site"""
    name: str
    base_cost: int
    description: str
    icon_coords: tuple
    visibility_init: tuple
    visibility_decay: str
    understandability_init: tuple
    understandability_decay: str
    respectability_init: tuple
    respectability_decay: str
    likability_init: tuple
    likability_decay: str
    usability_init: tuple
    usability_decay: str
    tags: list

markers = {
    "granite-monolith": Marker(
        name="Monolith (Granite)",
        description="A 5 meter monolith carved from a single piece of granite.\nHighly durable",
        icon_coords=(240,0),
        base_cost=100000,
        usability_init = (0,0,0),
        usability_decay = "constant",
        visibility_init = (6,6,6),
        visibility_decay = "slow_lin_0",
        respectability_init = (6,6,6),
        respectability_decay = "slow_lin_inc_8",
        likability_init = (0,0,0),
        likability_decay = "constant",
        understandability_init = (9,9,9),
        understandability_decay = "exp_0" ,
        tags=["surface", "structure", "language-dependent", "low-tech"]
    ),
    "atomic-flower": Marker(
        name="Atomic Flowers",
        description="Flowers with information on the dangers of the site\nencoded into their DNA. \
Self-propagating, but only\neffective against high-tech societies",
        icon_coords=(128,0),
        base_cost=500000,
        usability_init = (0,0,0),
        usability_decay = "constant",
        visibility_init = (1,1,1),
        visibility_decay = "constant",
        respectability_init = (0,0,0),
        respectability_decay = "constant",
        likability_init = (3,3,3),
        likability_decay = "constant",
        understandability_init = (0,2,8),
        understandability_decay = "constant",
        tags=["surface", "biological", "high-tech"]
    ),
    "good-cult": Marker(
        name="High Quality Cult",
        description="A highly organized priesthood dedicated to preserving\nthe message that \
this site is dangerous.\nVulnerable to religious turmoil",
        icon_coords=(176,16),
        base_cost=2000000,
        usability_init = (0,0,0),
        usability_decay = "constant",
        visibility_init = (7,7,7),
        visibility_decay = "constant",
        respectability_init = (7,7,7),
        respectability_decay = "constant",
        likability_init = (5,5,5),
        likability_decay = "constant",
        understandability_init = (10,10,10),
        understandability_decay = "lin_0",
        tags=["active", "biological", "culture-linked", "low-tech", "religious"]
    ),
    "ray-cats": Marker(
        name="Ray Cats",
        description="Cats genetically engineered to glow in the presence\nof radiation, \
accompanied by efforts to pass into\nlegend the message 'avoid places where the cats glow'",
        icon_coords=(112, 0),
        base_cost=1000000,
        usability_init = (0,0,0),
        usability_decay = "constant",
        visibility_init = (5,5,5),
        visibility_decay = "constant",
        respectability_init = (3,3,3),
        respectability_decay = "constant",
        likability_init = (-2,-2,-2),
        likability_decay = "constant",
        understandability_init = (5,5,5),
        understandability_decay = "constant",
        tags=["biological", "low-tech", "folklore-linked"]
    ),
    "buried-messages": Marker(
        name="Buried Messages",
        description="Warning messages inscribed in ceramics,\nburied at various depths across the \
site.\nMore effective upon cultures with industrial\ndigging technology",
        icon_coords=(64,16),
        base_cost=100000,
        usability_init = (0,0,0),
        usability_decay = "constant",
        visibility_init = (0,0,0),
        visibility_decay = "constant",
        respectability_init = (3,3,3),
        respectability_decay = "tech_curve",
        likability_init = (-2,-2,-2),
        likability_decay = "lin_0",
        understandability_init = (9,9,9),
        understandability_decay = "exp_0",
        tags=["buried", "low-tech"]
    ),
    "danger-sign": Marker(
        name="Danger Sign",
        description="A sign reading \"danger\" and bearing a radiation\nsymbol",
        icon_coords=(160,16),
        base_cost=1000,
        usability_init = (0,0,0),
        usability_decay = "constant",
        visibility_init = (1,1,1),
        visibility_decay = "lin_0",
        respectability_init = (7,7,7),
        respectability_decay = "lin_0",
        likability_init = (-2,-2,-2),
        likability_decay = "lin_0",
        understandability_init = (5,5,5),
        understandability_decay = "lin_0",
        tags=[]
    ),
    "disgust-faces": Marker(
        name="Disgusted Faces",
        description="Depictions of faces in sickness in pain, etched into\nstone",
        icon_coords=(144,16),
        base_cost=10000,
        usability_init = (0,0,0),
        usability_decay = "constant",
        visibility_init = (2,2,2),
        visibility_decay = "slow_lin_0",
        respectability_init = (0,0,0),
        respectability_decay = "constant",
        likability_init = (-3,-3,-3),
        likability_decay = "constant",
        understandability_init = (3,3,3),
        understandability_decay = "slow_lin_0",
        tags=[]
    ),
    "periodic-table": Marker(
        name="Periodic Table",
        description="A depiction of the periodic table, with the elements\nburied here circled \
and arrows pointing down",
        icon_coords=(192,0),
        base_cost=10000,
        usability_init = (0,0,0),
        usability_decay = "constant",
        visibility_init = (1,1,1),
        visibility_decay = "lin_0",
        respectability_init = (0,0,0),
        respectability_decay = "constant",
        likability_init = (0,0,0),
        likability_decay = "constant",
        understandability_init = (0,5,5),
        understandability_decay = "constant",
        tags=[]
    ),
    "walk-on-map": Marker(
        name="Walk On Map",
        description="A map of all known waste sites inscribed in the ground",
        icon_coords=(80,16),
        base_cost=10000,
        usability_init = (0,0,0),
        usability_decay = "constant",
        visibility_init = (8,8,8),
        visibility_decay = "lin_0",
        respectability_init = (1,1,1),
        respectability_decay = "constant",
        likability_init = (2,2,2),
        likability_decay = "constant",
        understandability_init = (0,7,7),
        understandability_decay = "constant",
        tags=[]
    ),
    "star-map": Marker(
        name="Star Map",
        description="A map of the stars showing their position when the\nsite was created and when \
the site will be safe.\nCould be used to calculate age",
        icon_coords=(128,16),
        base_cost=1000,
        usability_init = (0,0,0),
        usability_decay = "constant",
        visibility_init = (2,2,2),
        visibility_decay = "constant",
        respectability_init = (0,5,5),
        respectability_decay = "constant",
        likability_init = (1,1,1),
        likability_decay = "constant",
        understandability_init = (0,0,0),
        understandability_decay = "constant",
        tags=[]
    ),
    "rubble-field": Marker(
        name="Rubble Field",
        description="Fill the site with random rubble, making access\ndifficult",
        icon_coords=(192,16),
        base_cost=10000,
        usability_init = (-10,-6,-6),
        usability_decay = "constant",
        visibility_init = (9,9,9),
        visibility_decay = "slow_lin_0",
        respectability_init = (0,0,0),
        respectability_decay = "slow_lin_inc_3",
        likability_init = (-3,-3,-3),
        likability_decay = "lin_0",
        understandability_init = (0,0,0),
        understandability_decay = "constant",
        tags=[]
    ),
    "spike-field": Marker(
        name="Spike Field",
        description="Fill the site with dangerous and scary spikes",
        icon_coords=(144,0),
        base_cost=10000,
        usability_init = (-10,-5,-5),
        usability_decay = "constant",
        visibility_init = (10,10,10),
        visibility_decay = "lin_0",
        respectability_init = (9,9,9),
        respectability_decay = "constant",
        likability_init = (-7,-7,-7),
        likability_decay = "constant",
        understandability_init = (0,0,0),
        understandability_decay = "constant",
        tags=[]
    ),
    "attractive-monument": Marker(
        name="Attractive Monument",
        description="A pretty building for your site. Maybe people will\nwant to maintain it?",
        icon_coords=(112,16),
        base_cost=100000,
        usability_init = (4,4,4),
        usability_decay = "constant",
        visibility_init = (8,8,8),
        visibility_decay = "lin_0",
        respectability_init = (7,7,7),
        respectability_decay = "constant",
        likability_init = (9,9,9),
        likability_decay = "constant",
        understandability_init = (0,0,0),
        understandability_decay = "constant",
        tags=[]
    ),
    "bad-cult": Marker(
        name="Cult",
        description="A cult of dubious quality",
        icon_coords=(176,0),
        base_cost=1000,
        usability_init = (0,0,0),
        usability_decay = "constant",
        visibility_init = (7,7,7),
        visibility_decay = "constant",
        respectability_init = (-3,-3,-3),
        respectability_decay = "constant",
        likability_init = (-5,-5,-5),
        likability_decay = "constant",
        understandability_init = (9,9,9),
        understandability_decay = "exp_neg_10",
        tags=[]
    ),
    "visitor-center": Marker(
        name="Visitor Center",
        description="Build a visitor center for the site",
        icon_coords=(208,16),
        base_cost=30000,
        usability_init = (0,0,0),
        usability_decay = "constant",
        visibility_init = (4,4,4),
        visibility_decay = "lin_0",
        respectability_init = (1,1,1),
        respectability_decay = "constant",
        likability_init = (3,3,3),
        likability_decay = "constant",
        understandability_init = (10,10,10),
        understandability_decay = "exp_0",
        tags=[]
    ),
    "cemetery": Marker(
        name="Cemetery",
        description="Build a cemetery on the site - maybe people will\nleave it alone",
        icon_coords=(160,0),
        base_cost=10000,
        usability_init = (-3,-3,-3),
        usability_decay = "constant",
        visibility_init = (7,7,7),
        visibility_decay = "lin_0",
        respectability_init = (10,10,10),
        respectability_decay = "constant",
        likability_init = (-4,-4,-4),
        likability_decay = "constant",
        understandability_init = (-1,-1,-1),
        understandability_decay = "constant",
        tags=[]
    ),
    "wooden-monolith": Marker(
        name="Wooden Monolith",
        description="A monolith made of wood",
        icon_coords=(224,16),
        base_cost=1000,
        usability_init = (0,0,0),
        usability_decay = "constant",
        visibility_init = (6,6,6),
        visibility_decay = "fast_lin_0",
        respectability_init = (4,4,4),
        respectability_decay = "constant",
        likability_init = (0,0,0),
        likability_decay = "constant",
        understandability_init = (9,9,9),
        understandability_decay = "exp_0",
        tags=[]
    ),
    "metal-monolith": Marker(
        name="Metal Monolith",
        description="A monolith made of metal",
        icon_coords=(240,16),
        base_cost=10000,
        usability_init = (2,2,2),
        usability_decay = "constant",
        visibility_init = (6,6,6),
        visibility_decay = "lin_0",
        respectability_init = (5,5,5),
        respectability_decay = "constant",
        likability_init = (0,0,0),
        likability_decay = "constant",
        understandability_init = (9,9,9),
        understandability_decay = "exp_0",
        tags=[]
    ),
    "death-sculpture": Marker(
        name="Death Sculpture",
        description="scary!",
        icon_coords=(224,0),
        base_cost=10000,
        usability_init = (0,0,0),
        usability_decay = "constant",
        visibility_init = (8,8,8),
        visibility_decay = "lin_0",
        respectability_init = (7,7,7),
        respectability_decay = "constant",
        likability_init = (-2,-2,-2),
        likability_decay = "constant",
        understandability_init = (1,1,1),
        understandability_decay = "constant",
        tags=[]
    ),
    "black-hole": Marker(
        name="Black Hole",
        description="A giant void in the ground. Don't fall in!",
        icon_coords=(208,0),
        base_cost=10000,
        usability_init = (-10,-7,-7),
        usability_decay = "constant",
        visibility_init = (10,10,10),
        visibility_decay = "slow_lin_0",
        respectability_init = (6,6,6),
        respectability_decay = "constant",
        likability_init = (-6,-6,-6),
        likability_decay = "constant",
        understandability_init = (0,0,0),
        understandability_decay = "constant",
        tags=[]
    )
}

def get_marker_keys():
    """Returns the keys of the marker dictionary as a list"""
    return list(markers) # Casting a dictionary to a list returns the keys as a list
