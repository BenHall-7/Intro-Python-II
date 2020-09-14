from room import Room, Room_Overlook
from player import Player
from item import Item, BBQ
from textwrap import wrap
from error import GameEndError
import os

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room_Overlook("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'floor': Room("Chasm floor", """You land in a pool of water. Bones of past explorers
line the corners of this dark cave... North of you, a cavity with flickering gold lights"""),

    'end': Room("Grand Chamber", """Surrounding you, treasures beyond your wildest imagination!
Behind you, the entrance has caved...""", [
        Item("Chalice", "Solid gold and lined with rubies, fit for none nobler than youself ;)"),
        Item("Necklace", "Built with more gemstones than you can name"),
        Item("Gold coins", "What seems to be a foreign, ancient language is inscribed in these..."),
        Item("Throne", "Conveniently placed by the Barbeque, and exceptionally lavish"),
        BBQ("Fresh BBQ", "Tasty char-grilled sirloin steak prepared just for you. Now THIS is the real prize here.")
    ]),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room(
        "Treasure Chamber",
        """You've found the long-lost treasure
chamber! Sadly, it has already been mostly emptied by
earlier adventurers. The only exit is to the south.""",
        [
            Item("Parachute", "A cheap parachute left here by explorers"),
        ]),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['overlook'].n_to = room['floor']
room['floor'].n_to = room['end']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

player = Player(room['outside'])
action_res = []

# clear screen func
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def print_room():
    global player
    print(f"Current room: {player.room.name}")

    print("Description:")
    descr = wrap(player.room.description, initial_indent='  ', subsequent_indent='  ', width=64)
    for d in descr: print(d)

    if len(player.room.items) > 0:
        print("Items in room:")
        for item in player.room.items:
            print(f"- {item}")
    
    print()

def print_action_response():
    global action_res
    for l in action_res:
        print(l)
        print()

def read_input():
    global action_res
    action_res = []
    # sanitize inputs by removing empty entries caused by extra spaces
    return [s for s in input("> ").split(" ") if len(s) > 0]

while True:
    cls()
    print_room()
    print_action_response()

    do = read_input()
    try:
        if len(do) == 0:
            continue
        elif do[0] in ["n", "e", "s", "w"]:
            moved = player.move(do[0])
            if not moved:
                action_res.append(f"Unable to move {do[0]}")
        elif do[0] == "q":
            break
        elif do[0] in ["i", "inventory"]:
            if len(player.items) > 0:
                action_res.append("Your items:")
                action_res.extend(f"- {item}" for item in player.items)
            else:
                action_res.append("No items")
        elif do[0] in ["get", "take", "drop"]:
            if len(do) == 1:
                action_res.append(f"Expected item name. e.g: {do[0]} katana")
            else:
                item_name = " ".join(do[1:])
                drop = do[0] == "drop"
                # decide which list to search (room or player items)
                # based on if dropping the item
                search = player.room.items if not drop else player.items
                # case-agnostic search
                item = next((item for item in search if item.name.lower() == item_name.lower()), None)
                if item == None:
                    action_res.append(f"No weapon with the name '{item_name}' in room")
                elif drop:
                    player.items.remove(item)
                    player.room.items.append(item)
                    on_drop = item.on_drop()
                    if "print" in on_drop:
                        action_res.append(on_drop["print"])
                else:
                    player.items.append(item)
                    player.room.items.remove(item)
                    on_take = item.on_take()
                    if "print" in on_take:
                        action_res.append(on_take["print"])
        else:
            action_res.append(f"Invalid command '{do[0]}'")
    except GameEndError as e:
        print()
        print(e.message)
        break
