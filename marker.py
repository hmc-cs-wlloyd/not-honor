"""This module defines the marker class, representing markers to deter intrusion at a nuclear waste
isolation site, and defines the various markers available in the game"""

from dataclasses import dataclass

@dataclass
class Marker: #pylint: disable=too-many-instance-attributes,too-few-public-methods
    """A data-only class representing a marker effecting the waste isolation site"""
    name: str
    base_cost: int
    description: str
    visibility: float
    understandability: float
    respectability: float
    likability: float
    usability: float
    tags: list

markers = {
    "granite-monolith": Marker(
        name="Monolith (Granite)",
        description="A 5 meter monolith carved from a single piece of granite.\nHighly durable",
        base_cost=100000,
        visibility=1,
        understandability=.4,
        respectability=1,
        likability=.8,
        usability=0,
        tags=["surface", "structure", "language-dependent", "low-tech"]
    ),
    "atomic-flower": Marker(
        name="Atomic Flowers",
        description="Flowers with information on the dangers of the site\nencoded into their DNA. \
Self-propagating, but only\neffective against high-tech societies",
        base_cost=500000,
        visibility=.1,
        understandability=.1,
        respectability=0,
        likability=1,
        usability=1,
        tags=["surface", "biological", "high-tech"]
    ),
    "holy-shrine": Marker(
        name="Holy Shrine",
        description="A shrine marking the site as holy ground.\nEffective upon cultures that respect yours",
        base_cost=200000,
        visibility=1,
        understandability=.2,
        respectability=.8,
        likability=1,
        usability=0,
        tags=["surface", "structure", "culture-linked", "low-tech"]
    ),
    "atomic-cult": Marker(
        name="Atomic Cult",
        description="A highly organized priesthood dedicated to preserving\nthe message that \
this site is dangerous.\nVulnerable to religious turmoil",
        base_cost=2000000,
        visibility=.7,
        understandability=.8,
        respectability=.9,
        likability=.1,
        usability=.8,
        tags=["active", "biological", "culture-linked", "low-tech", "religious"]
    ),
    "ray-cats": Marker(
        name="Ray Cats",
        description="Cats genetically engineered to glow in the presence\nof radiation, \
accompanied by efforts to pass into\n legend the message 'avoid places where the cats glow'",
        base_cost=1000000,
        visibility=.9,
        understandability=.4,
        respectability=1,
        likability=1,
        usability=None,
        tags=["biological", "low-tech", "folklore-linked"]
    ),
    "buried-messages": Marker(
        name="Buried Messages",
        description="Warning messages inscribed in ceramics,\nburied at various depths across the \
site.\nMore effective upon cultures with industrial\ndigging technology",
        base_cost=100000,
        visibility=.1,
        understandability=.4,
        respectability=.3,
        likability=0,
        usability=1,
        tags=["buried", "low-tech"]
    )
}

def get_marker_keys():
    """Returns the keys of the marker dictionary as a list"""
    return list(markers) # Casting a dictionary to a list returns the keys as a list
