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


def pass_descriptions(item, description, light_status, uv, dark_error, uv_error):
    from game_objects import rat, torch
    if len(description) >= 4 and light_status == Lighting.DARK and uv:
        display_item(item, description[3], light_status)
    elif light_status == Lighting.DARK:
        if len(description) > 1 and description[0]:
            display_item(item, description[0], light_status)
        if uv and uv_error and item not in [rat, torch]:
            item.print(uv_error)
        else:
            item.print(dark_error)
    elif len(description) >= 3:
        if light_status == Lighting.DIM and description[1]:
            display_item(item, description[1], light_status)
        else:
            display_item(item, description[2], light_status)
    else:
        display_item(item, description[0], light_status)


class Stack:
    def __init__(self, count):
        self.count = count

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1


class LightEmitter:
    def __init__(self, light_emit):
        self.lightEmit = light_emit


class Item(Printer):
    def __init__(self, names, description, use):
        self.names = names
        self.description = description
        self.useDescription = use

    def describe(self, light_status, uv):
        from game_objects import empty_can, rat
        from events import ratFocus
        if ratFocus and self != rat:
            self.print(obscureVision)
        else:
            pass_descriptions(self, self.description, light_status, uv, TooDark,
                              'The torchlight reveals nothing unusual.')
            if (isinstance(self, InvSnack) or self == empty_can) and self.count > 1:
                self.print(f"You currently have {self.count} of them.")

    def use(self, player, light_status, uv):
        from events import ratFocus
        if ratFocus:
            self.print(cantMove)
        elif self.useDescription:
            pass_descriptions(self, self.useDescription, light_status, uv, Rummage, None)
        else:
            self.print(f"You cannot use the {self.names[0]}.")


class ItemRoom(Item):
    def __init__(self, names, room_description, description, use_description):
        Item.__init__(self, names, description, use_description)
        self.roomDescription = room_description

    def short_describe(self, light_status):
        if light_status == Lighting.LIGHT and len(self.roomDescription) > 1:
            display_item(self, self.roomDescription[1], light_status)
        else:
            display_item(self, self.roomDescription[0], light_status)


class ItemCandle(ItemRoom, LightEmitter):
    def __init__(self, names, room_description, description, use_description, light_emit):
        ItemRoom.__init__(self, names, room_description, description, use_description)
        LightEmitter.__init__(self, light_emit)


class ItemRoomStack(ItemRoom, Stack):
    def __init__(self, names, room_description, description, use_description, count):
        ItemRoom.__init__(self, names, room_description, description, use_description)
        Stack.__init__(self, count)


class ItemRoomStackTick(ItemRoom, Stack, Tickable):
    def __init__(self, names, room_description, description, use_description, count, tick_actions):
        ItemRoom.__init__(self, names, room_description, description, use_description)
        Stack.__init__(self, count)
        Tickable.__init__(self, tick_actions)


class ItemRoomTick(ItemRoom, Tickable):
    def __init__(self, names, room_description, description, use_description, tick_actions):
        ItemRoom.__init__(self, names, room_description, description, use_description)
        Tickable.__init__(self, tick_actions)


class InvTorch(Item, LightEmitter):
    def __init__(self, names, description, use_description, light_emit):
        Item.__init__(self, names, description, use_description)
        LightEmitter.__init__(self, light_emit)


class InvStack(Item, Stack):
    def __init__(self, names, description, use_description, count):
        Item.__init__(self, names, description, use_description)
        Stack.__init__(self, count)


class InvMatches(InvStack, LightEmitter, Tickable):
    def __init__(self, names, description, use_description, count, light_emit, tick_actions):
        InvStack.__init__(self, names, description, use_description, count)
        LightEmitter.__init__(self, light_emit)
        Tickable.__init__(self, tick_actions)


class InvSnack(InvStack):
    def __init__(self, names, description, use_description, count, in_vend):
        InvStack.__init__(self, names, description, use_description, count)
        self.inVend = in_vend

    def use(self, player, light_status, uv):
        from events import ratFocus
        from object_use import first
        if ratFocus:
            self.print(cantMove)
        else:
            display_item(self, self.useDescription, light_status)
            player.remove_inv(self)
            if first['snack']:
                self.print('~3..welcome home.2&')
                first['snack'] = False


class SpecialSnack(InvSnack):
    def __init__(self, names, description, use_description, count, count_all, in_vend):
        InvSnack.__init__(self, names, description, use_description, count, in_vend)
        self.countAll = count_all
