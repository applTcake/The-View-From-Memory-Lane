from main import player, room, end_game
from events import *

# start_game()
# intro()
default_spider()
spider_friend()
# room.startTick()
while not end_game:
    room.tick()
    events()
    player.act(input('> '))
    player.tickAll()
