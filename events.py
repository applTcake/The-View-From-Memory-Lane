from util import *
from statuseffects import *

# from playsound import playsound

first = {'match': True, 'candle': True, 'coin': 0, 'machine': 0,
         'snack': True, 'spider': 0, 'torch': True, 'rat': 0, 'uv_news': True}
spiderstatus = '{S} scuttles around on top of the vending machine, disorientedly.'
ratFocus = False
spiderName, SpiderName = 'the spider', 'The spider'


def default_spider():
    global spiderName, SpiderName
    spiderName, SpiderName = 'the spider', 'The spider'


def start_game():
    from util import Printer, yn
    from main import player
    title = 'THE VIEW FROM MEMORY LANE'
    player.print('-' * (Printer.screenWidth - 1))
    num_breaks = int((Printer.screenWidth - 1 - len(title)) / 2)
    breaks = ('-' * num_breaks)
    player.print(breaks + title + breaks)
    player.print('-' * (Printer.screenWidth - 1))
    player.print("""~2    an original puzzle text adventure.
  ~2
  (trigger warning: descriptions of gore, violence and death, spiders, rats and musophobia, isolation.)""")
    if yn('Proceed? (yes/no) ') == 1:
        exit()
    player.controls()
    if yn('Play game? (yesss/nooo) ') == 1:
        exit()


def intro():
    from main import player
    from util import Printer
    for i in range(5):
        player.print('_0.2&&&')
    player.print("""Are you quite dead yet?
    ~2Cause it's so quiet in here.
    ~2You haven't had a new thought in years.
    ~3...
    ~2it's not so bad, i admit.
    ~2but do you really think it will end that easily?
    ~4hehehe
    ~2ahahahahaha..
    ~2
    IT'S TIME FOR YOU TO WAKE UP3&""")

    # """It's quite in here.
    # ~2So quiet.
    # ~2hehehe
    # ~2ahahahahaha...
    # ~4And as much as i'd like for it to stay that way...
    # ~2
    # IT'S TIME FOR YOU TO WAKE UP2&"""
    for i in range(30):
        player.print('_' * Printer.screenWidth + '0.1&&&')
    player.print("""~2huh
  ~1Well this isn't ideal
  ~1You can't see a thing in here
  ~1It's too dark
  ~1What?""")


def events():
    from game_objects import spider, spider_status
    from main import player, room
    if room.counter == 0:
        room.stop_tick()
    if first['spider'] == 1 and player.get_lighting_status() != Lighting.DARK:
        player.print('~2There is a large furry spider before you!!')
        spider1()
        first['spider'] = 3
    elif first['spider'] == 2:
        first['spider'] = 3
    elif first['spider'] == 3:
        spider_status(spider, player.get_lighting_status())
        first['spider'] = 4
    if room.tickActions == spider1_Tick and room.counter == 0 and not first['torch']:
        room.tickActions = rat_Tick
        room.start_tick()
    if first['rat'] == 1:
        first['rat'] = 2
    if room.tickActions == rat_Tick and room.counter == 0 and first['rat'] == 2:
        if spider in room.items:
            room.tickActions = ratHunt_Tick
        else:
            room.tickActions = ratAttack_Tick
        room.start_tick()
    if room.tickActions == ratHunt_Tick and room.counter == 0 and spider in room.items and \
            player.get_lighting_status() != Lighting.DARK and first['spider'] < 5:
        spider_friend()


spider1_Tick = [
    None, None, None, None, None,
    'You hear quiet rustling from up ahead.',
    None, None,
    'The rustling turns into a soft tapping.',
    None, None, None,
    'spider_tense/',
    None, None,
    "spider_tense/{S} deftly climbs down the vending machine. Their limbs are moving rapidly./"
    "~~~1.5Tink tink tink",
    None, None, None,
    "spider_tense/{S} has successfully climbed down the vending machine./~~~1.5stook.",
    None, None, None,
    "spider_tense/{S} is stalking across the newspapers./~2flip flip...  flitflitflit.",
    None, None, None,
    "spider_tense/{S} approaches you./~2Something furry brushes past your hand."
]


def spider_tense(count):
    from game_objects import spider, spider_status
    from main import player, room
    global spiderstatus
    ls = player.get_lighting_status()
    if len(count) == 3:
        spiderstatus = count[1]
        oblivious = count[2]
        if ls == Lighting.DARK and (
                oblivious == "~2Something furry brushes past your hand." or spider not in room.items):
            player.print(oblivious)
        elif spider in room.items:
            spider_status(spider, ls)
            if first['spider'] == 2:
                first['spider'] = 3
    else:
        first['spider'] = 1
        if ls == Lighting.DARK:
            player.print('~1Clink1&')
        else:
            player.print('~2A large furry spider emerges on top of the vending machine!!')
            spider1()


def spider1():
    from main import player, room
    from game_objects import monster_energy_gun, spider
    from util import multi
    from object_use import spider_kill
    room.add_room(spider)
    first['spider'] = 2
    ans = multi(None, 'Do you run or fire your gun or let it be? ',
                (['run'], ['fire', 'gun', 'fire gun', 'fire my gun'], ['let it be', 'let be']), None, False, False)
    if ans == 0:
        player.print("""Whoa there, no need for alarm.
    ~~~0.7It's probably harmless anyway.
    ~~~0.7A huntsman perhaps?
    ~1You looked it up on wikipedia once.1&""")
    elif ans == 1:
        if monster_energy_gun in player.inv:
            spider_kill(spider)
            return
        else:
            player.print("""~2...
      ~2That is quite a violent thought, don't you think?
      ~3I mean, it's just a spider...
      ~3Well,
      ~1  we do what we must.
      ~3Fortunately you don't have a gun.
      ~1teehee0.5&&&""")
    elif ans == 2:
        player.print("""~2That's a nice thought.
    ~3'Let it be.'2&""")
    player.print("Besides, you've always been quite fond of spiders.2&")


rat_Tick = [
    None, None, None,
    """rat_tense/~2You hear a scrabbling of...claws?? on the table.
  ~3(please tell me that spiders have claws)0.5&&&/~2You hear a scrabbling of...claws?? on the table.""",
    None,
    """rat_tense/~1...Yes.
  ~2You think spiders do have claws.2&/""",
    None,
    """rat_tense/~1...
  ~2well that didn't sound like a spider.1&/""",
    None,
    "The scrabbling is getting louder...1&",
    None, None, None,
    """rat_tense/~3A
  ~2it's a rat.2&""",
    None,
    """rat_tense/~2Mice are..passable.
  ~2Some of them are cute, actually.
  ~3Rats are another matter entirely.1&""",
    None, None,
    """rat_tense/~1Hey.
  ~1Breathe.
  ~1There's no need to be afraid.
  ~2Think of it as it being like a spider.
  ~3Look at it.
  ~2It's completely harmless.
  ~4Well, almost.
  ~1So let's not dwell on such things, ok?3&""",
    None
]

ratHunt_Tick = [
    """rat_kill/{S} pounces on the rat!!
  ~2With one swift movement, they sink their fangs into the rat's saggy neck.
  ~4The rat squirms in silent defiance for a few seconds, before its body goes slack.
  ~4Eyes glazed over.
  ~2Staring.
  ~2...
  ~2You love spiders.2&""",
    None, None,
    "rat_kill/{S} is dragging the rat's limp body away./1",
    None, None, None,
    "rat_kill/The rat has been dragged out of view./2",
    None, None, None
]

ratAttack_Tick = [
    None, None,
    """rat_kill/~2...
  ~2It takes you exactly half a second.
  ~2You lift your energy gun with all your might
  ~2..bringing it down to the rat's skull.
  ~3Then, you follow through.
  ~2    over
  ~1and over
  ~1and over
  ~1again.
  ~2...
  ~1I...
  ~2...I think you can stop now.2&"""
]


def rat_tense(count):
    from game_objects import rat, spider
    from main import player, room
    global ratFocus
    if len(count) == 3:
        if spider in room.items:
            player.print(count[1])
        elif count[2] != '':
            player.print(count[2])
    else:
        if rat not in room.items:
            room.add_room(rat)
            ratFocus = True
        elif first['rat'] == 1:
            first['rat'] = 2
            room.counter += 1
            return
        player.print(count[1])


def rat_kill(count):
    from game_objects import dead_rat, rat, spider, monster_energy_gun
    from main import player, room
    global ratFocus, spiderstatus
    player.print(count[1].format(S=SpiderName))
    if len(count) == 3:
        if spider in room.items:
            if count[2] == '1':
                spiderstatus = count[1]
            else:
                room.remove_room(dead_rat)
    else:
        ratFocus = False
        room.remove_room(rat)
        room.add_room(dead_rat)
        if spider in room.items:
            spiderstatus = "{S} carefully assesses their meal."
        else:
            monster_energy_gun.Description = [""""...
      ~2I understand that you have been through...a lot.
      ~3But that does not excuse your behaviour.
      ~3So I implore you
      ~2Please stop.2&""", None, """"...
      ~2I understand that you have been through...a lot.
      ~3But that does not excuse your behaviour.
      ~3So I implore you
      ~2Please stop.2&"""]
            monster_energy_gun.useDescription = ["~1Please stop.2&", None, "~1Please stop.2&"]


def naming_ceremony(name):
    from game_objects import spider, dead_spider
    from main import player
    global SpiderName, spiderName
    spiderName = name
    SpiderName = spiderName
    given_spider = spiderName.lower().rstrip()
    if given_spider in ['spider', 'the spider']:
        player.print('What a creative name!2&')
    elif spiderName:
        spider.names.append(given_spider)
        dead_spider.names.append(given_spider)


def spider_friend():
    from main import player
    from util import yn
    player.print('~2You seem to be growing an attachment to the spider.')
    name = input('What will you name them? ')
    if name:
        naming_ceremony(name)
        player.print("{S} is scuttling about in excitement.2&".format(S=SpiderName))
    else:
        player.print("""Don't want to take away {s}'s right to choose their own name I see?
    ~3{S} appears pleased with your humanitarian ways.2&""".format(S=SpiderName, s=spiderName))
    player.print('They advance towards your hand, staring up at you with a hungry, fervent gaze.5&')
    if yn('Let {s} onto your palm? (yessir/nah bruv) '.format(s=spiderName)) == 0:
        player.print("""{S} steps gingerly onto your right hand with their angular legs.
    ~3First your middle finger, then your pinky, skittering towards the creases of your palm.
    ~4Then, slowly and tenderly, they sink their fangs into your wrist.
    ~6It tickles.
    ~3...
    ~3... huh.
    ~3It's been such an awfully long time since you've have physical contact with anyone...4&""".format(S=SpiderName))
    else:
        player.print('{S} respects your personal space.2&'.format(S=SpiderName))
    player.print('Right. Back to work.')
    first['spider'] = 5
