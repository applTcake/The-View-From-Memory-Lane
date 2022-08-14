from item import *
import random
from object_use import *

keypadGlowing = "Squinting in the darkness, you can just make out the hazy glow of the keypad."
needLight = "You'll need some light if you're going to do anything with it."
notStanding = "You don't feel like standing up."
meDescribe = """~1uh
  ~1yes
  ~~~1.5that's certainly you :)2&"""
earTwitch = ''.join(random.choices(["You can't move your ears.", "You wiggle your ears with ease."], [0.8, 0.2]))

# Room Items
arms = Item(
    ['hands', 'hand', 'arm', 'arms', 'fingers', 'finger'],
    [meDescribe], same2('What would you like to interact with?'))


def bright_candle(item, ls):
    item.print(item.description[1])
    item.print("""It is burning passionately.
  Wax occasionally rolls down its side like tears.""")


candle = ItemCandle(["candle", 'candlestick'],
                    ["A skinny candle stands tall before you. It is currently unlit.",
                     "A skinny candle stands tall before you, burning with vehemence."],
                    [None,
                     "The skinny candle stands atop a rusted, bronze candlestick. It's your favourite fragrance too.",
                     bright_candle], [candle_use], False)

chair = Item(['chair', 'seat', 'armchair', 'wooden chair', 'wooden seat', 'wooden armchair'],
             [None, """It's a slightly cramped but comfy wooden armchair, complete with a tattered cushion.
  ~4...
  ~2You remember this chair.""",
              """It's a slightly cramped but comfy wooden armchair, complete with a tattered burlap cushion.
  ~4It has a colourful hand-knitted back, consisting of midnight blues, autumn greens, sunset pinks...
  ~6...
  ~2You remember making this chair.2&"""], same2(notStanding))


def keypad_glow(item, ls):
    from main import player, room
    if vending_machine.count == 1:
        item.print(keypadGlowing)
    elif not room.get_uv_status(player):
        item.print(tooDark)


def keypad_glow_use(item, ls):
    if vending_machine.count == 1:
        item.print("The glow of the keypad isn't quite bright enough for you to operate the machine.")
    elif item == coin:
        item.print(needLight)
    else:
        item.print(Rummage)


coin_slot = Item(['coin slot'],
                 [keypad_glow, None,
                  "The vending machine generously provides a coin slot, with which to leech its users of their money."],
                 [keypad_glow_use, None, vending_use])

display_case = Item(
    ['display case', 'display chamber', 'glass display chamber', 'case', 'glass case', 'glass display case'],
    ["The glass display case has caught a lot of dust over the years, though you can just make out the gaudy "
     "packages of the snacks within."],
    ["""You can't open/break/pry the case in any way.
  Oh, what terrible service!
  ~4Guess you'll have to access its contents via the conveniently-provided coin slot and keypad instead.4&"""])

ears = Item(['ear', 'ears'], same2(meDescribe), same2(earTwitch))


def make_face(item, ls):
    from main import room
    if spider in room.items:
        item.print(spiderFace)
    else:
        item.print('You pull some faces in an attempt to entertain yourself.')


face = Item(['face'], same2(meDescribe), same2(make_face))

head = Item(['head'], same2(meDescribe), same2('You prepare yourself for the deeds you must do.'))

keypad = Item(['keypad', 'keyboard'],
              [keypad_glow, "It's a set of buttons for using the vending machine.",
               "It's a set of buttons from 0 to 9, including a 'Clear' button and an 'Enter' button."],
              [keypad_glow_use, None, vending_use])

legs = Item(['leg', 'legs', 'foot', 'feet', 'knees', 'toe', 'toes', 'body'], [meDescribe], same2(notStanding))

me = Item(['me', 'self', 'myself'], same2(meDescribe),
          same2("""???
  ~1You aren't making any sense.1&"""))

mescellaneous = Item(['shoulders'], [meDescribe], same2("For what?"))


def chat(item, ls):
    from main import room
    if spider in room.items:
        item.print('You try talking to the spider.2&')
        item.print(spiderStory)
    else:
        item.print('You have a nice conversation with yourself.2&')


mouth = Item(['mouth'], same2(meDescribe), same2(chat))


def light_room_news(item, ls):
    item.print(f"""There is a messy pile of articles and papers shoved to the left side of the table.
    The {news[item.count][0][1]} on top reads: {news[item.count][1]}.""")


articles = ItemRoomStack(
    ['article', 'articles', 'news', 'newspapers', 'papers', 'paper', 'magazines'],
    ["There is a haphazard stack of papers on one side of the table.", light_room_news],
    [None, None, article_flip, article_flip], [None, None, article_flip, article_flip], 0)

nose = Item(
    ['nose'], same2(meDescribe),
    ["You don't particularly smell anything.", "You don't particularly smell anything.",
     "The scent from the candle fills the air."])

snack = Item(
    ['snack', 'snacks', 'treat', 'treats', 'junk food', 'junk food'],
    same2(snack_describe), same2(snack_use))

table = Item(
    ['table', 'wooden table'],
    ["It's an old, sturdy, wooden table. A layer of dust covers its surface."],
    ["The table is too heavy to move."])


def money_box_status(item, ls):
    from main import player
    item.print("The money box is disjointed from the vending machine, so you can take out any coins with ease.")
    if vending_machine.count == 1 or coin in player.inv:
        item.print('It is currently empty.')
    else:
        item.print('You see a single coin glistening within it.')


def vending_aha(item, ls):
    from main import room
    if ls == Lighting.DARK:
        item.print("It's too dark to see.")
        return
    elif ls == Lighting.LIGHT:
        item.print("""It's a small table-top vending machine, containing an assortment of junk food.
  The snacks in the display chamber are labelled from 1 to 9, all of which can be accessed from the keypad.
  (dw it was restocked a few days ago, so it's safe to eat.)""")
    else:
        item.print("""It's a small table-top vending machine, containing an assortment of junk food.
  (dw it was restocked a few days ago, so it's safe to eat.)""")
    #If haven't discovered money box yet, discover.
    if first['machine'] == 2:
        item.print("~4Oh, right, I almost forgot.2&")
        first['machine'] = 3
        room.add_room(money_box)
    if first['machine'] == 3:
        money_box_status(item, ls)


vending_machine = ItemRoomStack(
    ['vending machine', 'machine', 'snack machine', 'vending', 'box'],
    ["You see the outline of a box. There seems to be a display case with something inside it.",
     "You see some snacks on display in a small shabby vending machine."],
    [keypad_glow, None, vending_aha], [keypad_glow_use, None, vending_use], 0)

you = Item(
    ['you', 'us'],
    same2("""~1...
  ~2um
  ~2you aren't supposed to do that.
  ~2that would be breaking the fourth wall.
  ~2remember?2&"""),
    same2("""???
  ~1For what purpose?1&"""))

# Hidden Room Items
dead_rat = Item(
    ['rat', 'ratthew'],
    ["""...
   ~2Why is it still staring at you?2&"""],
    ["""...
   ~2You think its for your own good that you don't.1&"""])

dead_spider = Item(['smear', 'spider', 'stain'],
                   ["""~2...
  ~3That's...
  ~3That's just a smear on the table.
  ~4Nothing more.3&"""],
                   ["""...
  ~2..heheh...
  ~2..What do you even mean by that???
  ~3LEAVE
  ~1THE SPIDER
  ~1ALONE.3&"""])

money_box = Item(['money box', 'coin box'],
                 [money_box_status], [vending_use])

project = Item(['project'],
               ["""...
               ~1You'll be fine.
               ~2I promise.2&"""],
               ["""Please, feel free to investigate anything.
               ~2I made it just for you :)1&"""])


def rat_poem(item, ls):
    if first['rat'] == 0:
        item.print("""~2Every breath you take,
    ~~~1.5Every thought you shake,
    ~~~1.5Every word you make your own,
    ~2The rat will be watching you.

    ~3You may succeed
    ~~~1.5   but you shall succumb.
    ~2You may fail
    ~~~1.5   but you shall never fall short
    ~2                          of its gaze.

    ~3Filthy body smeared, dragged over sin
    ~3                             after sin,
    ~1                             after sin.
    ~2Ears pink with youth, as it hears no evil,
    ~4Yet it coats itself in shadow.
    ~~~2.5It saw it all.
    ~~~1.5Oh yes.
    ~~~1.5Yes it did.

    ~3And when you die, it will mould a seed in the coffin of your mind
    ~5Forever sleeping, watching
    ~3begging
    ~~~1.5  for mercy.3&""")
        first['rat'] = 1
    else:
        item.print("""...
    ~2Why.
    ~2Why can't you just look away?2&""")


rat = Item(
    ['rat', 'ratthew'],
    same2(rat_poem), [])

room_coin = Item(
    ['coin', 'gold coin'],
    same2("You'll need to take it out of the vending machine first."), [vending_use])


def spider_status(item, ls):
    from events import spiderstatus, spiderName, SpiderName
    item.print(spiderstatus.format(S=SpiderName, s=spiderName))


def spider_describe(item, ls):
    from events import SpiderName
    spider_status(item, ls)
    item.print("""{S} is hairy with huge protruding legs.
  A huntsman perhaps?""".format(S=SpiderName))
    if ls == Lighting.LIGHT:
        item.print("You also think they're a huntsman because of the lack of cobwebs around.")


spider = ItemRoom(
    ['spider'], [spider_status], [spider_describe], [spider_use])


# Inventory
def matches_description_dark(item, ls):
    item.print(f"""You reach into your pocket and feel the rough texture of a box.""")
    amount = 'several'
    if item.count <= 0:
        item.print("""Sliding it open with your thumb, you notice that there are no more sticks left in the box.
    ~5You sit in silence for a while, contemplating your sheer stupidity.
    ~7
    ~3Lol.2&
    That was very silly of you, though I do congratulate you on your patience.
    I recommend you restart the game now.""")
    elif item.count == 1:
        item.print("""Sliding it open with your thumb, you notice a single wooden stick remaining inside it.
    It is cold and brittle, dead as a bone.
    ~6Alone, just like you.2&""")
    else:
        if item.count <= 5:
            amount = 'a few'
        item.print(f"""Sliding it open with your thumb, you notice {amount} wooden sticks inside it.
    They are cold and brittle, dead as bones.""")


def matches_description_light(item, ls):
    if item.count <= 0:
        item.print("There are no more matches left.")
    elif item.count <= 10:
        item.print("You are running out of matches.")
    else:
        item.print("There are enough matchsticks to last you a while.")
    item.print(f"""The front of the matchbox reads:
  REDHEADS - 1964 Olympics Tokyo. Contents 47 safety matches, made in Australia.
  There is also an illustration of a lady in a black kimono alongside a pictogram of a torch.""")


def matches_burnt():
    from main import player
    player.print("""The flame of the match travels down the stick, nearly burning your fingers.
  You instinctively drop the matchstick onto the ground and stamp it out with your foot.""")
    matches.stop_tick()
    player.get_lighting_status()


matches = InvMatches(
    ['matches', 'matchbox', 'match', 'matchstick', 'matchsticks'],
    [matches_description_dark, None, matches_description_light],
    same2(matches_use), 47, False, [None, None, None, matches_burnt])

# Hidden Inventory Items
coin = Item(
    ['coin', 'gold coin'],
    ["You feel its cold surface hard against the palm of your hand.", None,
     "A simple coin. Nothing much else to speak of."],
    [keypad_glow_use, None, vending_use])

empty_can = InvStack(
    ['empty can', 'can', 'monster can', 'monster energy can'],
    ["The can is significantly lighter than before. Its cylindrical surface cools your palm.", None,
     "It's a can with three claw marks dug onto its side. It's empty, but otherwise intact."],
    same2(can_use), 0)

monster_energy_gun = Item(
    ['Monster Energy Gun', 'monster energy gun', 'gun', 'monster gun', 'energy gun'],
    ["Makeshift rifle swaggg-", None,
     """Swaggy gun you've got there. It looks exactly like one of those you might see on tiktok :DD
  Consisting of 7 Monster Energy cans, this is one of your best crafts yet!"""],
    same2("~2I recommend you don't go swinging that thing around."))


def torch_describe(item, ls):
    if first['torch']:
        if ls == Lighting.DARK:
            item.print("""It's a mini-torch. You can feel its cylindrical shape, cold and metallic against your hand.
      Wonder what it does...?""")
        else:
            item.print("It's a blue mini-torch. Wonder what it does..?")
    else:
        item.print("It's one of those cheapjack LED mini-torches you might see in Officeworks.")
        if ls == Lighting.DARK:
            item.print("You can feel its cylindrical shape, cold and metallic in your hand.")
        if not first['uv_news']:
            item.print("It also happens to be a UV flashlight, which neither improves nor excuses its quality.")
        item.print('Whoever made these puzzles must have really regretted this purchase.')


torch = InvTorch(
    ['torch', 'mini-torch', 'mini torch', 'flashlight', 'uv', 'uv light', 'uv torch', 'uv mini torch', 'uv mini-torch',
     'uv flashlight'],
    same2(torch_describe), same2(torch_use), False)


# Snacks
def friend_shape(item, ls):
    item.print(
        f"You nibble the phrog. You are now filled with"
        f" {''.join(random.choices(['serotonin.', 'hunger.', 'ANGERRRRR'], [0.75, 0.2, 0.05]))}")


snack1 = InvSnack(
    ['Friendo Phrog', 'friendo phrog', 'phrog', 'friendo'],
    ["Feels wholesome.", None,
     """Made of 75% serotonin, 20% hunger.
  ~2and of course, 5% ANGER :)
  ~2(NOTE: No phrogs were harmed during the making of this game.)"""],
    friend_shape,
    0, 10)

snack2 = InvSnack(['PEPCORN', 'pepcorn'],
                  [
                      "You shake the package, attempting to breathe in the spiciness of the Lao Gan Ma Spicy Chilli "
                      "Crisp.",
                      None,
                      '"Perhaps my favourite snack of all time." - bdg'],
                  "Oh!!! Such a delicious, savory, a little bit spicy,, pepcorn. Truly the height of human creation "
                  ":))",
                  0, 8)


def crisp_type(item, ls):
    item.print("""Crisps come in all shapes and sizes. Some are soggy, some are too salty, some are burnt, 
    some are green.
  ~5Some are just right.
  ~3You got the """ + random.choice(['soggy', 'too salty', 'burnt', 'green', 'just right']) + """ crisps.""")


snack3 = InvSnack(['generic crisps', 'crisps'],
                  ["You swear the oil is seeping through the plastic, making your fingers feel grubby and improper.",
                   None,
                   "The fluorescent colours of the packaging reveals that the manufacturers had given up marketing "
                   "this as healthy food a long time ago."],
                  crisp_type, 0, 9)

snack4 = InvSnack(
    ['Smarttles', 'smarttles'],
    ["Sugar pebbles.", None,
     "!!! gay candi-"],
    "You can't tell if it tastes like chocolate or artificial fruit, but its yum.",
    0, 12)

snack5 = InvSnack(
    ['Doritoes: Chilly Nacho', 'doritoes: chilly nacho', 'doritoes chilly nacho', 'doritoe', 'doritoes', 'nachos',
     'chilly nachos', 'chilly nacho', 'nacho'],
    ["The packet feels cool to the touch. You feel a puff of cold air when you shake it.", None,
     "The package has an image of some tortilla chips shaped like foot fingers."],
    "The tips of your fingers grow cold as you snack at the chilly, crisp nachos. You swear there are small specks of "
    "snow attached to its surface.",
    0, 10)

snack6 = InvSnack(
    ['Oreo Wafers', 'oreo wafers', 'oreo', 'wafers', 'wafer'],
    ["It's a lengthy rectangular snack. Its cheap package crackles in your grasp.", None,
     "Cocoa wafers with a creme filling; more specifically, a combination of flour and water dispersions, as well as "
     "partially hydrogenated soybean oil. Yum."],
    """You spend 10 minutes prying open all of the wafer layers, then carefully scrape away the cream.
  You eat the wafers before the cream.""",
    0, 15)

snack7 = SpecialSnack(
    ['Monster Energy drink', 'monster energy drink', 'monster', 'energy drink', 'monster energy'],
    ["The cylindrical can is cool against your hand.", None,
     "It's a can with three claw marks dug onto its side. What more is there to say?"],
    monster_use, 0, 0, 7)

snack8 = InvSnack(
    ["Isnott's Trapezoids", "isnott's trapezoids", "isnotts trapezoids", "isnotts", "isnott's", 'isnott', 'trapezoids'],
    ["You gently shake the packet. Mm. Biscuits.", None,
     "Not a counterfeit."],
    "Cronchy. Your fingers are all powdery now, but it's worth it.",
    0, 12)

snack9 = InvSnack(
    ['Berries and Cream', 'berries and cream', 'berries & cream', 'berries n cream'],
    ["You swear you hear the faint laughter of a little lad.", None,
     """~2Hm.
  ~2Curious.
  ~2It reminds you of a song...3&"""],
    "The berries and the cream mix perfectly in your mouth, dancing in sync.",
    0, 20)
