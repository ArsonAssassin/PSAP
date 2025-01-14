from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region
from .Items import PokemonSnapItem

class PokemonSnapLocationCategory(IntEnum):    
    MISC = 0
    EVENT = 1
    SKIP = 2,
    PHOTO = 3


class PokemonSnapLocationData(NamedTuple):
    id: int
    name: str
    default_item: str
    category: PokemonSnapLocationCategory


class PokemonSnapLocation(Location):
    game: str = "Pokemon Snap"
    category: PokemonSnapLocationCategory
    default_item_name: str

    def __init__(
            self,
            player: int,
            name: str,
            category: PokemonSnapLocationCategory,
            default_item_name: str,
            address: Optional[int] = None,
            parent: Optional[Region] = None):
        super().__init__(player, name, address, parent)
        self.default_item_name = default_item_name
        self.category = category
        self.id = id

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 33330000
        table_offset = 1000

        table_order = [
            "Start Game", "Beach", "Tunnel", "Volcano", "River", "Cave", "Valley", "Rainbow Cloud", "Bulbasaur", "Pikachu", "Zubat", "Magikarp"
        ]

        output = {}
        for i, region_name in enumerate(table_order):
            if len(location_tables[region_name]) > table_offset:
                raise Exception("A location table has {} entries, that is more than {} entries (table #{})".format(len(location_tables[region_name]), table_offset, i))
            output.update({location_data.name: location_data.id for location_data in location_tables[region_name]})
        return output

    def place_locked_item(self, item: PokemonSnapItem):
        self.item = item
        self.locked = True
        item.location = self

location_tables = {
    "Start Game": [
    PokemonSnapLocationData(33339999, "Start Area", "Point Modifier", PokemonSnapLocationCategory.MISC),
    ],
    "Beach":[
    PokemonSnapLocationData(33330006, "Butterfree", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330008, "Pidgey", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330018, "Meowth", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330033, "Doduo", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330041, "Chansey", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330042, "Kangaskhan", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330046, "Scyther", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330052, "Lapras", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330054, "Eevee", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330056, "Snorlax", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ],
    "Tunnel": [    
    PokemonSnapLocationData(33330007, "Kakuna", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330016, "Diglett", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330017, "Dugtrio", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330031, "Magnemite", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330032, "Magneton", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330038, "Haunter", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330039, "Electrode", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330048, "Electabuzz", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330058, "Zapdos", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ],
    "Volcano": [
    PokemonSnapLocationData(33330001, "Charmander", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330002, "Charmeleon", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330003, "Charizard", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330012, "Vulpix", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330021, "Growlithe", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330022, "Arcanine", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330028, "Rapidash", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330049, "Magmar", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330059, "Moltres", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ],
    "River": [
    PokemonSnapLocationData(33330005, "Metapod", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330015, "Vileplume", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330019, "Psyduck", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330023, "Poliwag", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330029, "Slowpoke", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330030, "Slowbro", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330036, "Shellder", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330037, "Cloyster", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330040, "Koffing", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330055, "Porygon", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ],
    "Cave": [
    PokemonSnapLocationData(33330013, "Jigglypuff", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330024, "Weepinbell", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330025, "Victreebel", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330034, "Grimer", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330035, "Muk", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330047, "Jynx", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330053, "Ditto", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330057, "Articuno", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ],
    "Valley": [
    PokemonSnapLocationData(33330004, "Squirtle", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330010, "Sandshrew", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330011, "Sandslash", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330020, "Mankey", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330026, "Geodude", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330027, "Graveler", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330043, "Goldeen", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330044, "Staryu", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330045, "Starmie", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330051, "Gyarados", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330060, "Dratini", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData(33330061, "Dragonite", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ],
    "Rainbow Cloud": [
    PokemonSnapLocationData(33330062, "Mew", "Point Modifier", PokemonSnapLocationCategory.PHOTO)
    ],
    "Bulbasaur" : [
    PokemonSnapLocationData(33330000, "Bulbasaur", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ],
    "Pikachu": [
    PokemonSnapLocationData(33330009, "Pikachu", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ],
    "Zubat": [
    PokemonSnapLocationData(33330014, "Zubat", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ],
    "Magikarp": [
    PokemonSnapLocationData(33330050, "Magikarp", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ]
}

location_dictionary: Dict[str, PokemonSnapLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
