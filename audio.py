import winsound
from os.path import exists
import time
import random

# tinnitus in background?
#for i in range(10):
#    winsound.Beep(4280, 4000)

file_path_front = ".\\resources\\"
file_path_back = ".wav"

last_round_lighting = None
sfx = True

def sound(text):
    if sfx:
        if text == 'light_match':
            text += str(random.randint(1, 4))
        if text == 'page_flip':
            text += str(random.randint(1, 12))
        file_path = file_path_front + text + file_path_back
        winsound.PlaySound(file_path, winsound.SND_ASYNC)


def loop(text):
    if sfx:
        file_path = file_path_front + text + file_path_back
        winsound.PlaySound(file_path, winsound.SND_LOOP + winsound.SND_ASYNC)

# call coin effect 'coin_drop'
def music(ls, uv):
    from statuseffects import Lighting
    from game_objects import matches
