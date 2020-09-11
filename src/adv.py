from room import Room
from player import Player
from item import Item
from textwrap import wrap
import os

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room(
        "Treasure Chamber",
        """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south.""",
        [
            Item("Vader's Saber", "What feels to be unlimited power eminates from this weapon"),

        ]),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

player = Player(room['outside'])
action_res = []
CARDINALS = ["n", "e", "s", "w"]

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
    return input("> ")

while True:
    cls()
    print_room()
    print_action_response()

    do = read_input()
    if len(do) == 0:
        continue
    elif do in CARDINALS:
        moved = player.move(do)
        if not moved:
            action_res.append(f"Unable to move rooms in direction {do}")
        continue
    elif do == "q":
        break
    elif do == "items":
        if len(player.items) > 0:
            action_res.append("Your items:")
            action_res.extend(f"- {item}" for item in player.items)
        else:
            action_res.append("No items")
    else:
        action_res.append(f"Invalid command '{do}'")
