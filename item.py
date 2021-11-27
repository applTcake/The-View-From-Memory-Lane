from util import *

TooDark = "It's too dark to see."
Rummage = "You rummage through the gloom to no avail."
cantMove = "You find yourself unable to move."
obscureVision = "The rat obscures your vision."


def display_item(item, action, ls):
    if isinstance(action, str):
        item.print(action)
    else:
        action(item, ls)


def pass_descriptions(item, description, lightStatus, uv, dark_error, uv_error):
    from game_objects import rat
    if len(description) >= 4 and lightStatus == Lighting.DARK and uv:
        display_item(item, description[3], lightStatus)
    elif lightStatus == Lighting.DARK:
        if len(description) > 1 and description[0]:
            display_item(item, description[0], lightStatus)
        elif not uv:
            item.print(dark_error)
        if uv and uv_error and item not in [rat]:
            item.print(uv_error)
    elif len(description) >= 3:
        if lightStatus == Lighting.DIM and description[1]:
            display_item(item, description[1], lightStatus)
        else:
            display_item(item, description[2], lightStatus)
    else:
        display_item(item, description[0], lightStatus)


class Stack():
    def __init__(self, count):
        self.count = count

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1


class LightEmitter():
    def __init__(self, lightEmit):
        self.lightEmit = lightEmit


class Item(Printer):
    def __init__(self, names, description, use):
        self.names = names
        self.description = description
        self.useDescription = use

    def describe(self, lightStatus, uv):
        from game_objects import empty_can, rat
        from events import ratFocus
        if ratFocus and self != rat:
            self.print(obscureVision)
        else:
            pass_descriptions(self, self.description, lightStatus, uv, TooDark,
                             'The torchlight reveals nothing unusual.')
            if (isinstance(self, InvSnack) or self == empty_can) and self.count > 1:
                self.print(f"You currently have {self.count} of them.")

    def use(self, player, lightStatus, uv):
        from events import ratFocus
        if ratFocus:
            self.print(cantMove)
        elif self.useDescription:
            pass_descriptions(self, self.useDescription, lightStatus, uv, Rummage, None)
        else:
            self.print(f"You cannot use the {self.names[0]}.")


class ItemRoom(Item):
    def __init__(self, names, roomDescription, description, useDescription):
        Item.__init__(self, names, description, useDescription)
        self.roomDescription = roomDescription

    def short_describe(self, lightStatus, uv):
        if lightStatus == Lighting.LIGHT and len(self.roomDescription) > 1:
            display_item(self, self.roomDescription[1], lightStatus)
        else:
            display_item(self, self.roomDescription[0], lightStatus)


class ItemCandle(ItemRoom, LightEmitter):
    def __init__(self, names, roomDescription, description, useDescription, lightEmit):
        ItemRoom.__init__(self, names, roomDescription, description, useDescription)
        LightEmitter.__init__(self, lightEmit)


class ItemRoomStack(ItemRoom, Stack):
    def __init__(self, names, roomDescription, description, useDescription, count):
        ItemRoom.__init__(self, names, roomDescription, description, useDescription)
        Stack.__init__(self, count)


class ItemRoomStackTick(ItemRoom, Stack, Tickable):
    def __init__(self, names, roomDescription, description, useDescription, count, tickActions):
        ItemRoom.__init__(self, names, roomDescription, description, useDescription)
        Stack.__init__(self, count)
        Tickable.__init__(self, tickActions)


class ItemRoomTick(ItemRoom, Tickable):
    def __init__(self, names, roomDescription, description, useDescription, tickActions):
        ItemRoom.__init__(self, names, roomDescription, description, useDescription)
        Tickable.__init__(self, tickActions)


class InvTorch(Item, LightEmitter):
    def __init__(self, names, description, useDescription, lightEmit):
        Item.__init__(self, names, description, useDescription)
        LightEmitter.__init__(self, lightEmit)


class InvStack(Item, Stack):
    def __init__(self, names, description, useDescription, count):
        Item.__init__(self, names, description, useDescription)
        Stack.__init__(self, count)


class InvMatches(InvStack, LightEmitter, Tickable):
    def __init__(self, names, description, useDescription, count, lightEmit, tickActions):
        InvStack.__init__(self, names, description, useDescription, count)
        LightEmitter.__init__(self, lightEmit)
        Tickable.__init__(self, tickActions)


class InvSnack(InvStack):
    def __init__(self, names, description, useDescription, count, inVend):
        InvStack.__init__(self, names, description, useDescription, count)
        self.inVend = inVend

    def use(self, player, lightingStatus, uv):
        from events import ratFocus
        from object_use import first
        if ratFocus:
            self.print(cantMove)
        else:
            display_item(self, self.useDescription, lightingStatus)
            player.removeInv(self)
            if first['snack']:
                self.print('~3..welcome home.2&')
                first['snack'] = False


class SpecialSnack(InvSnack):
    def __init__(self, names, description, useDescription, count, countAll, inVend):
        InvSnack.__init__(self, names, description, useDescription, count, inVend)
        self.countAll = countAll
