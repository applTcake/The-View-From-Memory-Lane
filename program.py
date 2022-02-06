from main import player, room, end_game
from events import *

start_game()
intro()
#room.start_tick()
while not end_game:
    room.tick()
    events()
    player.act(input('> '))
    player.tickAll()
