from enum import IntEnum
from typing import NamedTuple
import random
from BaseClasses import Item


class PokemonSnapItemCategory(IntEnum):
    TOOL = 0
    AREA = 1,
    MISC = 2,
    SKIP = 3,
    EVENT = 4


class PokemonSnapItemData(NamedTuple):
    name: str
    ps_code: int
    category: PokemonSnapItemCategory


class PokemonSnapItem(Item):
    game: str = "Pokemon Snap"

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 690000
        return {item_data.name: base_id + item_data.ps_code for item_data in _all_items}


key_item_names = {
}


_all_items = [PokemonSnapItemData(row[0], row[1], row[2]) for row in [    
    ("Apple Unlocked",             1000, PokemonSnapItemCategory.TOOL), #803AE51F
    ("Pester Ball Unlocked",             1001, PokemonSnapItemCategory.TOOL), #803AE51F
    ("Flute Unlocked",             1002, PokemonSnapItemCategory.TOOL),  #803AE51F
    ("Speed Boost Unlocked",             1003, PokemonSnapItemCategory.TOOL),  #803AE51F

    ("Beach Unlocked",             2000, PokemonSnapItemCategory.AREA), 
    ("Tunnel Unlocked",             2001, PokemonSnapItemCategory.AREA),     
    ("Volcano Unlocked",             2002, PokemonSnapItemCategory.AREA), 
    ("River Unlocked",             2003, PokemonSnapItemCategory.AREA), 
    ("Cave Unlocked",             2004, PokemonSnapItemCategory.AREA), 
    ("Valley Unlocked",             2005, PokemonSnapItemCategory.AREA), 
    ("Rainbow Cloud Unlocked",             2006, PokemonSnapItemCategory.AREA), 

    ("Point Modifier",            3000, PokemonSnapItemCategory.MISC), #81232E6A
    ("Film Capacity Upgrade",       3001, PokemonSnapItemCategory.MISC), #800AC0E3
    ("Rapid Fire Upgrade",       3002, PokemonSnapItemCategory.MISC), #80382CB7
]]

item_descriptions = {
}

item_dictionary = {item_data.name: item_data for item_data in _all_items}

def BuildItemPool(count, guaranteed_items):
    item_pool = []
    
    item_pool.append(PokemonSnapItemData("Apple Unlocked", 1000, PokemonSnapItemCategory.TOOL))
    item_pool.append(PokemonSnapItemData("Pester Ball Unlocked", 1001, PokemonSnapItemCategory.TOOL))
    item_pool.append(PokemonSnapItemData("Flute Unlocked", 1002, PokemonSnapItemCategory.TOOL))
    item_pool.append(PokemonSnapItemData("Speed Boost Unlocked", 1003, PokemonSnapItemCategory.TOOL))

    
    item_pool.append(PokemonSnapItemData("Beach Unlocked", 2000, PokemonSnapItemCategory.AREA))
    item_pool.append(PokemonSnapItemData("Tunnel Unlocked", 2001, PokemonSnapItemCategory.AREA))
    item_pool.append(PokemonSnapItemData("Volcano Unlocked", 2002, PokemonSnapItemCategory.AREA))
    item_pool.append(PokemonSnapItemData("River Unlocked", 2003, PokemonSnapItemCategory.AREA))
    item_pool.append(PokemonSnapItemData("Cave Unlocked", 2004, PokemonSnapItemCategory.AREA))
    item_pool.append(PokemonSnapItemData("Valley Unlocked", 2005, PokemonSnapItemCategory.AREA))
    item_pool.append(PokemonSnapItemData("Rainbow Cloud Unlocked", 2006, PokemonSnapItemCategory.AREA))
    for i in range(count - 11):
        item_pool.append(PokemonSnapItemData("Point Modifier", 3000, PokemonSnapItemCategory.MISC))
  
    random.shuffle(item_pool)
    return item_pool
