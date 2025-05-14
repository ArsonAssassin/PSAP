# world/pokemon_snap/__init__.py
from typing import Dict, Set, List
import random
from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification
from Options import Toggle

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule, add_rule, add_item_rule

from .Items import PokemonSnapItem, PokemonSnapItemCategory, item_dictionary, key_item_names, item_descriptions, BuildItemPool, _all_items
from .Locations import PokemonSnapLocation, PokemonSnapLocationCategory, location_tables, location_dictionary
from .Options import PokemonSnapOption

class PokemonSnapWeb(WebWorld):
    bug_report_page = ""
    theme = "stone"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Pokemon Snap randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["ArsonAssassin"]
    )


    tutorials = [setup_en]


class PokemonSnapWorld(World):
    """
    Pokemon Snap is a game about taking photographs of monsters to score points.
    """

    game: str = "Pokemon Snap"
    options_dataclass = PokemonSnapOption
    options: PokemonSnapOption
    topology_present: bool = True
    web = PokemonSnapWeb()
    data_version = 0
    base_id = 33330000
    enabled_location_categories: Set[PokemonSnapLocationCategory]
    required_client_version = (0, 5, 0)
    item_name_to_id = PokemonSnapItem.get_name_to_id()
    location_name_to_id = PokemonSnapLocation.get_name_to_id()
    item_name_groups = {
    }
    item_descriptions = item_descriptions


    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []
        self.enabled_location_categories = set()       
        self.start_area = None

    def generate_early(self):
        self.enabled_location_categories.add(PokemonSnapLocationCategory.MISC)
        self.enabled_location_categories.add(PokemonSnapLocationCategory.EVENT)
        self.enabled_location_categories.add(PokemonSnapLocationCategory.PHOTO)


    def create_regions(self):
        # Create Regions
        regions: Dict[str, Region] = {}
        regions["Menu"] = self.create_region("Menu", [])
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
            "Start Game", "Beach", "Tunnel", "Volcano", "River", "Cave", "Valley", "Rainbow Cloud", "Bulbasaur", "Pikachu", "Zubat", "Magikarp"
        ]})
        

        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{from_region} -> {to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])
        create_connection("Menu", "Start Game") 
      
        create_connection("Start Game", "Beach") 
        create_connection("Start Game", "Tunnel") 
        create_connection("Start Game", "Volcano") 
        create_connection("Start Game", "River") 
        create_connection("Start Game", "Cave") 
        create_connection("Start Game", "Valley") 
        create_connection("Start Game", "Rainbow Cloud") 

        create_connection("River", "Bulbasaur") 
        create_connection("Cave", "Bulbasaur") 
        
        create_connection("Tunnel", "Zubat") 
        create_connection("Cave", "Zubat") 
        
        create_connection("Beach", "Pikachu") 
        create_connection("River", "Pikachu")         
        create_connection("Tunnel", "Pikachu") 
        create_connection("Cave", "Pikachu") 
        
        create_connection("Beach", "Magikarp")        
        create_connection("Tunnel", "Magikarp") 
        create_connection("Volcano", "Magikarp")  
        create_connection("River", "Magikarp")    
        create_connection("Cave", "Magikarp") 
        create_connection("Valley", "Magikarp")    
        
        for entrance in self.multiworld.get_entrances(self.player):
            print("Entrance: " + entrance.name)
        for region in self.multiworld.regions:
            print("Region: " + region.name)
            for exit in region.exits:
                print("Region exit: " + exit.name)
            for entrance in region.entrances:
                print("Region entrance: " + entrance.name)
            for location in region.locations:
                print("Region location: " + location.name)

        
        
    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)
        #print("location table size: " + str(len(location_table)))
        for location in location_table:
            if location.name == "Start Area":
                areas = [item for item in _all_items if item.category == PokemonSnapItemCategory.AREA]
                print("Areas: ")
                for area in areas:
                    print(area.name)
                self.start_area = random.choice(areas)
                print("Start area set to: " + self.start_area.name)
                start_item = self.create_item(self.start_area.name)
                new_location = PokemonSnapLocation(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    None,
                    new_region
                )
                new_location.place_locked_item(start_item)
            #print("Creating location: " + location.name)
            elif location.category in self.enabled_location_categories:
                #print("Adding location: " + location.name + " with default item " + location.default_item)
                new_location = PokemonSnapLocation(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region
                )
            else:
                # Replace non-randomized progression items with events
                event_item = self.create_item(location.default_item)
                #if event_item.classification != ItemClassification.progression:
                #    continue
                #print("Adding Location: " + location.name + " as an event with default item " + location.default_item)
                new_location = PokemonSnapLocation(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    None,
                    new_region
                )
                event_item.code = None
                new_location.place_locked_item(event_item)
                #print("Placing event: " + event_item.name + " in location: " + location.name)

            new_region.locations.append(new_location)
        print("created " + str(len(new_region.locations)) + " locations")
        self.multiworld.regions.append(new_region)
        print("adding region: " + region_name)
        return new_region


    def create_items(self):
        skip_items: List[PokemonSnapItem] = []
        itempool: List[PokemonSnapItem] = []
        itempoolSize = 0
        
        #print("Creating items")
        for location in self.multiworld.get_locations(self.player):
                if location.name == "Start Area":
                    continue
                #print("found item in category: " + str(location.category))
                item_data = item_dictionary[location.default_item_name]
                if item_data.category in [PokemonSnapItemCategory.SKIP, PokemonSnapItemCategory.EVENT]:                
                    #print("Adding skip item: " + location.default_item_name)
                    skip_items.append(self.create_item(location.default_item_name))
                elif location.category in self.enabled_location_categories:
                    #print("Adding item: " + location.default_item_name)
                    itempoolSize += 1
                    itempool.append(self.create_item(location.default_item_name))        

        print("Requesting itempool size: " + str(itempoolSize))
        foo = BuildItemPool(itempoolSize, self.options.guaranteed_items.value, self.start_area)
        print("Created item pool size: " + str(len(foo)))

        removable_items = [item for item in itempool if item.classification != ItemClassification.progression]
        print("marked " + str(len(removable_items)) + " items as removable")

        for item in removable_items:
            print("removable item: " + item.name)
            itempool.remove(item)
            itempool.append(self.create_item(foo.pop().name))

        # Add regular items to itempool
        self.multiworld.itempool += itempool

        # Handle SKIP items separately
        for skip_item in skip_items:
            location = next(loc for loc in self.multiworld.get_locations(self.player) 
                            if loc.default_item_name == skip_item.name)
            location.place_locked_item(skip_item)
            #self.multiworld.itempool.append(skip_item)
            #print("Placing skip item: " + skip_item.name + " in location: " + location.name)
        
        print("Final Item pool: ")
        for item in self.multiworld.itempool:
            print(item.name)


    def create_item(self, name: str) -> Item:
        useful_categories = {
        }
        data = self.item_name_to_id[name]

        if name in key_item_names:
            item_classification = ItemClassification.progression
        elif item_dictionary[name].category in useful_categories:
            item_classification = ItemClassification.useful
        else:
            item_classification = ItemClassification.filler

        return PokemonSnapItem(name, item_classification, data, self.player)


    def get_filler_item_name(self) -> str:
        return ""
    

    
    def set_rules(self) -> None:        
        print("Setting rules")
        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                    set_rule(location, lambda state: True)        
        self.multiworld.completion_condition[self.player] = lambda state:self.multiworld.get_location("Mew", self.player).can_reach(state)
        set_rule(self.multiworld.get_entrance("Start Game -> Beach", self.player), lambda state: state.has("Beach Unlocked", self.player))   
        set_rule(self.multiworld.get_entrance("Start Game -> Tunnel", self.player), lambda state: state.has("Tunnel Unlocked", self.player))   
        set_rule(self.multiworld.get_entrance("Start Game -> Volcano", self.player), lambda state: state.has("Volcano Unlocked", self.player))   
        set_rule(self.multiworld.get_entrance("Start Game -> River", self.player), lambda state: state.has("River Unlocked", self.player))   
        set_rule(self.multiworld.get_entrance("Start Game -> Cave", self.player), lambda state: state.has("Cave Unlocked", self.player))   
        set_rule(self.multiworld.get_entrance("Start Game -> Valley", self.player), lambda state: state.has("Valley Unlocked", self.player))   
        set_rule(self.multiworld.get_entrance("Start Game -> Rainbow Cloud", self.player), lambda state: state.has("Rainbow Cloud Unlocked", self.player))   

        set_rule(self.multiworld.get_entrance("River -> Bulbasaur", self.player), lambda state: True)
        set_rule(self.multiworld.get_entrance("Cave -> Bulbasaur", self.player), lambda state: True)
        
        set_rule(self.multiworld.get_entrance("Tunnel -> Zubat", self.player), lambda state: True)
        set_rule(self.multiworld.get_entrance("Cave -> Zubat", self.player), lambda state: True)
        
        set_rule(self.multiworld.get_entrance("Beach -> Pikachu", self.player), lambda state: True)
        set_rule(self.multiworld.get_entrance("River -> Pikachu", self.player), lambda state: True)   
        set_rule(self.multiworld.get_entrance("Tunnel -> Pikachu", self.player), lambda state: True)
        set_rule(self.multiworld.get_entrance("Cave -> Pikachu", self.player), lambda state: True)
        
        set_rule(self.multiworld.get_entrance("Beach -> Magikarp", self.player), lambda state: True)
        set_rule(self.multiworld.get_entrance("Tunnel -> Magikarp", self.player), lambda state: True)
        set_rule(self.multiworld.get_entrance("Volcano -> Magikarp", self.player), lambda state: True)
        set_rule(self.multiworld.get_entrance("River -> Magikarp", self.player), lambda state: True)
        set_rule(self.multiworld.get_entrance("Cave -> Magikarp", self.player), lambda state: True)
        set_rule(self.multiworld.get_entrance("Valley -> Magikarp", self.player), lambda state: True)
        
        #beach
        set_rule(self.multiworld.get_location(f"Scyther", self.player), lambda state: state.has("Pester Ball Unlocked", self.player))
        set_rule(self.multiworld.get_location(f"Magikarp", self.player), lambda state: state.has("Pester Ball Unlocked", self.player) or state.has("Apple Unlocked", self.player))
        set_rule(self.multiworld.get_location(f"Chansey", self.player), lambda state: state.has("Pester Ball Unlocked", self.player) or state.has("Apple Unlocked", self.player))
        set_rule(self.multiworld.get_location(f"Snorlax", self.player), lambda state: state.has("Pester Ball Unlocked", self.player) or state.has("Flute Unlocked", self.player))
        #tunnel
        set_rule(self.multiworld.get_location(f"Magnemite", self.player), lambda state: state.has("Apple Unlocked", self.player))
        set_rule(self.multiworld.get_location(f"Magneton", self.player), lambda state: state.has("Apple Unlocked", self.player))
        set_rule(self.multiworld.get_location(f"Zapdos", self.player), lambda state: state.has("Apple Unlocked", self.player) and state.has("Flute Unlocked", self.player))
        #volcano
        set_rule(self.multiworld.get_location(f"Charmeleon", self.player), lambda state: state.has("Pester Ball Unlocked", self.player) or state.has("Apple Unlocked", self.player))
        set_rule(self.multiworld.get_location(f"Charizard", self.player), lambda state: state.has("Pester Ball Unlocked", self.player) or state.has("Apple Unlocked", self.player))
        set_rule(self.multiworld.get_location(f"Growlithe", self.player), lambda state: state.has("Pester Ball Unlocked", self.player))
        set_rule(self.multiworld.get_location(f"Arcanine", self.player), lambda state: state.has("Pester Ball Unlocked", self.player))
        set_rule(self.multiworld.get_location(f"Moltres", self.player), lambda state: state.has("Pester Ball Unlocked", self.player) or state.has("Apple Unlocked", self.player))
        #river
        set_rule(self.multiworld.get_location(f"Bulbasaur", self.player), lambda state: state.has("Pester Ball Unlocked", self.player))
        set_rule(self.multiworld.get_location(f"Vileplume", self.player), lambda state: state.has("Flute Unlocked", self.player))
        set_rule(self.multiworld.get_location(f"Slowbro", self.player), lambda state: state.has("Apple Unlocked", self.player))
        #cave
        set_rule(self.multiworld.get_location(f"Victreebel", self.player), lambda state: state.has("Pester Ball Unlocked", self.player) or state.has("Apple Unlocked", self.player))
        set_rule(self.multiworld.get_location(f"Ditto", self.player), lambda state: state.has("Pester Ball Unlocked", self.player))
        set_rule(self.multiworld.get_location(f"Articuno", self.player), lambda state: state.has("Flute Unlocked", self.player))
        #valley
        set_rule(self.multiworld.get_location(f"Graveler", self.player), lambda state: state.has("Pester Ball Unlocked", self.player))
        set_rule(self.multiworld.get_location(f"Goldeen", self.player), lambda state: state.has("Pester Ball Unlocked", self.player) or state.has("Apple Unlocked", self.player))
        set_rule(self.multiworld.get_location(f"Gyarados", self.player), lambda state: state.has("Pester Ball Unlocked", self.player))
        set_rule(self.multiworld.get_location(f"Dratini", self.player), lambda state: state.has("Pester Ball Unlocked", self.player) or state.has("Apple Unlocked", self.player))
        set_rule(self.multiworld.get_location(f"Dragonite", self.player), lambda state: state.has("Pester Ball Unlocked", self.player))
        
    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}


        name_to_ps_code = {item.name: item.ps_code for item in item_dictionary.values()}
        # Create the mandatory lists to generate the player's output file
        items_id = []
        items_address = []
        locations_id = []
        locations_address = []
        locations_target = []
        for location in self.multiworld.get_filled_locations():


            if location.item.player == self.player:
                #we are the receiver of the item
                items_id.append(location.item.code)
                items_address.append(name_to_ps_code[location.item.name])


            if location.player == self.player:
                #we are the sender of the location check
                locations_address.append(item_dictionary[location_dictionary[location.name].default_item].ps_code)
                locations_id.append(location.address)
                if location.item.player == self.player:
                    locations_target.append(name_to_ps_code[location.item.name])
                else:
                    locations_target.append(0)

        slot_data = {
            "options": {
                "guaranteed_items": self.options.guaranteed_items.value,
            },
            "seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "slot": self.multiworld.player_name[self.player],  # to connect to server
            "base_id": self.base_id,  # to merge location and items lists
            "locationsId": locations_id,
            "locationsAddress": locations_address,
            "locationsTarget": locations_target,
            "itemsId": items_id,
            "itemsAddress": items_address
        }

        return slot_data
