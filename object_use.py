from game_objects import *
from util import *

bnc = False
back = ['b', 'back', 'return', 'escape', 'esc']


def ease_to_dark():
    from main import player
    from game_objects import torch
    if player.get_lighting_status() == Lighting.DARK:
        player.print("You're welcomed once more into a realm of merciful darkness.")
        if torch.lightEmit and first['torch']:
            lose_innocence(player, 1)


def matches_use(item, ls):
    if item.counter > 0:
        if yn("Blow out matchstick? (yep/nope) ") == 0:
            item.stop_tick()
            item.lightEmit = False
            ease_to_dark()
    elif item.count == 0:
        item.print("You don't have any matches left to light.")
    else:
        if ls == Lighting.DARK:
            item.print('You strike a match. You start to discern some things in front of you.')
            if first['match']:
                item.print('~2..Turn back now. This is your final warning.2&')
                first['match'] = False
        else:
            item.print("You strike another match. The room is already bright enough to see because of the candle.")
        item.decrement()
        item.start_tick()
        item.lightEmit = True


def candle_use(item, ls):
    from game_objects import matches
    if ls == Lighting.DIM:
        if first['candle']:
            item.print("""As you transfer the flame of the match to the candle, you are taken aback by how vibrantly the wick blazes up.
      ~3It is as though the candle has been aching for this precise moment for a very, very long time.
      ~4The brightness hurts your eyes a little, as the dancing light illuminates your vicinity with greater clarity.4&""")
            first['candle'] = False
        else:
            item.print('The fire returns to the candle, with the vigour of a starved traveller drinking from an oasis.')
        item.print("You blow out the match.")
        matches.stop_tick()
        matches.LightEmit = False
        item.lightEmit = True
    else:
        if yn('Blow out candle? (yup/nup) ') == 0:
            item.print('You swear the flame gives out a scream as you snuff it out with ease.2&')
            item.lightEmit = False
            ease_to_dark()


def lose_innocence(item, num):
    if num == 1:
        item.print("~2The faintness of the torch remains the same, dimmer than ever.")
    item.print("""~3...
  ~2This is well and truly a rip-off.2&""")
    first['torch'] = False


def torch_use(item, ls):
    from game_objects import torch
    if not torch.lightEmit:
        item.print('A muted blue glow shines out from the torch, barely visible to the eye.')
        if ls == Lighting.DARK and first['torch']:
            lose_innocence(item, 0)
        elif not first['torch']:
            item.print('Another great example of a pathetic UV flashlight.')
    else:
        item.print('You turn off the torch.')
    torch.lightEmit = not torch.lightEmit


news = [['DADADADADA', 'Someone went missing..', 'SECRET MESSAGE!!!'],
        ['MISSING PERSONS', 'see previous article', "GAHAHA THIS WAS MY EVIL PLAN ALL ALONG!!"],
        ['SPORTS NEWS',
         """REMEMBER: THE CODE IS...
      psyche! not gonna tell you! <333""",
         "double psyche >:)"]]


def news_flip(item, ls):
    from game_objects import torch, coin
    from main import player
    ans = None
    p = ['p', 'prev', 'previous']
    n = ['n', 'next', 'next']
    b = back
    while ans != b:
        if ls == Lighting.LIGHT:
            item.print('\n' + news[item.count][0] + '\n\n' + news[item.count][1] + '\n')
        elif ls == Lighting.DIM:
            item.print(f"""It is a newspaper article with the headline: {news[item.count][0]}.
      You'll need some more light to read all of it.""")
        if torch.lightEmit:
            if first['uv_news']:
                item.print("""~4Oh.
        ~1The torchlight reveals something else written on the newspaper.3&""")
                if ls != Lighting.DARK:
                    item.print("""A series of annotations, urgently scrawled out on its margins.2&
          The light is feeble, so you'll need to darken the room to see it more clearly.2&""")
                first['uv_news'] = False
            elif ls != Lighting.DARK:
                item.print("""The torchlight reveals something else written on the newspaper: a series of annotations, urgently scrawled out on its margins.
                   The light is feeble, so you'll need to darken the room to see it more clearly.""")
            if ls == Lighting.DARK:
                item.print('\n' + news[item.count][0] + '\n\n' + news[item.count][2] + '\n')
        if item.count == 0:
            ans = multi(None, "(Type 'next' to move between articles. Type 'back' to return.) ", (b, n), None, True,
                        False)
        elif item.count == 2:
            if first['coin'] == 0:
                first['coin'] = 1
            ans = multi(None, "(Type 'previous' to move between articles. Type 'back' to return.) ", (b, p), None, True,
                        False)
        else:
            ans = multi(None, "(Type 'previous' or 'next' to move between articles. Type 'back' to return.) ",
                        (b, p, n), None, True, False)
        if ans == p:
            item.decrement()
        elif ans == n:
            item.increment()
    if first['coin'] == 1:
        item.print("""As you're rifling through the pages, a single coin falls to the table, spinning and rattling briefly as it comes to a stop near your fingertips.
    ~5You take the coin.1&""")
        player.add_inv(coin)
        first['coin'] = 2


def snack_describe(item, ls):
    from main import player, room
    treats = []
    for items in player.inv:
        if items in player.snacks:
            treats.append(items)
    if len(treats) == 0:
        item.print("You'll need to buy one first.")
    elif len(treats) == 1:
        items.describe(room.get_lighting_status(player), room.get_uv_status(player))
    else:
        item.print("Which snack are you referring to?")


def snack_use(item, ls):
    from main import player, room
    treats = []
    for items in player.inv:
        if items in player.snacks:
            treats.append(items)
    if len(treats) == 0:
        item.print("You'll need to buy one first.")
    elif len(treats) == 1:
        items.use(player, room.get_lighting_status(player), room.get_uv_status(player))
    else:
        item.print("Which snack are you referring to?")


def keypad_nope(item, ans):
    if len(ans) > 3:
        item.print("You can only enter a maximum of 3 digits.")
    elif ans.isnumeric():
        item.print('Invalid number. Item does not exist.')


def end_vending():
    from game_objects import room_coin, vending_machine
    from main import room
    if first['machine'] == 1:
        first['machine'] = 2
        room.start_tick()
    vending_machine.count = 2
    room.add_room(room_coin)


def vending_use(item, ls):
    from game_objects import vending_machine, coin, room_coin, money_box, keypad, snack7, torch, coin_slot
    from main import player, room
    if item == money_box and room_coin not in room.items:
        item.print('The money box is currently empty.')
        return
    elif vending_machine.count == 0 or first['machine'] == 2 or (
            item in [keypad, coin_slot] and vending_machine.count == 2):
        if coin not in player.inv:
            if item == room_coin:
                item.print("You don't have that with you right now.")
            else:
                item.print("You'll need to insert a coin first.")
            return
        else:
            item.print('You insert the coin into the vending machine. The keypad glows up, faint as it may be.')
            player.remove_inv(coin)
            if first['machine'] == 0:
                item.print("""~3...wow.
        ~2it...still works.2&""")
                first['machine'] += 1
            vending_machine.increment()
    if vending_machine.count == 1:
        while True:
            code = int(multi(item, "Enter number into keypad (press 'back' to return): ",
                             (['001', '01', '1'], ['002', '02', '2'], ['003', '03', '3'],
                              ['004', '04', '4'], ['005', '05', '5'], ['006', '06', '6'],
                              ['007', '07', '7'], ['008', '08', '8'], ['009', '09', '9'],
                              ['333'],
                              back), keypad_nope, False, False))
            if code == 10:
                return
            elif code == 9:
                if torch not in player.inv:
                    item.print("""The vending machine whirs into action, then with a small clank, produces a single..
          ~4...torch.
          ~2You take it with you.1&""")
                    player.add_inv(torch)
                    end_vending()
                    return
                else:
                    item.print('This product is already sold out.')
            else:
                snack = player.snacks[int(code)]
                if snack.inVend == 0:
                    item.print('This product is already sold out.')
                else:
                    break

        if snack == snack7:
            item.print(
                f"The vending machine whirs into action, then with a small clank, produces a single {snack.names[0]}."
                f" You take it.")
            if snack7.inVend == 5:
                item.print("~2..Don't drink too much, ok?2&")
            elif snack7.inVend <= 3:
                item.print('~2...1&')
        else:
            item.print(
                f"The vending machine whirs into action, then with a small clank, produces a single packet of "
                f"{snack.names[0]}. You take the snack.")
        player.add_inv(snack)
        snack.inVend -= 1
        if snack.inVend == 0:
            item.print('This product is now sold out.')
        end_vending()
    else:
        item.print('You retrieve the gold coin from the money box.')
        room.remove_room(room_coin)
        player.add_inv(coin)
        vending_machine.count = 0


def spider_use_again(item, ans):
    item.print("I don't understand what you want.")


def spider_kill(item):
    from game_objects import dead_spider, monster_energy_gun
    from main import room
    item.print(
        "~3Yes you monster, you horribly slaughter the innocent creature by pounding into it with your Energy Gun over "
        "and over until it stops twitching, are you happy now?")
    room.remove_room(item)
    room.add_room(dead_spider)
    monster_energy_gun.Description = ["""...
  ~2You've..
  ~1...changed.2&""", None, """...
  ~2You've..
  ~1...changed.2&"""]
    monster_energy_gun.useDescription = ["""...
  ~2Don't you dare use that thing.
  ~2murderer.2&""", None, """...
  ~2Don't you dare use that thing.
  ~2murderer.2&"""]


def theyit(string, plus):
    if plus:
        return string, f"{string} {plus} it", f"{string} {plus} them"
    return string, string + ' it', string + ' them'


def spider_use(item, ls):
    from game_objects import monster_energy_gun, snack9, dead_rat, spider
    from main import player, room
    from events import spiderName, SpiderName
    global bnc
    if room.tickActions == ratHunt_Tick:
        item.print('{S} is a bit preoccupied at the moment.'.format(S=SpiderName))
        return
    ans = multi(item, "What would you like to do with {s}? ".format(s=spiderName),
                ([('b', 'back', 'return', 'escape'), theyit('leave', None)],
                 [('fire', 'gun', 'fire gun', 'fire my gun')],
                 [theyit('feed', None)],
                 [('dance', 'song'), theyit('tame', None), theyit('train', None), theyit('command', None),
                  theyit('order', None)],
                 [theyit('name', None), theyit('rename', None)],
                 [('run')],
                 [('let it be', 'let be', 'let them be')],
                 [theyit('look', None), theyit('observe', None), theyit('examine', None), theyit('inspect', None)],
                 [theyit('pet', None), theyit('pat', None), theyit('stroke', None), theyit('touch', None),
                  theyit('caress', None)],
                 [theyit('poke', None)],
                 [('hold like a borger', 'hold it like a borger', 'hold them like a borger', 'pick up', 'pick it up',
                   'pick them up'), theyit('hold', None), theyit('take', None), theyit('get', None)],
                 [theyit('hug', None), theyit('cuddle', None), theyit('love', None), theyit('care', None),
                  theyit('care', 'for')],
                 [theyit('play', 'with'), theyit('tickle', None), theyit('amuse', None), theyit('befriend', None)],
                 [theyit('flirt', 'with'), theyit('impress', None)],
                 [theyit('kiss', None), theyit('smooch', None), theyit('make out', 'with')],
                 [theyit('date', None), theyit('go out', 'with')],
                 [theyit('speak', 'to'), theyit('speak', 'with'), theyit('talk', 'to'), theyit('chat', 'to'),
                  theyit('chat', 'with'), theyit('gossip', 'with'),
                  theyit('converse', 'with'), theyit('communicate', 'with'), theyit('ask', None),
                  theyit('deep talk', 'with')],
                 [theyit('tease', None), theyit('prank', None), theyit('trick', None)],
                 [theyit('eat', None), theyit('devour', None), theyit('consume', None), theyit('swallow', None),
                  theyit('chew', None)],
                 [theyit('kill', None), theyit('murder', None), theyit('destroy', None), theyit('eliminate', None),
                  theyit('annihilate', None), theyit('obliterate', None), theyit('exterminate', None)],
                 [theyit('harm', None), theyit('hurt', None), theyit('attack', None), theyit('hit', None),
                  theyit('squash', None), theyit('squish', None), theyit('kick', None), theyit('punch', None),
                  theyit('throw', None), theyit('stomp', None), theyit('betray', None)],
                 [theyit('torture', None), theyit('torment', None), theyit('burn', None), theyit('bash', None),
                  theyit('smash', None), theyit('crush', None), theyit('stab', None)],
                 [theyit('manipulate', None), theyit('abuse', None), theyit('bully', None), theyit('traumatise', None),
                  theyit('gaslight', None), theyit('threaten', None), theyit('terrify', None), theyit('horrify', None),
                  theyit('petrify', None), theyit('backstab', None), theyit('blackmail', None)],
                 ['nothing'],
                 [theyit('abandon', None), theyit('desert', None), theyit('neglect', None), theyit('ignore', None),
                  theyit('perturb', None), theyit('unsettle', None), theyit('upset', None), theyit('disturb', None),
                  theyit('unnerve', None)],
                 [theyit('scream', 'at'), theyit('shout', 'at'), theyit('shriek', 'at'), theyit('yell', 'at'),
                  theyit('spook', None), theyit('scare', None), theyit('alarm', None), theyit('frighten', None),
                  theyit('startle', None), theyit('surprise', None),
                  theyit('unnerve', None),
                  ('creep out', 'creep it out', 'creep them out', 'freak out', 'freak it out', 'freak them out')]
                 ), spider_use_again, False, True)
    if ans == 0:
        return
    elif ans == 1:
        if monster_energy_gun in player.inv:
            spider_kill(item)
        else:
            item.print("""...
      ~2ahaha
      ~1You don't even have a gun!3&""")
    elif ans == 2:
        feed = input(f"What would you like to feed them? ")
        all_items = room.items + player.inv
        for item in all_items:
            if feed in item.names:
                if feed in snack9.names:
                    item.print("""You feed {s} a packet of Berries and Cream.
                     ~2If you prompt them enough, they might just break into a dance.2&""".format(s=spiderName))
                    bnc = True
                    return
                if feed in dead_rat.names:
                    item.print("""~2Yes.
                     ~1It'll get to that in just a moment.2&""")
                if feed in spider.names:
                    item.print("~2Well this is awkward1&")
                else:
                    item.print("You're not sure if this is edible for the spider.")
                return
        item.print("You don't have that with you.")
    elif ans == 3:
        item.print("""You command {s} to dance.
    ~2They begin to dance...2&""".format(s=spiderName))
        if bnc:
            #      playsound('little_lad_dance.mp3')
            spiderstatus = '{S} is doing the Little Lad Dance :))'
            bnc = False
        else:
            #      playsound('spider_dance.mp3')
            spiderstatus = 'The arachnid sways erratically to the non-diegetic music.'
    elif ans == 4:
        if first['spider'] < 5:
            item.print("Not yet. You need to get to know them better first :)")
        else:
            name = input("What would you like to name them? ")
            spider.names = ['spider']
            if name:
                naming_ceremony(name)
                if name == spiderName:
                    item.print("{S} will continue to be referred to as {s}.".format(s=spiderName, S=SpiderName))
                else:
                    item.print("{S} will now be referred to as ".format(S=SpiderName) + name + ".")
            else:
                if SpiderName != spiderName:
                    item.print("{S} will continue to be referred simply as '{s}'.".format(s=spiderName, S=SpiderName))
                else:
                    item.print("{S} will simply be referred to as 'the spider' from now on.".format(S=SpiderName))
                default_spider()

    else:
        spider_response = ['', '', '', '', '',
                           """No need to be afraid!
    ~1They're just a spider after all...1&""",
                           ':)',
                           """You exchange a knowing glance with {s}.
    ~2swag.1&""",
                           """You pet {s}.
    ~2Fluffy. It gives you an oddly comforting shiver down your spine.""",
                           """You poke {s}.
    ~2somft.1&""",
                           """You hold {s} like a borger.
    They wriggle in your grasp.""",
                           """You hug {s}.
    ~2{S} is stunned. They look up at you inquisitively.""",
                           """You tickle {s}.
    ~2{S} isn't impressed.""",
                           "~1You wonder, do spiders blush?1&",
                           """You give {s} a heartfelt kiss.
    ~2Aww <33""",
                           "As much as that is adorable, this is not a dating sim.",
                           """~2Y'know.
    ~2There was a tiny, insignificant, foolish spider
    ~3who one day decided to climb a drainpipe.
    ~3heh.
    ~1Stupid idea, right?
    ~~~1.5The downpour was bound to come.
    ~3The spider tried to stay strong,
    ~~~1.5but it was in vain.
    ~2The storm washed the spider out.
    ~~~1.5And the spider, being so incompetent and gullible,
    ~3was shattered.
    ~2But after a long, hard day, the sunshine eventually returned, didn't it?
    ~4You know it did.
    ~1It dried up the rain.
    ~1And that scares the spider sometimes,
    ~2Because it's as though the storm never really happened.
    ~3Still, the question remains:
    ~3Will the itsy-bitsy spider climb up the spout again?3&""",
                           """You show off to {s} with your well-practised disappearing thumb trick.
    ~3{S}'s eyes visibly widen as they try to comprehend this phenomenon.2&""",
                           """~~~0.5I..um...
    ~1Please do not eat the spider.
    ~1There's literally a snack machine in front of you
    ~2So Please don't do that, ok?1&""",
                           """...
    ~2What would you do that for?
    ~~~1.5Why???""",
                           """~1No.
    ~1Why would a person like you do such a thing.
    ~2Do not even think about it.""",
                           """~2aaaa
    ~2aaaaaaaaaaaa
    ~3AaaaAAAAAAAAaaaaAAAAAAAAAAAAAAAAAAAAAA...
    ~5..don't you dare.2&""",
                           "~2You're scary.1&",
                           "~2You're boring.1&",
                           """...2&
    mhm.~1""",
                           """Gahh!!!
    ~1Stop making loud noises like that! >:(1&"""
                           ]
        item.print(spider_response[ans].format(s=spiderName, S=SpiderName))
    return


def can_use(self, ls):
    from game_objects import monster_energy_gun
    from main import player
    if self.count == 7:
        if ls == Lighting.DARK:
            self.print(needLight)
        else:
            self.print("""...
      ~2What are you going to do with all of those cans, huh?
      ~4...
      ~2...Ah.
      ~1Ohhhhh
      ~~~0.8You spend several hours working at the table, meticulously crafting a..*sigh*.
      ~4a Monster Energy Gun.
      ~3...
      ~2...ehehehe
      ~2ahahahahaha...
      ~4Happy now?2&""")
            self.count = 1
            player.remove_inv(self)
            player.add_inv(monster_energy_gun)
    else:
        self.print("This item is practically worthless now.")


def monster_use(item, ls):
    from game_objects import empty_can
    from main import player
    item.countAll += 1
    num = item.countAll
    if num == 1:
        item.print("""You swiftly down the energy drink. Ahh, refreshing :)
    ~2All that remains is an empty can.2&""")
    if num == 2:
        item.print(
            "You down another drink! Woo, you feel your senses buzzing as you shift into a state of hyperfocus on the "
            "task at hand.4&")
    if num == 3:
        item.print("""You guzzle down another can!! Boy are you feeling ambitious today! hehe
    ~3Even so, you think to yourself that it would be detrimental to your health if you indulged yourself any further.4&""")
    if num == 4:
        item.print("""Glug,
    ~1glug,
    ~1glug.
    ~1
    ~2hey
    ~2are you ok?2&""")
    if num == 5:
        item.print("""glug
    ~~~0.8glug
    ~~~0.8glug.
    ~~~0.8
    ~2You should sto
    ~~~0.5You tell yourself that you should stop.2&""")
    if num == 6:
        item.print("""glug
    ~~~0.6glug
    ~~~0.6glug
    ~~~0.6
    ~1..i...
    ~2..i'm sorry.2&""")
    if num == 7:
        item.print("""glug
    ~~~0.4glug
    ~~~0.4glug
    ~~~0.4
    I'm sorry, dammit!
    ~1This was a bad idea
    ~1this was a STUPID idea
    ~1I shouldn't have forced you into this
    ~1dammit i'm sorry!!!
    ~2
    ~~~0.5Just please...
    ~4DON'T BLAME YOURSELF FOR THIS!!!!3&""")
    player.add_inv(empty_can)
