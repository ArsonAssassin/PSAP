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

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 690000
        table_offset = 1000

        table_order = [
            "Photos",
        ]

        output = {}
        for i, region_name in enumerate(table_order):
            if len(location_tables[region_name]) > table_offset:
                raise Exception("A location table has {} entries, that is more than {} entries (table #{})".format(len(location_tables[region_name]), table_offset, i))

            output.update({location_data.name: id for id, location_data in enumerate(location_tables[region_name], base_id + (table_offset * i))})

        return output

    def place_locked_item(self, item: PokemonSnapItem):
        self.item = item
        self.locked = True
        item.location = self

location_tables = {
    "Photos": [
    PokemonSnapLocationData("Bulbasaur", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Charmander", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Charmeleon", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Charizard", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Squirtle", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Metapod", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Butterfree", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Kakuna", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Pidgey", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Pikachu", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Sandshrew", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Sandslash", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Vulpix", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Jigglypuff", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Zubat", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Vileplume", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Diglett", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Dugtrio", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Meowth", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Psyduck", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Mankey", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Growlithe", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Arcanine", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Poliwag", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Weepinbell", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Victreebel", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Geodude", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Graveler", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Rapidash", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Slowpoke", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Slowbro", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Magnemite", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Magneton", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Doduo", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Grimer", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Muk", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Shellder", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Cloyster", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Haunter", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Electrode", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Koffing", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Chansey", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Kangaskhan", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Goldeen", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Staryu", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Starmie", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Scyther", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Jynx", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Electabuzz", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Magmar", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Magikarp", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Gyarados", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Lapras", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Ditto", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Eevee", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Porygon", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Snorlax", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Articuno", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Zapdos", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Moltres", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Dratini", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Dragonite", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    PokemonSnapLocationData("Mew", "Point Modifier", PokemonSnapLocationCategory.PHOTO)
    ],

}

location_dictionary: Dict[str, PokemonSnapLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
