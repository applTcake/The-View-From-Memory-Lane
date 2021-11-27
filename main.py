from game_objects import *
from statuseffects import *
from util import *
from events import *
from item import *
import random

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
    def parseCommand(self, command):
        commandParts = command.lower().rstrip().split(" ", 1)
        actionName = commandParts[0]
        if len(commandParts) > 1:
            argument = commandParts[1]
        else:
            argument = ''

        if actionName in ['l', 'look', 'examine', 'e', 'inspect', 'observe'] and argument in ['around', 'surroundings',
                                                                                              'room', '']:
            action = ActionType.LOOK_ROOM
        elif actionName in ['l', 'look', 'examine', 'e', 'inspect', 'observe']:
            action = ActionType.LOOK
        elif actionName in ['use', 'u', 'interact']:
            if argument == '':
                self.print('What would you like to interact with?')
                action = ActionType.IGNORED
            else:
                action = ActionType.USE
        elif actionName in ['i', 'inv', 'inventory', 'storage']:
            action = ActionType.INVENTORY
        elif actionName in ['exit', 'bye', 'goodbye', 'quit', 'stop']:
            action = ActionType.EXIT
        elif actionName in ['help', 'h', 'controls', 'ctrls', 'ctrl', 'c', 'rules']:
            action = ActionType.HELP
        else:
            action = ActionType.INVALID
        return Command(action, argument)


class Player(Printer):
    def __init__(self, inventory):
        self.inventory = inventory
        self.lightingStatus = Lighting.DARK
        self.uvStatus = False

    def getLightingStatus(self):
        from game_objects import candle, matches, torch
        changeOfLight = False
        self.lightingStatus = Lighting.DARK
        if matches.lightEmit and matches.counter > 0:
            self.lightingStatus = Lighting.DIM
        elif matches.lightEmit or matches.counter > 0:
            matches.lightEmit = False
            matches.stopTick()
            changeOfLight = True
        if candle.lightEmit:
            self.lightingStatus = Lighting.LIGHT
        elif self.lightingStatus == Lighting.DARK and changeOfLight:
            self.print('Shadows envelop you once more.')
            if torch.lightEmit and first['torch']:
                LoseInnocence(self, 1)
        return self.lightingStatus

    def getUvStatus(self):
        from game_objects import torch
        return torch.lightEmit

    def addInv(self, item):
        if item not in self.inv:
            self.inv.append(item)
        if isinstance(item, InvStack):
            item.increment()

    def removeInv(self, item):
        if isinstance(item, InvStack):
            item.decrement()
            if item.count > 0:
                return
        self.inv.remove(item)

    def act(self, com):
        from game_objects import empty_can
        from events import ratFocus
        parser = CommandParser()
        parsedCommand = parser.parseCommand(com)
        command = parsedCommand.command
        argument = parsedCommand.argument
        if command == ActionType.LOOK_ROOM:
            room.look(self)
        elif command == ActionType.LOOK:
            room.lookAt(self, parsedCommand.argument)
        elif command == ActionType.USE:
            self.use(room, parsedCommand.argument)
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
                self.print('You currently have: ' + (', ').join(invlist) + '.')
        elif command == ActionType.HELP:
            self.controls()
        elif command == ActionType.EXIT:
            if yn('Quit game? (y/n) ') == 0:
                exit()
        elif command == ActionType.INVALID:
            self.print("Invalid command. For controls, type 'help'.")

    def use(self, room, itemName):
        allItems = room.items + self.inv
        for item in allItems:
            if itemName in item.names:
                item.use(self, room.getLightingStatus(self), room.getUvStatus(self))
                return
        self.print("You don't have that right now.")

    def tickAll(self):
        allItems = self.inv + room.items
        for item in allItems:
            if isinstance(item, Tickable):
                item.tick()


class Room(Tickable):
    def __init__(self, light, dark, uv, lightingStatus, uvStatus, tickActions):
        self.light = light
        self.dark = dark
        self.uv = uv
        self.lightingStatus = lightingStatus
        self.uvStatus = uvStatus
        Tickable.__init__(self, tickActions)

    def addRoom(self, item):
        self.items.append(item)

    def removeRoom(self, item):
        self.items.remove(item)

    def getLightingStatus(self, player):
        return Lighting(
            max(self.lightingStatus.value, player.getLightingStatus().value)
        )

    def getUvStatus(self, player):
        return self.uvStatus or player.getUvStatus()

    def look(self, player):
        from game_objects import vending_machine
        from events import ratFocus
        currentLightingStatus = self.getLightingStatus(player)
        currentUvStatus = self.getUvStatus(player)
        if ratFocus:
            if currentLightingStatus == Lighting.DARK:
                self.print(self.dark)
                self.print("~4But somehow, you can still see it.3&")
            self.print("""There is a rat.
      ~2Its bloated eyes are staring right back at you.2&""")
        else:
            if currentLightingStatus == Lighting.DARK:
                if currentUvStatus:
                    self.print(self.uv)
                elif vending_machine.count == 1:
                    self.print(keypadGlowing)
                    self.print("Otherwise, you see very little.")
                else:
                    self.print(self.dark)
            else:
                self.print(self.light)
                for item in self.items:
                    if isinstance(item, ItemRoom):
                        item.short_describe(currentLightingStatus, currentUvStatus)

    def lookAt(self, player, itemName):
        allItems = player.inv + self.items
        for item in allItems:
            if itemName in item.names:
                item.describe(self.getLightingStatus(player), self.getUvStatus(player))
                break
        else:
            self.print("You currently see no such item in your vicinity.")


room = Room("You are sitting before a wooden table.",
            "It's too dark to see anything at the moment. You couldn't see your hands if you put them in front of your face.",
            "You can discern very little other than the bluish purple gleam of the torch. You'll need to examine closer if you want to discover anything with it.",
            Lighting.DARK, False, spider1_Tick)

room.items = [arms, chair, coin_slot, display_case, keypad, legs, me, snack, table, you,
              candle, newspaper_article, vending_machine]
room.hiddenitems = [dead_rat, dead_spider, money_box, rat, room_coin, spider]

player = Player([])
player.inv = [matches]
player.hidden = [coin, empty_can, monster_energy_gun, torch]
player.snacks = [snack1, snack2, snack3, snack4, snack5, snack6, snack7, snack8, snack9]
