from util import *

tooDark = "It's too dark to see."
Rummage = "You rummage through the gloom to no avail."
uvNothing = 'The torchlight reveals nothing unusual.'
cantMove = "You find yourself unable to move."
obscureVision = "The rat obscures your vision."


def display_item(item, action, ls):
    if isinstance(action, str):
        item.print(action)
    else:
        action(item, ls)


"""
Current format:

1 description: [light]
2 descriptions (only for room_descriptions): [dim, light]
3 descriptions: [dark, dim, light]
    (same2 fills in dark & light)
4 descriptions: [dark, dim, light, dark & uv]

If dim does not exist, message is replaced with the one from light
Room_descriptions for ItemRooms can only have 1 or 2 descriptions


...But you know what would make this so much easier?

1 description: [light]
2 descriptions: [light, dim]
3 descriptions: [light, dim, dark]
    (same2 fills in light & dark)
4 descriptions: [light, dim, dark, dark + uv]

Basic common sense :)
"""


#Deciding which description to pass based on lighting & uv settings
def pass_descriptions(item, description, light_status, uv, dark_error, uv_error):
    from game_objects import rat, torch
    described = False
    #If more than/equal to 4 descriptions AND dark & uv
    if len(description) >= 4 and light_status == Lighting.DARK and uv:
        #dark + uv
        display_item(item, description[3], light_status)
    #Elif dark...
    elif light_status == Lighting.DARK:
        #...and more than 3 descriptions AND description dark exists, description dark
        if len(description) > 1 and description[0]:
            display_item(item, description[0], light_status)
            described = True
        #...and uv AND no-special-uv-message-here exists, no-special-uv-here message
        if uv and uv_error and item not in [rat, torch]:
            item.print(uv_error)
        #Elif dark message wasn't previously described, too-dark error message
        elif not described:
            item.print(dark_error)
    #Elif more than/equal to 3 descriptions...
    elif len(description) >= 3:
        #...and dim AND description dim exists, description dim
        if light_status == Lighting.DIM and description[1]:
            display_item(item, description[1], light_status)
        #...if not above, light description
        else:
            display_item(item, description[2], light_status)
    #If not anything, description light (default)
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


# Room items
class Item(Printer):
    def __init__(self, names, description, use):
        self.names = names
        self.description = description
        self.useDescription = use

    #When looking at item
    def describe(self, light_status, uv):
        from game_objects import empty_can, rat
        from events import ratFocus
        #rattatta
        if ratFocus and self != rat:
            self.print(obscureVision)
        else:
            pass_descriptions(self, self.description, light_status, uv, tooDark, uvNothing)
            #Count snack-related items.
            if (isinstance(self, InvSnack) or self == empty_can) and self.count > 1:
                self.print(f"You currently have {self.count} of them.")

    #When using item
    def use(self, player, light_status, uv):
        from events import ratFocus
        #RATTATTA
        if ratFocus:
            self.print(cantMove)
        elif self.useDescription:
            pass_descriptions(self, self.useDescription, light_status, uv, Rummage, None)
        #No-use message in case
        else:
            self.print(f"You cannot use the {self.names[0]}.")


# (Special) room items that display a message when looking around room
class ItemRoom(Item):
    def __init__(self, names, room_description, description, use_description):
        Item.__init__(self, names, description, use_description)
        self.roomDescription = room_description

    #When observing room
    def short_describe(self, light_status):
        #If lighting light and there is a specific light description (1), light description
        if light_status == Lighting.LIGHT and len(self.roomDescription) > 1:
            display_item(self, self.roomDescription[1], light_status)
        #Else default/dim description
        else:
            display_item(self, self.roomDescription[0], light_status)


#Special, room items with additional naming options
class ItemSpider(ItemRoom):
    def __init__(self, names, nickname, status, description, use_description):
        ItemRoom.__init__(self, names, status, description, use_description)
        self.nickname = nickname


# Special, light-emitting room items
class ItemCandle(ItemRoom, LightEmitter):
    def __init__(self, names, room_description, description, use_description, light_emit):
        ItemRoom.__init__(self, names, room_description, description, use_description)
        LightEmitter.__init__(self, light_emit)


# Special, stackable room items
class ItemRoomStack(ItemRoom, Stack):
    def __init__(self, names, room_description, description, use_description, count):
        ItemRoom.__init__(self, names, room_description, description, use_description)
        Stack.__init__(self, count)


# Special, stackable AND tickable room items. smh who even uses this
class ItemRoomStackTick(ItemRoom, Stack, Tickable):
    def __init__(self, names, room_description, description, use_description, count, tick_actions):
        ItemRoom.__init__(self, names, room_description, description, use_description)
        Stack.__init__(self, count)
        Tickable.__init__(self, tick_actions)


# Special tickable room items that NO ONE USES
class ItemRoomTick(ItemRoom, Tickable):
    def __init__(self, names, room_description, description, use_description, tick_actions):
        ItemRoom.__init__(self, names, room_description, description, use_description)
        Tickable.__init__(self, tick_actions)


# Light-emitting inv items
class InvTorch(Item, LightEmitter):
    def __init__(self, names, description, use_description, light_emit):
        Item.__init__(self, names, description, use_description)
        LightEmitter.__init__(self, light_emit)


# Stackable inv items
class InvStack(Item, Stack):
    def __init__(self, names, description, use_description, count):
        Item.__init__(self, names, description, use_description)
        Stack.__init__(self, count)


# Light-emitting stackable inv items
class InvMatches(InvStack, LightEmitter, Tickable):
    def __init__(self, names, description, use_description, count, light_emit, tick_actions):
        InvStack.__init__(self, names, description, use_description, count)
        LightEmitter.__init__(self, light_emit)
        Tickable.__init__(self, tick_actions)


# Snacks. Gosh finally something legible.
class InvSnack(InvStack):
    def __init__(self, names, description, use_description, count, in_vend):
        InvStack.__init__(self, names, description, use_description, count)
        self.inVend = in_vend

    #Overriding default use action
    def use(self, player, light_status, uv):
        from events import ratFocus
        from object_use import first
        #Rat messes it up :P
        if ratFocus:
            self.print(cantMove)
        else:
            #display use description based on lighting
            display_item(self, self.useDescription, light_status)
            player.remove_inv(self)
            if first['snack']:
                self.print('~3..welcome home.2&')
                first['snack'] = False


# extra extra spicy candy ;P
class SpecialSnack(InvSnack):
    def __init__(self, names, description, use_description, count, count_all, in_vend):
        InvSnack.__init__(self, names, description, use_description, count, in_vend)
        self.countAll = count_all
