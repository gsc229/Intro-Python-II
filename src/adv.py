from room import Room
from player import Player
from item import Item
import random
import colorama
from colorama import Fore, Back, Style
colorama.init()


# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     """North of you, the cave mount beckons"""),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}

items = [
    Item("Gold Coins", "A sack of gold coins"),

    Item("Big Knife", "You could do some heavy damage with this knife!"),

    Item("Fear Potion", "Whoever drinks this potion will see what it is they are most afriad of!"),

    Item("Invisibility Cloak",
         "Put on this cloak and you will be invisible, moreover you can move through solid objects!"),

    Item("Empty", "You have no items")
]


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

for rm in room:
    random_item = items[random.randrange(len(items))]
    if random_item.name == "Empty":
        room[rm].items = []
        print(f'{room[rm].name}: {random_item.name}')
    else:
        room[rm].items = []
        room[rm].items.append(random_item)
        print(f'{room[rm].name}: {random_item.name}')
#
# Main
#

# Make a new player object that is currently in the 'outside' room.
player = Player(room['outside'])


def error_msg_1():
    input(Fore.RED +
          "There is no room in that direction. Press [ENTER] to continue" + Style.RESET_ALL)


def view_player_items():
    while True:
        player_items = {}
        input_str = ""
        for indx, item in enumerate(player.items):
            player_items[str(indx)] = item
            input_str = input_str + "\n" + f"[{indx}]" + item.name
        read_more = str(input(
            Fore.MAGENTA + 'Your satchel:' + Style.RESET_ALL + input_str + Fore.MAGENTA + '\nTo read more info, type item number then press [ENTER], or [ENTER] to go back to room... ' + Style.RESET_ALL))

        if not read_more == "":
            input(
                Fore.MAGENTA + f"{player_items[read_more].name} description: " + Style.RESET_ALL + f"\n {player_items[read_more].description} \n Press [ENTER] to continue")
        else:
            break


def view_room_items(room):
    # Loop for finding items
    while True:

        if len(room.items) == 0:
            input(
                f"You have entered the {room.name}, but there are no items. Press [ENTER] to continue...")
            break

        else:
            input_str = ""
            room_items = {}
            # from the room items, create a string for input and a dictionary w/ loop index for the keys
            for indx, item in enumerate(room.items):
                input_str = input_str + "\n" + f"[{indx}]" + item.name
                room_items[str(indx)] = item

            pick_item = input(
                Fore.GREEN + f'In the {room.name} you find the following items:' + Fore.CYAN + input_str + Fore.YELLOW + '\nType an item number to put it in your satchel or press any key to leave item' + Style.RESET_ALL)

            print(pick_item)

            if pick_item == "":
                break
            else:
                try:
                    player.items.append(room_items[pick_item])
                    room.items.remove(room_items[pick_item])
                    print(
                        f'You added {room_items[pick_item].name} to your satchel. Press [ENTER] to return to room!')
                    break
                except KeyError:
                    print(
                        "Hmm, try typing the item name again, or press [ENTER] to leave item behind")


print(Fore.CYAN)

# Loop for chaingin rooms
while True:
    print(
        Fore.CYAN + f'Your current location is: {player.current_room.name}.\n ' + Style.RESET_ALL + Fore.GREEN + f'{player.current_room.description}' + Style.RESET_ALL)

    direction = input(
        Fore.YELLOW + "Choose a direction, [N], [S], [E], [W] or...\nInspect items in your satchel [I] or...\nLook for items in room [L]" + Style.RESET_ALL).lower() + "_to"

    if direction == "i_to":

        if len(player.items) == 0:
            input(
                "You don't have any items in your satchel. Move to rooms to find items! Hit [ENTER] key to continue...")
        else:
            view_player_items()
    # QUIT
    elif direction == "q_to":
        print(Fore.RED + "See ya!" + Style.RESET_ALL)
        break
    elif direction == "l_to":
        view_room_items(player.current_room)
    else:
        try:
            chosen_room = getattr(player.current_room, direction)
            player.current_room = chosen_room
            input(
                Fore.CYAN + f'Your have entered into the {player.current_room.name}.\n ' + Style.RESET_ALL + Fore.GREEN + f'{player.current_room.description}' + Style.RESET_ALL + "\nPress [ENTER] to continue...")
            view_room_items(chosen_room)
        except AttributeError:
            error_msg_1()


# Write a loop that:
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here)
# * Waits for user input and decides what to do.
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.
