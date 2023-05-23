from game_objects import *
from util import *
import audio

bnc = False
back = ['b', 'back', 'return', 'escape', 'esc']

#The Calm Message + potential loss of innocence
def ease_to_dark():
    from main import player
    from game_objects import torch
    if player.get_lighting_status() == Lighting.DARK:
        player.print("You're welcomed once more into a realm of merciful darkness.")
        if torch.lightEmit and first['torch']:
            lose_innocence(player, 1)


def matches_use(item, ls):
    #If match is ticking, can blow out match
    if item.counter > 0:
        if yn("Blow out matchstick? (yep/nope) ") == 0:
            item.stop_tick()
            item.lightEmit = False
            audio.sound('flame_blow')
            ease_to_dark()
    #No matches ;-;
    elif item.count == 0:
        item.print("You don't have any matches left to light.")
    #Otherwise, match can be struck
    else:
        audio.sound('light_match')
        if ls == Lighting.DARK:
            item.print('You strike a match. You start to discern some things in front of you.')
            if first['match']:
                item.print('~2..Turn back now. This is your final warning.2&')
                first['match'] = False
        #In light or dim lighting
        else:
            item.print("You strike another match. The room is already bright enough to see because of the candle.")
        item.decrement()
        item.start_tick()
        item.lightEmit = True


def candle_use(item, ls):
    from game_objects import matches
    #Toggle on
    if ls == Lighting.DIM:
        #First time
        if first['candle']:
            audio.sound('flame_crackle')
            item.print("""As you transfer the flame of the match to the candle, you are taken aback by how vibrantly the wick blazes up.
      ~3It is as though the candle has been aching for this precise moment for a very, very long time.
      ~4The brightness hurts your eyes a little, as the dancing light illuminates your vicinity with greater clarity.4&""")
            first['candle'] = False
        #Not first time ;)
        else:
            audio.sound('flame_crackle')
            item.print('The fire returns to the candle, with the vigour of a starved traveller drinking from an oasis.2&')
        #Blow out match, stop tick
        audio.sound('flame_blow')
        item.print("You blow out the match.")
        matches.stop_tick()
        matches.LightEmit = False
        item.lightEmit = True
    #Toggle off
    else:
        if yn('Blow out candle? (yup/nup) ') == 0:
            audio.sound('flame_blow')
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
    #Toggle on
    if not torch.lightEmit:
        item.print('A muted blue glow shines out from the torch, barely visible to the eye.')
        if ls == Lighting.DARK and first['torch']:
            lose_innocence(item, 0)
        elif not first['torch']:
            item.print('Another great example of a pathetic UV flashlight.')
    # Toggle off
    else:
        item.print('You turn off the torch.')
    torch.lightEmit = not torch.lightEmit


news = [[[' dodgy newspaper article', 'headline'],'DADADADADA',
         'Someone went missing..guess who took them.',
         """Someone went missing..guess who took them. (us. yes, this dodgy newspaper company is the one behind this dodgy case.
         Go ahead. Sue us.)"""],
        [[' dodgy newspaper article', 'headline'], 'MISSING PERSONS', """see previous article.
        yeah so someone really important went missing.""",
         "yeah so someone really important went missing. (if you ship us 10000kg of candy to our headquarters we will "
         "tell you where they are/return them to you if we're feeling generous.)"],
        [['n article from a magazine', 'heading'], 'CHAMELEON FACTS 101 - THE SPECIES OF SWAGGER',
         """* chamelions are great they inhabit warm climets, like reinforests and desserts
         * chamelions dont actually chanj colour to blend into suroundings - they use it to reflect their mood :DD as they shoud
         * and they actually chanj colour using salt cristlz in their skin, they stRETCh their skin to chanj colour. VERY COOL
         * chamelion tails are very stronk and long - they help rap around branches and support climing
         * chamelion tungs are ruffly 1.5 to 2 times longer than the body :OOO The tung is usually coiled up like a spring, and then shoot out at food
         * chamelion spit is 1000 times stikkier than human spit    good for catching food
         * Half of chameleon species are endangered, due to range restrictions and habitat conditions, making them more vulnerable to the effects of climate change and thus more prone to extinction.
         
         Moving on :DDD
         * chamelion eyes muv independependedently, so they have 360 degreee vison. They can also see an insekt 10 metres away :0
         * chamelions eat lotta plamts. rodents and birbs too, but also PLAMTS. (and insekts)
         * chamelions like lots of time alone - they get strest when too near other kreechurs :-: SO RESPECT BOUNDRIES!!!
         * chamelions can see altraviolettt!! they use it communicate with other chamelions!!!
         * chamelions even glow under UV lite!! And the glow comes from their bones :0000
         * chamelions shed less skin when they are old
         
         (Alongside the text is an image of an aquamarine Parsons chameleon. The caption reads: "some chamelions are as big as cat : DDDD")""",
         """There is a single comment near the bottom-right corner of the page. It reads:
         
            I wish I were a solitary creature.
         
         The image of the Parsons chameleon has an odd, compelling pattern on its head."""],
        [['n overzealous advert poster', 'heading with 3D fluorescent block letters'], 'TAKE A BREAK!!',
        """TAKE A BREAK, AND GET AWAY!
        
        RUN AWAY WITH US FOR THE SUMMER. LET'S GO UPSTATE!!
        
        (The poster has a stock photo of a nuclear family with hiking equipment, photoshopped in front of a countryside resort in Sweden or some place.)""", ""],
        [[' random piece of paper from an unknown source,', 'hastily-scribbled title'], 'FEBRUARY 16th - Transcript',
         """~2Today is a bad day.
         ~2There isn't any news to suggest that as such. In fact, it's more peaceful than usual.
         ~4But I've just got this feeling, you know?
         ~3Something terrible is going down.
         ~2Wish I knew what it was.
         ~3Hang on, who turned off the lights?
         ~~~1.5Could someone please turn on the lights?
         ~~~1.5Is this some kind of sick joke?
         ~~~1.5Hello???""",
         """<starts reading>
         
         ~5Why did you stop? Come on, keep reading.
         
         ~2<continues reading>
         
         ~3...
         ~2Look I know you're upset, but you've got to think...
         ~3You haven't learned anything.
         ~2You haven't even tried.
         ~2And you can't even utter a single thank you for all the effort I've put into this project for you, huh.
         ~5And no, I'm not angry at you.
         ~~~1.5But I'm not sorry for you either.
         ~2Just...I wish you'd say something.
         ~5By all means, please, enjoy being in denial for a couple years more.
         ~3Hell, I could turn off this torch for you right now."""
         ]]


def article_flip(item, ls):
    from game_objects import torch, coin
    from main import player
    ans = None
    p = ['p', 'prev', 'previous']
    n = ['n', 'next', 'next']
    b = back
    while ans != b:
        audio.sound('page_flip')
        # Full article in light
        if ls == Lighting.LIGHT:
            item.print('\n' + news[item.count][1] + '\n\n' + news[item.count][2] + '\n')
        # Abridged article in dim
        elif ls == Lighting.DIM:
            item.print(f"""It is a{news[item.count][0][0]} with the {news[item.count][0][1]}: {news[item.count][1]}.
            You'll need some more light to read all of it.""")
        #Torch mode
        if torch.lightEmit and news[item.count][3]:
            #First Experience TM
            if first['uv_news']:
                item.print("""~4Oh.
        ~1The torchlight reveals something else written on the paper.3&""")
                #Can't read, too bright
                if ls != Lighting.DARK:
                    item.print("""A series of annotations, urgently scrawled out on its margins.2&
          The light is feeble, so you'll need to darken the room to see it more clearly.2&""")
                first['uv_news'] = False
            #Not first time
            elif ls != Lighting.DARK:
                item.print("""The torchlight reveals something else written on the paper: a series of annotations, urgently scrawled out on its margins.
                   The light is feeble, so you'll need to darken the room to see it more clearly.""")
            #Full article in torch-mode
            if ls == Lighting.DARK:
                item.print('\n' + news[item.count][1] + '\n\n' + news[item.count][3] + '\n')
        #WHAT IS THIS EVEN DOING HERE YOU SHOULDN'T BE HERE
        elif ls == Lighting.DARK:
            item.print('\n' + news[item.count][1] + '\n\n' + uvNothing + '\n')
        #Move articles first
        if item.count == 0:
            ans = multi(None, "(Type 'next' to move between articles. Type 'back' to return.) ", (b, n), try_again=None,
                        original_result=True, tuples=False)
        # Move articles last
        elif item.count == len(news)-1:
            if first['coin'] == 0:
                first['coin'] = 1
            ans = multi(None, "(Type 'previous' to move between articles. Type 'back' to return.) ", (b, p),
                        try_again=None, original_result=True, tuples=False)
        # Move articles middle
        else:
            ans = multi(None, "(Type 'previous' or 'next' to move between articles. Type 'back' to return.) ",
                        (b, p, n), try_again=None, original_result=True, tuples=False)
        if ans == p:
            item.decrement()
        elif ans == n:
            item.increment()
    #Coined the coin
    if first['coin'] == 1:
        audio.sound('coin_drop')
        item.print("""As you're rifling through the pages, a single coin falls to the table, spinning and rattling briefly as it comes to a stop near your fingertips.
    ~5You take the coin.1&""")
        player.add_inv(coin)
        first['coin'] = 2

#Mayyybe do something about this repetition?
def snack_describe(item, ls):
    from main import player, room
    #Make list of all snacks in inv
    treats = []
    for items in player.inv:
        if items in player.snacks:
            treats.append(items)
    #If no snacks
    if len(treats) == 0:
        item.print("You'll need to buy one first.")
    #If yes snack
    elif len(treats) == 1:
        items.describe(room.get_lighting_status(player), room.get_uv_status(player))
    #If yes snacks
    else:
        item.print("Which snack are you referring to?")


def snack_use(item, ls):
    from main import player, room
    # Make list of all snacks in inv
    treats = []
    for items in player.inv:
        if items in player.snacks:
            treats.append(items)
    # If no snacks
    if len(treats) == 0:
        item.print("You'll need to buy one first.")
    # If yes snack
    elif len(treats) == 1:
        items.use(player, room.get_lighting_status(player), room.get_uv_status(player))
    # If yes snacks
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
        #Start spider tick
        room.start_tick()
    vending_machine.count = 2
    room.add_room(room_coin)


def vending_use(item, ls):
    from game_objects import vending_machine, coin, room_coin, money_box, keypad, snack7, torch, coin_slot
    from main import player, room
    #If describing box and coin not in room...naturally the coin is not in the box.
    if item == money_box and room_coin not in room.items:
        item.print('The money box is currently empty.')
        return
    #If coin in vending machine/player doesn't know about the money box...
    elif vending_machine.count == 0 or first['machine'] == 2 or (
            item in [keypad, coin_slot] and vending_machine.count == 2):
        #...and coin is not in inv...
        if coin not in player.inv:
            #...AND player wants to use said coin, don't give it to them.
            if item == room_coin:
                item.print("You don't have that with you right now.")
            #Else respond with a flippant remark :o)
            else:
                item.print("You'll need to insert a coin first.")
            return
        #Else, well I guess everything works out then
        else:
            audio.sound('vending_in')
            item.print('You insert the coin into the vending machine. The keypad glows up, faint as it may be.')
            player.remove_inv(coin)
            #Pause for Emotional Reunion moment
            if first['machine'] == 0:
                item.print("""~3...wow.
        ~2it...still works.2&""")
                first['machine'] += 1
            #Begin phase 1 ;)
            vending_machine.increment()
    if vending_machine.count == 1:
        while True:
            code = int(multi(item, "Enter number into keypad (press 'back' to return): ",
                             (['001', '01', '1'], ['002', '02', '2'], ['003', '03', '3'],
                              ['004', '04', '4'], ['005', '05', '5'], ['006', '06', '6'],
                              ['007', '07', '7'], ['008', '08', '8'], ['009', '09', '9'],
                              ['216'],
                              back), try_again=keypad_nope, original_result=False, tuples=False))
            #Back
            if code == 10:
                return
            #Torch code
            elif code == 9:
                if torch not in player.inv:
                    audio.sound('vending_out')
                    item.print("""The vending machine whirs into action, then with a small clank, produces a single..
          ~4...torch.
          ~2You take it with you.1&""")
                    player.add_inv(torch)
                    end_vending()
                    return
                else:
                    item.print('This product is already sold out.')
            #Sorting snacks
            else:
                snack = player.snacks[int(code)]
                if snack.inVend == 0:
                    item.print('This product is already sold out.')
                else:
                    break

        #Monster energy
        if snack == snack7:
            audio.sound('vending_out')
            item.print(
                f"The vending machine whirs into action, then with a small clank, produces a single {snack.names[0]}."
                f" You take it.")
            if snack7.inVend == 5:
                item.print("~2..Don't drink too much, ok?2&")
            elif snack7.inVend <= 3:
                item.print('~2...1&')
        #Everything else
        else:
            audio.sound('vending_out')
            item.print(
                f"The vending machine whirs into action, then with a small clank, produces a single packet of "
                f"{snack.names[0]}. You take the snack.")
        player.add_inv(snack)
        snack.inVend -= 1
        if snack.inVend == 0:
            item.print('This product is now sold out.')
        end_vending()
    #coin retrieved!
    else:
        item.print('You retrieve the gold coin from the money box.')
        room.remove_room(room_coin)
        player.add_inv(coin)
        vending_machine.count = 0


def spider_use_again(item, ans):
    from game_objects import spider
    item.print(f"{spider.nickname[1]} doesn't understand your intentions.")


def spider_kill(item):
    from game_objects import dead_spider, monster_energy_gun
    from main import room
    #The killing
    item.print(
        "~3Yes you monster, you horribly slaughter the innocent creature by pounding into it with your Energy Gun over "
        "and over until it stops twitching, are you happy now?")
    room.remove_room(item)
    room.add_room(dead_spider)
    #Character development for the gun
    monster_energy_gun.Description = same2("""...
  ~2You've..
  ~1...changed.2&""")
    monster_energy_gun.useDescription = same2("""...
  ~2Don't you dare use that thing.
  ~2murderer.2&""")


def theyit(string, plus):
    if plus:
        return string, f"{string} {plus} it", f"{string} {plus} them"
    return string, string + ' it', string + ' them'

"""
So if you type:
    theyit('point at', None)
It would return:
    'point at', 'point at it', 'point at them'
       ^
But if you type:
    theyit('point', 'at')
It would return:
    'point', 'point at it', 'point at them'
       ^

Small difference, goes a long way
"""


#Don't remove these, they are also used in game_objects ;)
spiderStory = """~2Y'know.
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
    ~3Will the itsy-bitsy spider climb up the spout again?3&"""

spiderFace = "~2Stop making faces like that, you're scaring the spider.2&"


def spider_use(item, ls):
    from game_objects import monster_energy_gun, snack9, dead_rat, spider
    from main import player, room
    #from events import spiderName, SpiderName
    global bnc, spiderstatus
    #Do be draggin that rat away--
    if room.tickActions == ratHunt_Tick:
        item.print(f'{spider.nickname[1]} is a bit preoccupied at the moment.')
        return
    ans = multi(item, f"What would you like to do with {spider.nickname[0]}? ",
                ([back, theyit('leave', None)],
                 [('fire', 'gun', 'fire gun', 'fire my gun')],
                 [theyit('feed', None)],
                 [('dance', 'song'), theyit('tame', None), theyit('train', None), theyit('command', None),
                  theyit('order', None), theyit('pressure', None), theyit('peer pressure', None)],
                 [theyit('name', None), theyit('rename', None)],

                 [('run')],
                 [('let it be', 'let be', 'let them be')],
                 [theyit('look', 'at'), theyit('observe', None), theyit('examine', None), theyit('inspect', None),
                  theyit('eye', None), theyit('glance', 'at'), theyit('view', None), theyit('see', None),
                  theyit('watch', None), theyit('study', None)],
                 [theyit('pet', None), theyit('pat', None), theyit('stroke', None), theyit('touch', None),
                  theyit('caress', None)],
                 [theyit('poke', None)],
                 [('hold like a borger', 'hold it like a borger', 'hold them like a borger', 'pick up', 'pick it up',
                   'pick them up'), theyit('hold', None), theyit('take', None), theyit('get', None)],
                 [theyit('hug', None), theyit('cuddle', None), theyit('love', None), theyit('care', None),
                  theyit('care', 'for')],
                 [theyit('play', 'with'), theyit('tickle', None), theyit('amuse', None), theyit('befriend', None)],
                 [theyit('flirt', 'with'), theyit('wink', 'at')],
                 [theyit('kiss', None), theyit('smooch', None), theyit('make out', 'with')],
                 [theyit('date', None), theyit('go out', 'with'), theyit('go on a date', 'with')],
                 [('story'), theyit('speak', 'to'), theyit('speak', 'with'), theyit('talk', 'to'), theyit('chat', 'to'),
                  theyit('chat', 'with'), theyit('gossip', 'with'), theyit('converse', 'with'),
                  theyit('communicate', 'with'), theyit('ask', None), theyit('deep talk', 'with')],
                 [theyit('tease', None), theyit('prank', None), theyit('trick', None), theyit('impress', None),
                  theyit('fool', None), theyit('dupe', None), theyit('entertain', None)],
                 [theyit('pick on', None), theyit('annoy', None), theyit('irritate', None), theyit('hassle', None),
                  theyit('pester', None)],
                 [theyit('eat', None), theyit('devour', None), theyit('consume', None), theyit('swallow', None),
                  theyit('chew', None), theyit('chew', 'on'), theyit('bite', None), theyit('munch', None),
                  theyit('munch', 'on'), theyit('cronch', None), theyit('cronch', 'on')],
                 [theyit('kill', None), theyit('murder', None), theyit('destroy', None), theyit('eliminate', None),
                  theyit('annihilate', None), theyit('obliterate', None), theyit('exterminate', None),
                  theyit('assassinate', None)],
                 [theyit('harm', None), theyit('hurt', None), theyit('attack', None), theyit('hit', None),
                  theyit('squash', None), theyit('squish', None), theyit('kick', None), theyit('punch', None),
                  theyit('throw', None), theyit('toss', None), theyit('stomp', None), theyit('maim', None),
                  theyit('betray', None), theyit('anger', None), theyit('laugh at', None), theyit('insult', None),
                  theyit('deceive', None), theyit('harass', None), theyit('lie', 'to'),
                  ('lie', 'make them cry', 'make it cry')],
                 [theyit('torture', None), theyit('torment', None), theyit('burn', None), theyit('bash', None),
                  theyit('smash', None), theyit('crush', None), theyit('stab', None), theyit('crunch', None)],
                 [theyit('manipulate', None), theyit('abuse', None), theyit('bully', None), theyit('traumatise', None),
                  theyit('gaslight', None), theyit('gatekeep', None), theyit('girlboss', None), theyit('exploit', None),
                  theyit('threaten', None), theyit('terrify', None), theyit('horrify', None), theyit('petrify', None),
                  theyit('backstab', None), theyit('blackmail', None), theyit('gaslight gatekeep girlboss', None)],
                 [('nothing')],
                 [theyit('abandon', None), theyit('desert', None), theyit('neglect', None), theyit('ignore', None),
                  theyit('perturb', None), theyit('unsettle', None), theyit('upset', None), theyit('disturb', None),
                  theyit('unnerve', None), theyit('disown', None), theyit('reject', None), theyit('renounce', None),
                  theyit('forsake', None)],
                 [theyit('rob', None), theyit('steal', None)],
                 [theyit('scream', 'at'), theyit('shout', 'at'), theyit('shriek', 'at'), theyit('yell', 'at'),
                  theyit('spook', None), theyit('scare', None), theyit('alarm', None), theyit('frighten', None),
                  theyit('startle', None), theyit('surprise', None), theyit('provoke', None), theyit('unnerve', None),
                  theyit('trigger', None),
                  ('creep out', 'creep it out', 'creep them out', 'freak out', 'freak it out', 'freak them out')],
                 [theyit('smile', 'at'), theyit('grin', 'at'), theyit('beam', 'at'), theyit('leer', 'at'),
                  theyit('smirk', 'at'), theyit('sneer', 'at'), theyit('scowl', 'at'), theyit('pout', 'at'),
                  theyit('frown', 'at'), theyit('glare', 'at'), theyit('gaze', 'at'), theyit('stare', 'at'),
                  theyit('spy on', None), theyit('glower', 'at'), theyit('make faces', 'at'),
                  theyit('pull faces', 'at')]
                 ), try_again=spider_use_again, original_result=False, tuples=True)
    if ans == 0:
        return
    elif ans == 1: #fire gun
        if monster_energy_gun in player.inv:
            spider_kill(item)
        else:
            item.print("""...
      ~2ahaha
      ~1You don't even have a gun!3&""")
    elif ans == 2: #feed
        feed = input(f"What would you like to feed them? ")
        all_items = room.items + player.inv
        for item in all_items:
            if feed in item.names:
                if feed in snack9.names:
                    item.print(f"""You feed {spider.nickname[0]} a packet of Berries and Cream.
                     ~2If you prompt them enough, they might just break into a dance.2&""")
                    bnc = True
                    return
                if feed in player.snacks.names:
                    item.print("This snack doesn't strike you as spider-friendly.")
                if feed in dead_rat.names:
                    item.print("""~2Yes.
                     ~1It'll get to that in just a moment.2&""")
                if feed in spider.names:
                    item.print("~2Well this is awkward1&")
                else:
                    item.print("You're not sure if this is edible for the spider.")
                return
        item.print("You don't have that with you.")
    elif ans == 3: #dance, train, command
        item.print(f"""You command {spider.nickname[0]} to dance.
    ~2They begin to dance...2&""")
        if bnc:
            audio.sound('lil_lad_dance')
            spiderstatus = f'{spider.nickname[1]} is doing the Little Lad Dance :))'
            bnc = False
        else:
            audio.sound('spider_dance')
            spiderstatus = 'The arachnid sways erratically to the non-diegetic music.'
    elif ans == 4: #name
        if first['spider'] < 5:
            item.print("Not yet. You need to get to know them better first :)")
        else:
            name = input("What would you like to name them? ")
            spider.names = ['spider']
            if name:
                naming_ceremony(name)
                if name == spider.nickname[0]:
                    item.print(f"{spider.nickname[1]} will continue to be referred to as {spider.nickname[0]}.")
                else:
                    item.print(f"{spider.nickname[1]} will now be referred to as " + name + ".")
            else:
                if spider.nickname[1] != spider.nickname[0]:
                    item.print(f"{spider.nickname[1]} will continue to be referred simply as '{spider.nickname[0]}'.")
                else:
                    item.print(f"{spider.nickname[1]} will simply be referred to as 'the spider' from now on.")
                #default_spider()

    else:
        spider_response = ['', '', '', '', '',
                           """No need to be afraid!
    ~1They're just a spider after all...1&""", #run
                           ':)', #let be
                           f"""You exchange a knowing glance with {spider.nickname[0]}.
    ~2swag.1&""", #look, observe
                           f"""You pet {spider.nickname[0]}.
    ~2Fluffy. It gives you an oddly comforting shiver down your spine.""", #pet, touch
                           f"""You poke {spider.nickname[0]}.
    ~2somft.1&""",  #poke
                           f"""You hold {spider.nickname[0]} like a borger.
    They wriggle in your grasp.""", #hold, pick up
                           f"""You hug {spider.nickname[0]}.
    ~2{spider.nickname[1]} is stunned. They look up at you inquisitively.""", #hug, love, care for
                           f"""You tickle {spider.nickname[0]}.
    ~2{spider.nickname[1]} isn't impressed.1&""", #play with, befriend
                           "~1Can spiders blush?1&", #flirt
                           f"""You give {spider.nickname[0]} a heartfelt kiss.
    ~2Aww <33""", #kiss
                           "As much as that is adorable, this is not a dating sim.", #date
                           spiderStory, #talk
                           f"""You show off to {spider.nickname[0]} with your well-practised disappearing thumb trick.
    ~3{spider.nickname[1]}'s eyes visibly widen as they try to comprehend this phenomenon.2&""", #tease, trick, impress, entertain
    f"""~1Oi!
     ~1Stop stroking {spider.nickname[0]} the wrong way! 
     ~2Rude :/""", #pick on, annoy
                           """~~~0.5I..um...
    ~1Please do not eat the spider.
    ~1There's literally a snack machine in front of you
    ~2So Please don't do that, ok?1&""", #eat
                           """...
    ~2What would you do that for?
    ~~~1.5Why???""", #kill
                           """~1No.
    ~1Why would a person like you do such a thing.
    ~2Do not even think about it.""", #harm, betray
                           """~2aaaa
    ~2aaaaaaaaaaaa
    ~3AaaaAAAAAAAAaaaaAAAAAAAAAAAAAAAAAAAAAA...
    ~5..don't you dare.2&""", #torture
                           """...
                           ~2You're scary.1&""", #manipulate, terrify
                           "~2You're boring.1&", #nothing
                           """...2&
    mhm.~1""", #ignore, disturb, disown
    """You rob the spider of your attention. You're just too cool and too busy to get hang up on the matters of eight-legged insects.
    ~6Hang on, are spiders insects?1&""", #rob
                           """Gahh!!!
    ~1Stop making loud noises like that! >:(1&""", #scream, freak out
    spiderFace #smile, scowl, stare, pull faces
                           ]
        item.print(spider_response[ans])
    return

def can_use(self, ls):
    from game_objects import monster_energy_gun
    from main import player
    #If enough cans, check for light, and build
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
            #insta-remove all cans from inv, replace with gun
            self.count = 1
            player.remove_inv(self)
            player.add_inv(monster_energy_gun)
    else:
        self.print("This item is practically worthless now.")
        # Just you wait, just you wait.


def monster_use(item, ls):
    from game_objects import empty_can
    from main import player
    #Count number of cans that have been used, print messages accordingly
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
    #add can every time
    player.add_inv(empty_can)
