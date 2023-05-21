from main import player, room, end_game
from events import *
import audio

#start_game()
#intro()
#Below starts spider tick
#room.start_tick()
while not end_game:
    room.tick()
    events()
    audio.music(player.get_lighting_status(), player.get_uv_status())
    audio.last_round_lighting = player.get_lighting_status()
    player.act(input('> '))
    player.tickAll()
