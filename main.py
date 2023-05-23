from game_objects import *
from item import *

end_game = False

class Command:
    def __init__(self, command, argument):
        self.command = command
        self.argument = argument


class ActionType(Enum):
    LOOK = 0
    LOOK_ROOM = 1
    USE = 2
    INVENTORY = 3
    EXIT = 4
    HELP = 5
    SETTINGS = 6
    IGNORED = 7
    INVALID = 8


inv = ['i', 'inv', 'inventory', 'storage']

#Identifies how to respond to user input
class CommandParser(Printer):
    def parse_command(self, command):
        command_parts = command.lower().rstrip().split(" ", 1)
        action_name = command_parts[0]
        if len(command_parts) > 1:
            argument = command_parts[1]
        else:
            argument = ''

        if action_name in ['l', 'look', 'examine', 'e', 'inspect', 'observe']:
            if argument in ['around', 'surroundings', 'room', 'eye', 'eyes', '']:
                action = ActionType.LOOK_ROOM
            elif argument in inv:
                action = ActionType.INVENTORY
            else:
                action = ActionType.LOOK
        elif action_name in ['use', 'u', 'interact']:
            if argument == '':
                self.print('What would you like to interact with?')
                action = ActionType.IGNORED
            elif argument in ['eye', 'eyes']:
                action = ActionType.LOOK_ROOM
            elif argument in inv:
                action = ActionType.INVENTORY
            else:
                action = ActionType.USE
        elif action_name in inv:
            action = ActionType.INVENTORY
        elif action_name in ['exit', 'bye', 'goodbye', 'quit', 'stop', 'leave', 'end']:
            action = ActionType.EXIT
        elif action_name in ['help', 'h', 'controls', 'ctrls', 'ctrl', 'c', 'rules']:
            action = ActionType.HELP
        elif action_name in ['settings', 'options']:
            action = ActionType.SETTINGS
        else:
            action = ActionType.INVALID
        return Command(action, argument)

# CODE FOR INVENTORY ITEMS
class Player(Printer):
    def __init__(self, inventory):
        self.inventory = inventory
        self.lightingStatus = Lighting.DARK
        self.uvStatus = False

    #Identify brightness based on light-emitting items
    def get_lighting_status(self):
        from game_objects import candle, matches, torch
        change_of_light = False
        self.lightingStatus = Lighting.DARK
        #If match ticking AND match is active, light is dim.
        if matches.lightEmit and matches.counter > 0:
            self.lightingStatus = Lighting.DIM
        #If not both, then no match light, light changes
        elif matches.lightEmit or matches.counter > 0:
            matches.lightEmit = False
            matches.stop_tick()
            change_of_light = True
        #If candle is on, light is bright
        if candle.lightEmit:
            self.lightingStatus = Lighting.LIGHT
        #If dark due to light changes, display The Harsh Message
        elif self.lightingStatus == Lighting.DARK and change_of_light:
            self.print('Shadows envelop you once more.')
            #If torch is on at the time, losing innocence montage
            if torch.lightEmit and first['torch']:
                lose_innocence(self, 1)
        return self.lightingStatus

    #As for uv setting, simply contact the status of your nearest torch ;)
    def get_uv_status(self):
        from game_objects import torch
        return torch.lightEmit

    # Add and remove inv items
    def add_inv(self, item):
        if item not in player.inv:
            player.inv.append(item)
        if isinstance(item, InvStack):
            item.increment()

    def remove_inv(self, item):
        if isinstance(item, InvStack):
            item.decrement()
            if item.count > 0:
                return
        player.inv.remove(item)

# CODE FOR HOW PLAYER ACTS BASED ON COMMAND
    def act(self, com):
        from game_objects import empty_can
        from events import ratFocus
        parser = CommandParser()
        parsed_command = parser.parse_command(com)
        command = parsed_command.command
        argument = parsed_command.argument
        #Look at room
        if command == ActionType.LOOK_ROOM:
            room.look(self)
        #Look at something
        elif command == ActionType.LOOK:
            room.lookat(self, parsed_command.argument)
        #Use something
        elif command == ActionType.USE:
            self.use(room, parsed_command.argument)
        #Inv
        elif command == ActionType.INVENTORY:
            #Rat ruins all
            if ratFocus:
                self.print(obscureVision)
            else:
                invlist = []
                for item in player.inv:
                    #Display number of items if it's a snack-related object
                    if (isinstance(item, InvSnack) or item == empty_can) and item.count > 1:
                        invlist.append(item.names[0] + ' x ' + str(item.count))
                    else:
                        invlist.append(item.names[0])
                self.print('You currently have: ' + ', '.join(invlist) + '.')
        elif command == ActionType.HELP:
            self.controls()
        elif command == ActionType.SETTINGS:
            self.settings()
        elif command == ActionType.EXIT:
            if yn('Quit game? (y/n) ') == 0:
                exit()
        elif command == ActionType.INVALID:
            self.print("Invalid command. For controls, type 'help'.")

#COMMAND FOR USING ITEMS
    def use(self, room, item_name):
        #Look for item
        allItems = room.items + player.inv
        for item in allItems:
            #If item found, get lighting and uv status, describe interaction, and leave program
            if item_name in item.names:
                item.use(self, room.get_lighting_status(self), room.get_uv_status(self))
                return
        self.print("You don't have that right now.")

    #Time passage for all items
    def tickAll(self):
        all_items = player.inv + room.items
        for item in all_items:
            if isinstance(item, Tickable):
                item.tick()


# CODE FOR ROOM ITEMS
class Room(Tickable):
    def __init__(self, light, dark, uv, lighting_status, uv_status, tick_actions):
        self.light = light
        self.dark = dark
        self.uv = uv
        self.lightingStatus = lighting_status
        self.uvStatus = uv_status
        Tickable.__init__(self, tick_actions)

    #Get lighting and uv status from player
    def get_lighting_status(self, player):
        return Lighting(
            max(self.lightingStatus.value, player.get_lighting_status().value)
        )

    def get_uv_status(self, player):
        return self.uvStatus or player.get_uv_status()

    #Add and remove room items
    def add_room(self, item):
        room.items.append(item)

    def remove_room(self, item):
        room.items.remove(item)

#COMMAND FOR LOOKING AROUND ROOM
    def look(self, player):
        from game_objects import vending_machine
        from events import ratFocus
        #Get lighting & uv status
        current_lighting_status = self.get_lighting_status(player)
        current_uv_status = self.get_uv_status(player)
        #Rat ruins everything again
        if ratFocus:
            if current_lighting_status == Lighting.DARK:
                self.print(self.dark)
                self.print("~4But somehow, you can still see it.3&")
            self.print("""There is a rat.
      ~2Its bloated eyes are staring right back at you.2&""")
        else:
            #If dark...
            if current_lighting_status == Lighting.DARK:
                #...and uv, describe uv
                if current_uv_status:
                    self.print(self.uv)
                #...and vending pending, describe vending glow
                elif vending_machine.count == 1:
                    self.print(keypadGlowing)
                    self.print("Otherwise, you see very little.")
                #...it's just dark. Yeah.
                else:
                    self.print(self.dark)
            #If not dark...
            else:
                self.print(self.light)
                #Describe each room item based on lighting status
                for item in room.items:
                    if isinstance(item, ItemRoom):
                        item.short_describe(current_lighting_status)

#COMMAND FOR LOOKING AT ITEMS
    def lookat(self, player, item_name):
        #Look for item
        all_items = player.inv + room.items
        for item in all_items:
            if item_name in item.names:
                #If item found, get lighting and uv status, describe, and leave program
                item.describe(self.get_lighting_status(player), self.get_uv_status(player))
                break
        else:
            self.print("You currently see no such item in your vicinity.")


room = Room(light="You are sitting before a wooden table.",
            dark="It's too dark to see anything at the moment. You couldn't see your hands if you put them in front of "
            "your face.",
            uv="You can discern very little other than the bluish purple gleam of the torch. You'll need to examine "
            "closer if you want to discover anything with it.",
            lighting_status=Lighting.DARK, uv_status=False, tick_actions=rat_Tick)

#Room items
room.items = [arms, candle, chair, coin_slot, display_case, ears, face, head, keypad, legs, me, mescellaneous, mouth,
              articles, nose, snack, table, stuff, vending_machine, you]
#Potential room items
room.hidden = [dead_rat, dead_spider, money_box, project, rat, room_coin, spider]

player = Player([])

#Inventory
player.inv = [matches]
#Potential inventory items
player.hidden = [coin, empty_can, monster_energy_gun, torch]
#All snacks
player.snacks = [snack1, snack2, snack3, snack4, snack5, snack6, snack7, snack8, snack9]
