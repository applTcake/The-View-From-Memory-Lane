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
    IGNORED = 6
    INVALID = 7


class CommandParser(Printer):
    def parse_command(self, command):
        command_parts = command.lower().rstrip().split(" ", 1)
        action_name = command_parts[0]
        if len(command_parts) > 1:
            argument = command_parts[1]
        else:
            argument = ''

        if action_name in ['l', 'look', 'examine', 'e', 'inspect', 'observe'] and argument in ['around', 'surroundings',
                                                                                               'room', '']:
            action = ActionType.LOOK_ROOM
        elif action_name in ['l', 'look', 'examine', 'e', 'inspect', 'observe']:
            action = ActionType.LOOK
        elif action_name in ['use', 'u', 'interact']:
            if argument == '':
                self.print('What would you like to interact with?')
                action = ActionType.IGNORED
            else:
                action = ActionType.USE
        elif action_name in ['i', 'inv', 'inventory', 'storage']:
            action = ActionType.INVENTORY
        elif action_name in ['exit', 'bye', 'goodbye', 'quit', 'stop']:
            action = ActionType.EXIT
        elif action_name in ['help', 'h', 'controls', 'ctrls', 'ctrl', 'c', 'rules']:
            action = ActionType.HELP
        else:
            action = ActionType.INVALID
        return Command(action, argument)


class Player(Printer):
    def __init__(self, inventory):
        self.inventory = inventory
        self.lightingStatus = Lighting.DARK
        self.uvStatus = False

    def get_lighting_status(self):
        from game_objects import candle, matches, torch
        change_of_light = False
        self.lightingStatus = Lighting.DARK
        if matches.lightEmit and matches.counter > 0:
            self.lightingStatus = Lighting.DIM
        elif matches.lightEmit or matches.counter > 0:
            matches.lightEmit = False
            matches.stop_tick()
            change_of_light = True
        if candle.lightEmit:
            self.lightingStatus = Lighting.LIGHT
        elif self.lightingStatus == Lighting.DARK and change_of_light:
            self.print('Shadows envelop you once more.')
            if torch.lightEmit and first['torch']:
                lose_innocence(self, 1)
        return self.lightingStatus

    def get_uv_status(self):
        from game_objects import torch
        return torch.lightEmit

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

    def act(self, com):
        from game_objects import empty_can
        from events import ratFocus
        parser = CommandParser()
        parsed_command = parser.parse_command(com)
        command = parsed_command.command
        argument = parsed_command.argument
        if command == ActionType.LOOK_ROOM:
            room.look(self)
        elif command == ActionType.LOOK:
            room.lookat(self, parsed_command.argument)
        elif command == ActionType.USE:
            self.use(room, parsed_command.argument)
        elif command == ActionType.INVENTORY:
            if ratFocus:
                self.print(obscureVision)
            else:
                invlist = []
                for item in player.inv:
                    if (isinstance(item, InvSnack) or item == empty_can) and item.count > 1:
                        invlist.append(item.names[0] + ' x ' + str(item.count))
                    else:
                        invlist.append(item.names[0])
                self.print('You currently have: ' + ', '.join(invlist) + '.')
        elif command == ActionType.HELP:
            self.controls()
        elif command == ActionType.EXIT:
            if yn('Quit game? (y/n) ') == 0:
                exit()
        elif command == ActionType.INVALID:
            self.print("Invalid command. For controls, type 'help'.")

    def use(self, room, item_name):
        allItems = room.items + player.inv
        for item in allItems:
            if item_name in item.names:
                item.use(self, room.get_lighting_status(self), room.get_uv_status(self))
                return
        self.print("You don't have that right now.")

    def tickAll(self):
        all_items = player.inv + room.items
        for item in all_items:
            if isinstance(item, Tickable):
                item.tick()


class Room(Tickable):
    def __init__(self, light, dark, uv, lighting_status, uv_status, tick_actions):
        self.light = light
        self.dark = dark
        self.uv = uv
        self.lightingStatus = lighting_status
        self.uvStatus = uv_status
        Tickable.__init__(self, tick_actions)

    def add_room(self, item):
        room.items.append(item)

    def remove_room(self, item):
        room.items.remove(item)

    def get_lighting_status(self, player):
        return Lighting(
            max(self.lightingStatus.value, player.get_lighting_status().value)
        )

    def get_uv_status(self, player):
        return self.uvStatus or player.get_uv_status()

    def look(self, player):
        from game_objects import vending_machine
        from events import ratFocus
        current_lighting_status = self.get_lighting_status(player)
        current_uv_status = self.get_uv_status(player)
        if ratFocus:
            if current_lighting_status == Lighting.DARK:
                self.print(self.dark)
                self.print("~4But somehow, you can still see it.3&")
            self.print("""There is a rat.
      ~2Its bloated eyes are staring right back at you.2&""")
        else:
            if current_lighting_status == Lighting.DARK:
                if current_uv_status:
                    self.print(self.uv)
                elif vending_machine.count == 1:
                    self.print(keypadGlowing)
                    self.print("Otherwise, you see very little.")
                else:
                    self.print(self.dark)
            else:
                self.print(self.light)
                for item in room.items:
                    if isinstance(item, ItemRoom):
                        item.short_describe(current_lighting_status)

    def lookat(self, player, item_name):
        all_items = player.inv + room.items
        for item in all_items:
            if item_name in item.names:
                item.describe(self.get_lighting_status(player), self.get_uv_status(player))
                break
        else:
            self.print("You currently see no such item in your vicinity.")


room = Room("You are sitting before a wooden table.",
            "It's too dark to see anything at the moment. You couldn't see your hands if you put them in front of "
            "your face.",
            "You can discern very little other than the bluish purple gleam of the torch. You'll need to examine "
            "closer if you want to discover anything with it.",
            Lighting.DARK, False, spider1_Tick)

room.items = [arms, chair, coin_slot, display_case, keypad, legs, me, snack, table, you,
              candle, newspaper_article, vending_machine]
room.hidden = [dead_rat, dead_spider, money_box, rat, room_coin, spider]

player = Player([])
player.inv = [matches]
player.hidden = [coin, empty_can, monster_energy_gun, torch]
player.snacks = [snack1, snack2, snack3, snack4, snack5, snack6, snack7, snack8, snack9]
