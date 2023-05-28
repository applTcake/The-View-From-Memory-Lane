from util import *
from statuseffects import *
import audio

first = {'match': True, 'candle': True, 'coin': 0, 'machine': 0,
         'snack': True, 'spider': 0, 'torch': True, 'rat': 0, 'uv_news': True}
"""
    match, candle, torch: toggled on for first time
    coin:
        1 - got to required article
        2 - coin fell to table; player took it
    machine:
        1 - inserted coin (glowing keypad mode)
        2 - item selected (looking for money box mode)
        3 - recognised existence of money box
        (Similar to vending_machine_count, except goes from 2 to 0 when coin retrieved)
    snack: '..welcome home.'
    spider:
        1 - appeared on vending machine
        2 - recognised existence of spider
        3 - 
        4 - described spider status
        5 - befriended spider
    rat:
    uv_news:
"""

ratFocus = False


def start_game():
    from util import yn, screenWidth
    from main import player
    title = 'THE VIEW FROM MEMORY LANE'
    #screenWidth-1 if len(title) is an even number
    player.print('-' * (screenWidth - 1))
    num_breaks = int((screenWidth - 1 - len(title)) / 2)
    breaks = ('-' * num_breaks)
    player.print(breaks + title + breaks)
    player.print('-' * (screenWidth - 1))
    player.print("""~2    an original puzzle text adventure.
  ~2
  (trigger warning: descriptions of gore, violence and death, spiders, rats and musophobia, isolation.)""")
    #Start-of-game formalities
    if yn('Proceed? (yes/no) ') == 1:
        exit()
    player.controls()
    if yn('Play game? (yesss/nooo) ') == 1:
        exit()


def intro():
    from main import player
    from util import screenWidth
    #print five of these underscore thingys just because.
    for i in range(5):
        player.print('_0.2&&&')
    player.print("""are you dead yet?
    ~2cause it's so quiet in here.
    ~2and all of your thoughts are rotting away at the edges..
    ~3...
    ~2it's not so bad, i admit.
    ~2and maybe it can be a comfort.
    ~3but do you really think you can go that easily?
    ~4hehehe
    ~2ahahahahaha..
    ~2
    IT'S TIME FOR YOU TO WAKE UP3&""")

    '''It's quite in here.
     ~2So quiet.
     ~2hehehe
     ~2ahahahahaha...
     ~4And as much as i'd like for it to stay that way...
     ~2
     IT'S TIME FOR YOU TO WAKE UP2&'''

    for i in range(30):
        player.print('_' * screenWidth + '0.1&&&')
    player.print("""~2huh
  ~1Well this isn't ideal
  ~1You can't see a thing in here
  ~1It's too dark
  ~1What?""")

#Checked each turn:
def events():
    from game_objects import spider, spider_status
    from main import player, room
    #Just in case to prevent it from ticking down further
    if room.counter == 0:
        room.stop_tick()
    #Spider appear and turn the lights on = spider encounter
    if first['spider'] == 1 and player.get_lighting_status() != Lighting.DARK:
        player.print('~2There is a large furry spider before you!!')
        spider1()
        first['spider'] = 3
    #
    elif first['spider'] == 2:
        first['spider'] = 3
    #If phase 3, describe spider status
    elif first['spider'] == 3:
        spider_status(spider, player.get_lighting_status())
        first['spider'] = 4
    #If ended spider tick or started bonus ticks and no rat encounters AND torch found. Initiate rattattack.
    if ((room.tickActions == spider1_Tick and room.counter == 0) or (
            room.tickActions == vibe_Tick and first['rat'] == 0)) and not first['torch']:
        room.tickActions = rat_Tick
        room.start_tick()
    #If spider ticked once and ended, start bonus ticks
    elif room.tickActions == spider1_Tick and room.counter == 0 and first['machine'] >= 2:
        room.tickActions = vibe_Tick
        room.start_tick()
    #
    if first['rat'] == 1:
        first['rat'] = 2
    #If rat has traumatised sufficiently traumatised its victim.
    if room.tickActions == rat_Tick and room.counter == 0 and first['rat'] == 2:
        #Spider aid
        if spider in room.items:
            room.tickActions = ratHunt_Tick
        #The Alternative
        else:
            room.tickActions = ratAttack_Tick
        room.start_tick()
    #If rat hunt is over, room isn't dark, the spider made it and still hasn't been befriended. BEFRIEND.
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
    f"spider_tense/SP1 deftly climbs down the vending machine. Their limbs are moving rapidly./"
    "~~~1.5Tink tink tink",
    None, None, None,
    f"spider_tense/SP1 has successfully climbed down the vending machine./~~~1.5stook.",
    None, None, None,
    f"spider_tense/SP1 is stalking across the newspapers./~2flip flip...  flitflitflit.",
    None, None, None,
    f"spider_tense/SP1 approaches you./~2Something furry brushes past your hand."
]


def spider_tense(count):
    from game_objects import spider, spider_status
    from main import player, room
    global spiderstatus
    ls = player.get_lighting_status()
    #If tick has: (1) spider_tense, (2) visible spider status, (3) oblivious spider status:
    if len(count) == 3:
        spiderstatus = count[1]
        oblivious = count[2]
        #If dark AND brushing past status or spider unrecognised, oblivious
        if ls == Lighting.DARK and (
                oblivious == "~2Something furry brushes past your hand." or spider not in room.items):
            player.print(oblivious)
        #Elif spider recognised, spider status
        elif spider in room.items:
            spider_status(spider, ls)
            #Up a phase
            if first['spider'] == 2:
                first['spider'] = 3
    #Else, first spider_tense
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
                (['run'], ['fire', 'gun', 'fire gun', 'fire my gun'], ['let it be', 'let be']), try_again=None,
                original_result=False, tuples=False)
    if ans == 0: #run
        player.print("""Whoa there, no need for alarm.
    ~~~0.7It's probably harmless anyway.
    ~~~0.7A huntsman perhaps?
    ~1You looked it up on wikipedia once.1&""")
    elif ans == 1: #fire gun
        #For those who've hacked the game...
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
    elif ans == 2: #let be
        player.print("""~2That's a nice thought.
    ~3'Let it be.'2&""")
    player.print("Besides, you've always been quite fond of spiders.2&")


vibe_Tick = [None, None,
             f'spider_vibe/SP1 is striding around the candlestick.',
             None, None, None,
             f'spider_vibe/SP1 is crawling on the vending machine.',
             None, None, None,
             f'spider_vibe/SP1 is stalking across the newspapers.',
             None, None, None,
             f'spider_vibe/SP1 approaches you.',
             None]


#Changing spider status in the background-
def spider_vibe(count):
    global spiderstatus
    spiderstatus = count[1]


rat_Tick = [
    None, None, None, None, None,
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
    f"""rat_kill/SP1 pounces on the rat!!
  ~2With one swift movement, they sink their fangs into the rat's saggy neck.
  ~4The rat squirms in silent defiance for a few seconds, before its body goes slack.
  ~4Eyes glazed over.
  ~2Staring.
  ~2...
  ~2You love spiders.2&""",
    None, None,
    f"rat_kill/SP1 is dragging the rat's limp body away./1",
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
    #If 3 messages, last of which implies spider dead
    if len(count) == 3:
        #Print first message if spider is alive and well, otherwise...
        if spider in room.items:
            player.print(count[1])
        elif count[2] != '':
            player.print(count[2])
    #Else, Rat Presence.
    else:
        audio.loop('4280_pitch')
        #RECOGNISE THE RAT.
        if rat not in room.items:
            room.add_room(rat)
            ratFocus = True
        #
        elif first['rat'] == 1:
            first['rat'] = 2
            room.counter += 1
            return
        player.print(count[1])


def rat_kill(count):
    from game_objects import dead_rat, rat, spider, monster_energy_gun, same2
    from main import player, room
    global ratFocus, spiderstatus
    audio.sound('nothing')
    player.print(count[1])
    #If spider is clearing the scene
    if len(count) == 3:
        if spider in room.items:
            #First time, make message spider status
            if count[2] == '1':
                spiderstatus = count[1]
            #Second time, remove rat
            else:
                room.remove_room(dead_rat)
    #Else, the moment of killing
    else:
        ratFocus = False
        room.remove_room(rat)
        room.add_room(dead_rat)
        #Spider cleaning service
        if spider in room.items:
            spiderstatus = f"{spider.nickname[1]} carefully assesses their meal."
        #Else, additional gun character development
        else:
            monster_energy_gun.Description = same2(""""...
      ~2I understand that you have been through...a lot.
      ~3But that does not excuse your behaviour.
      ~3So I implore you
      ~2Please stop.2&""")
            monster_energy_gun.useDescription = same2("~1Please stop.2&")


def naming_ceremony(name):
    from game_objects import spider, dead_spider
    from main import player
    spider.nickname[0] = name
    spider.nickname[1] = spider.nickname[0]
    #If spider named spider, it's creative :)
    given_spider = spider.nickname[0].lower().rstrip()
    if given_spider in ['spider', 'the spider']:
        player.print('What a creative name!2&')
    #Offically add name to spider list
    elif spider.nickname[0]:
        spider.names.append(given_spider)
        dead_spider.names.append(given_spider)


def spider_friend():
    from main import player
    from util import yn
    player.print('~2You seem to be growing an attachment to the spider.')
    name = input('What will you name them? ')
    if name:
        naming_ceremony(name)
        player.print(f"SP1 is scuttling about in excitement.2&")
    else:
        player.print(f"""Don't want to take away SP1's right to choose their own name I see?
    ~3SP1 appears pleased with your humanitarian ways.2&""")
    player.print('They advance towards your hand, staring up at you with a hungry, fervent gaze.5&')
    if yn(f'Let SP0 onto your palm? (yessir/nah bruv) ') == 0:
        player.print(f"""SP1 steps gingerly onto your right hand with their angular legs.
    ~3First your middle finger, then your pinky, skittering towards the creases of your palm.
    ~4Then, slowly and tenderly, they sink their fangs into your wrist.
    ~6It tickles.
    ~3...
    ~3... huh.
    ~3It's been such an awfully long time since you've have physical contact with anyone...4&""")
    else:
        player.print(f'SP1 respects your personal space.2&')
    player.print('Right. Back to work.')
    first['spider'] = 5
