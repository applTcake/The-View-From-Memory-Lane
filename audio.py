import winsound
from os.path import exists
import time

# tinnitus in background?
#for i in range(10):
#    winsound.Beep(4280, 4000)

file_path_front = "C:\\Users\\ariel\\ye got games on your phone\\TextAdventure\\resources\\"
file_path_back = ".wav"

last_round_lighting = None


def sound(text):
    file_path = file_path_front + text + file_path_back
    winsound.PlaySound(file_path, winsound.SND_ASYNC)


def loop(text):
    file_path = file_path_front + text + file_path_back
    winsound.PlaySound(file_path, winsound.SND_LOOP + winsound.SND_ASYNC)


def music(ls, uv):
    from statuseffects import Lighting
    from game_objects import matches
    if last_round_lighting == ls:
        if ls == Lighting.DARK:
            loop('quiet')
    if matches.lightEmit:
        loop('match_back')
