from main import player, room, end_game
from events import *
from util import Tickable

start_game()
intro()
# room.startTick()
while end_game == False:
    room.tick()
    events()
    player.act(input('> '))
    player.tickAll()
